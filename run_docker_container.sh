#!/bin/bash

CONTAINER=rotate-and-crop
docker run -it --rm -v `pwd`/data:/data -v `pwd`/scripts:/scripts -v `pwd`/output:/output $CONTAINER
