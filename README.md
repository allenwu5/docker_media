# docker_media
* Process video, image, audio files

# Usage
## Convert video to images.
```
docker run --rm -it -v ~/work/data/:/mnt arashilen/ubuntu-media python ffmpeg.py --input=/mnt/video --output=/mnt/image --fps=5
```
## Convert video to images, then convert images to new video.
```
docker run --rm -it -v ~/work/data/:/mnt arashilen/ubuntu-media python ffmpeg.py --input=/mnt/video --output=/mnt/image --fps=5 --to-video=/mnt/new_video 
```
