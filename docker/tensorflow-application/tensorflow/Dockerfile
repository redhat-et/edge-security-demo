FROM tensorflow/serving

# Define metadata
LABEL author="Andrew Stoycos"
LABEL description="Use Tensorflow Serving to deploy a Tensorflow Object Dection API ML model"

# install wget
RUN apt-get update
RUN apt-get install -qy wget

# Create variable. Use it with docker build --build-arg model_url=...
# For this demo I use http://download.tensorflow.org/models/object_detection/ssdlite_mobilenet_v2_coco_2018_05_09.tar.gz
# you can use any model from the tensorflow model ZOO https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md
ARG model_url

# Download model
WORKDIR /models
RUN wget -nv -O model.tar.gz $model_url
RUN tar -xvf model.tar.gz
RUN mkdir -p object-detect/1
RUN find -name saved_model -exec mv {}/saved_model.pb {}/variables object-detect/1/ \;

EXPOSE 8050
ENTRYPOINT ["tensorflow_model_server", "--model_base_path=/models/object-detect"]
CMD ["--rest_api_port=8050","--port=8051"]

#Run with: 
# Docker build -t <container Name> --build-arg model_url=http://download.tensorflow.org/models/object_detection/ssdlite_mobilenet_v2_coco_2018_05_09.tar.gz .