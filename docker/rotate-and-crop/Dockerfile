FROM ubuntu:latest

RUN apt-get update && apt-get install -y python-scipy python-matplotlib python-pip libfreeimage-dev zbar-tools
RUN pip install --upgrade pip && pip install "scikit-image<0.12"
COPY requirements.txt .
RUN pip install -r requirements.txt
