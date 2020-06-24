# Files needed to provision tensor flow app

To conplete video streaming and analytics three containers are used. 

1. A `Tensorflow Serving` container which accepts war batches of video frames in bitstring format and returns dictionaries of usful detections 

2. An `Inference` container which handles video parsing, sending of frames to th tensorflow serving module, and drawing of results onto frames. It then can store the inferenced frames in short 3 ish second video frames to ceph object storage for eventual serving back to a user. 

3. A `Serving` pod to spin up a flask based webserver which displays the inferenced video back to the user, via a connection to ceph object stroage 

![TF architecture](https://raw.githubusercontent.com/astoycos/edge-security-demo/master/tensorflow_app/Keylime-Demo-tf-arch.png)