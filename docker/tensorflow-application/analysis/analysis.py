from __future__ import absolute_import, division, print_function, unicode_literals

import pathlib
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import cv2
import subprocess
import time
import base64
import json 
import imageio

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

import importlib

from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

importlib.reload(vis_util)

import datetime
import time
import cv2
import requests
from io import BytesIO
import http.client as httplib

#This will need to be imported from an envionment variable 
tf_url = "http://0.0.0.0:8050/v1/models/default:predict"
DEBUG = False 
#conn = httplib.HTTPConnection('127.0.0.1', timeout=5)

# Tensorflow Model ZOO inference Libraries 
def get_category_index(label_path):
  """ Transforms label map into category index for visualization.

      Returns:
          category_index: The category index corresponding to the given
              label map.
  """
  label_map = label_map_util.load_labelmap(label_path)
  categories = label_map_util.convert_label_map_to_categories(
                  label_map,
                  max_num_classes=90,
                  use_display_name=True)
  category_index = label_map_util.create_category_index(categories)
  return category_index

#Function Acceps a batch of images
def run_inference_for_batch_of_images(tf_url, images):
    """ Takes in batch of video frames to send to TFServing Container

        Args:
            tf_url: The URL for the tf Serving Contianer(Will need to read in from environment)
            images: The list of images to send to the server.
            i: An integer used in iteration over input images.
    """
    #instances we're sending to TF serving in b64 encoded strings
    #original png formatted images
    raw_numpy = []
    for image in images:
        raw_numpy.append(np.array(image))
    
    #Convert list of images to np.array's of images
    payload = {"instances": [np.array(image).tolist() for image in images]}
    
    print("Number of Images in Batch: " + str(len(images)))
    #Send batc to Tensorflow Serving for inference
    print("POSTing image to " + tf_url + " Awaiting response...")
    json_response = requests.post(tf_url, json=payload)
    print(json_response)
    print("Response received.")

    # Write output to a .txt file DEBUGGING 
    if DEBUG:
        output_file = "output.txt"
        with open(output_file, "w") as out:
            out.write(json_response.text)

    # Extracts the inference results
    output_dict = json.loads(json_response.text)
    output_dict = output_dict["predictions"]
    
    #Loops through the results and extracts necessary data for bounding box drawing 
    out_dictionaries = []
    for num, image_dict in enumerate(output_dict): 
        tmp_dict = {}
        detection = image_dict.pop('num_detections')
        for key,value in image_dict.items():
            tmp_dict[key] = np.array(value[0:int(detection)])
        
        tmp_dict['num_detections'] = int(detection)
        out_dictionaries.append(tmp_dict)
    
    for tmp_dict in out_dictionaries:
        tmp_dict['detection_classes'] = tmp_dict['detection_classes'].astype(np.int64)
    
        if 'detection_masks' in tmp_dict:
            # Reframe the the bbox mask to the image size.
            detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                        output_dict['detection_masks'], output_dict['detection_boxes'],
                        image.shape[0], image.shape[1])      
            detection_masks_reframed = tf.cast(detection_masks_reframed > 0.3,
                                                tf.uint8)
            output_dict['detection_masks_reframed'] = detection_masks_reframed.numpy()
    # Visualizes inferred image
    return show_inference(raw_numpy, out_dictionaries)

  

#Overlays the results from image analysis onto frame
#Accepts the output dictionary from tensorflow serving 
#Returns an array of inferenced images in np.array format
def show_inference(input_images, output_dict):
    """ Decodes JSON data and converts it to a bounding box overlay
            on the input image, then saves the image to a directory.

        Args:
            input_image: The string representing the input image.
            response: The list of response dictionaries from the server.
            i: An integer used in iteration over input images.
    """
    out_images = []
    for num, image in enumerate(input_images):
        output_dict_tmp = output_dict[num]
        print(image.shape)
        print(output_dict_tmp)
        vis_util.visualize_boxes_and_labels_on_image_array(
            image,
            output_dict_tmp['detection_boxes'],
            output_dict_tmp['detection_classes'],
            output_dict_tmp['detection_scores'],
            category_index,
            instance_masks=output_dict_tmp.get('detection_masks_reframed', None),
            use_normalized_coordinates=True,
            line_thickness=2,
            min_score_thresh=.3)

        out_images.append(image)
    return(out_images)
    #visualization_utils.save_image_array_as_png(image, output_file)

#Function to read in frames and do analysis as long as video sream is active 
def generate():

    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "protocol_whitelist;file,tcp,https,tls"
    cap = cv2.VideoCapture("carVideo.mp4")

    #Frame count 
    i = 0
    #Segment count
    j = 0

    #While incoming video is received from IoT Device Simulator
    batch = []
    while(cap.isOpened()): 

        # Capture frames 
        ret, tempframe = cap.read()
        if ret == True: 
            #Run inference on video Frame    
            #Add add every other frame to inference batch for speed up)
            if(i != 0 and i%2 == 0):
                batch.append(tempframe)
            #Every 5 Frames Send batch to TF_serving container 
            if (i%10 == 0 and i != 0):

                #Considering a Video with 30fps make 3 second clip with at 90fps
                if(i == 90):
                    #Re-Zero frame count
                    i=0
                    j = j+1

                #Otherwise send frames for inference and append them to the current video segment 
                else:
                    out_batch = run_inference_for_batch_of_images(tf_url,batch)
                    #Send out_batch to the video server
                    send_to_videoserver(out_batch)
                batch = []

                i = i + 1
            else:
                #Be sure to always increment frame number
                i = i + 1
                continue
    #Clear variables before closing module 
    j = 0
    i = 0

def send_to_videoserver(images):
	payload = {"instances": [np.array(image).tolist() for image in images]}
    # TODO Change to streaming service's IP
	response = requests.post("http://0.0.0.0:8080/video_stream", json=payload)
	return response

if __name__ == "__main__":
    PATH_TO_LABELS = 'models/research/object_detection/data/mscoco_label_map.pbtxt'
    category_index = get_category_index(PATH_TO_LABELS)
    generate()
