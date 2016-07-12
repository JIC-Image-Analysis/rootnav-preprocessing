!#/bin/bash

IMAGE_NAME=rotate-and-crop

cp ../requirements.txt $IMAGE_NAME
cd $IMAGE_NAME
docker build --no-cache -t $IMAGE_NAME .
rm requirements.txt
cd ../
