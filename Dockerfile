FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y vlc
RUN apt-get install -y ffmpeg
RUN apt-get install -y git
RUN apt-get install -y python3.8
RUN apt-get install -y python3.8-distutils

RUN rm /usr/bin/python3
RUN ln -s python3.8 /usr/bin/python


ADD https://bootstrap.pypa.io/get-pip.py get-pip.py
RUN python get-pip.py

RUN useradd -m user

ADD *.py .
ADD requirements.txt .
RUN pip install -r requirements.txt


# VLC is not supposed to be run as root. Sorry.
USER user