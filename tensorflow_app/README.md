# Cloud Native Video Sreaming and Analytics

To complete video streaming and analytics three containers are used. 

1. A `Tensorflow Serving` container which accepts war batches of video frames in bitstring format and returns dictionaries of useful detections 

    - See Dockerfile in `video-serving` directory for more info 
    - The container is already made in my Quay repo -> (Still need to Upload)

2. An `Inference` container which handles video parsing, sending of frames to the tensorflow serving module, and drawing of results onto frames. It then can store the inferenced frames in short 3 ish second video frames to ceph object storage for eventual serving back to a user. 

    - The `app` directory houses the code for the `Inference` Container
    - `analsis.py` uses FFMPEG to parse Video and send frames to the Tensorflow serving container 
    - Was previously run as a  `Knative` service for automatic scalability, in this instance just run as pod 
    - To learn more about how the inference function(I.E bounding boxes on images) Works read [this link](https://github.com/tensorflow/models/tree/master/research/object_detection)
    - To run Locally see `Dockerfile` for all the required dependencies 
    - TODO: 
        - Containerize the inference APP, see Existing Dockerfile in `app` directory for a good start
        - Setup a BATCH_SIZE variable 
        - Read in the Tensorflow Serving URL, Debug value, and batch size from environment (os.Env etc etc)
        - make `requirements.txt` for easier reproducability a


3. A `Serving` pod to spin up a flask based webserver which displays the inferenced video back to the user, via a connection to ceph object stroage 
    - `update.py` is called to pull segments from ceph and make the HLS playlist file(`.m3u8`) for serving to user via a Flask app which is started by  `serving.py`
    - TODO: 
        - This needs to be updated depending on how we stream the video from the agent pods to the central video server (i.e probably remove Ceph)
        - Most likely either "Stream" video with a kafka queue setup, I.E A topic for each agent that the central video server digests 

Existing Arch reference 
![TF architecture](https://raw.githubusercontent.com/astoycos/edge-security-demo/master/tensorflow_app/Keylime-Demo-tf-arch.png)
