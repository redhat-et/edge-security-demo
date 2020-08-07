from flask import Flask, Response, request
from flask import render_template, send_file
import threading
import argparse
import datetime
import imutils
import time
import cv2
import requests
import numpy as np
from PIL import Image
from flask import jsonify
import time


outputFrame = None 
lock = threading.Lock()

app = Flask(__name__, template_folder='templates')

@app.route("/")
def index():
	return render_template('index.html')

def stream_to_memory():
	global outputFrame, lock	
	list1 = request.json['instances']
	for l in list1:
		img=np.asarray(l, dtype=np.uint32)
		outputFrame = Image.fromarray(img.astype('uint8'))


@app.route("/video")
def video():
	def produce_frame(): 
		global outputFrame, lock 
		
		while True: 
			if outputFrame is None: 
				continue
			
			image1 = np.asarray(outputFrame)
			(flag, image) = cv2.imencode(".JPEG", image1)

			if not flag:
				continue
			
			yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
				bytearray(image) + b'\r\n')
			time.sleep(1.0)

	return Response(produce_frame(), mimetype = "multipart/x-mixed-replace; boundary=frame")
			
				
@app.route("/video_stream", methods=['POST'])
def video_stream():
	stream_to_memory()
	return 'OK'
	
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, debug=True, threaded=True, use_reloader=False)