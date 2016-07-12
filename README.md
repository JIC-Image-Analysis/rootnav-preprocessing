# RootNav preprocessing

## Introduction

The script in this project has been created to rotate and crop an image from
a camera to make it suitable for processing using
[RootNav](https://www.cpib.ac.uk/tools-resources/software/rootnav/).

This image analysis project has been setup to take advantage of a technology
known as Docker.

This means that you will need to:

1. Download and install the [Docker Toolbox](https://www.docker.com/products/docker-toolbox)
2. Build a docker image

before you can run the image analysis in a docker container.


## Build a Docker image

Before you can run your analysis you need to build your docker image.  Once you
have built the docker image you should not need to do this step again.

A docker image is basically a binary blob that contains all the dependencies
required for the analysis scripts. In other words the docker image has got no
relation to the types of images that we want to analyse, it is simply a
technology that we use to make it easier to run the analysis scripts.

```
$ cd docker
$ bash build_docker_image.sh
$ cd ..
```

## Preparing data and output directories

This work flow depends on input files being located in a directory called
``data`` and the resulting files being written to a directory named ``output``.

Let's create these directories.

```
$ mkdir data
$ mkdir output
```

Now copy the files you want to analyse into the data directory.

## Run the image analysis in a Docker container

The image analysis will be run in a Docker container.  The script
``run_docker_container.sh`` will drop you into an interactive Docker session.

```
$ bash run_docker_container.sh
[root@048bd4bd961c /]#
```

Now you can run the image analysis.

```
[root@048bd4bd961c /]# python scripts/analysis.py data/ output/
```
