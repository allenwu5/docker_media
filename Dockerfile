FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y vlc
RUN apt-get install -y ffmpeg
RUN apt-get install -y python3
RUN apt-get install -y git

RUN useradd -m user

# VLC is not supposed to be run as root. Sorry.
USER user