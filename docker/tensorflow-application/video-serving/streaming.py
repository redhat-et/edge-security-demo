from flask import Flask, Response, request
from flask import render_template, send_file
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
from collections import deque

app = Flask(__name__, template_folder='templates')

# Queue implemented for consistent FPS
# TODO Use a Kafka queue which can help us to decouple the two applications 
# (analysis and streaming) and provide a more scalable approach.
q=deque(maxlen=5)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/video")
def video():
	def produce_frame():
		while True:
			if len(q) is 0:
				continue
			
			outputFrame = q.popleft()
			yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
				bytearray(outputFrame) + b'\r\n')
			time.sleep(0.25)

	return Response(produce_frame(), mimetype = "multipart/x-mixed-replace; boundary=frame")
			
				
@app.route("/video_stream", methods=['POST'])
def video_stream():
	list = request.json['instances']
	for l in list:
		a = np.asarray(l, dtype=np.uint32)
		b = Image.fromarray(a.astype('uint8')) 
		c = np.asarray(b)
		(flag, image) = cv2.imencode(".JPEG", c)
		q.append(image)
	return 'OK'
	
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, debug=True, threaded=True, use_reloader=False)
