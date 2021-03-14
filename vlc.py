import argparse
import shlex
import subprocess
from os import listdir
from os.path import isdir, join, splitext

from tqdm import tqdm
import shutil
from pathlib import Path
import ffmpeg


def list_files(dir_path, sub_path=None):
    files = []
    for file_name in sorted(listdir(dir_path)):
        full_path = join(dir_path, file_name)
        if isdir(full_path):
            new_sub_path = join(
                sub_path, file_name) if sub_path else file_name
            files += list_files(full_path, new_sub_path)
        else:
            file_name, file_ext = splitext(file_name)
            files.append((full_path, sub_path, file_name, file_ext))
    return files


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",
                        help="Input file or folder.")
    parser.add_argument("--output",
                        help="Output folder.")
    parser.add_argument("--rate", type=float,
                        help="")

    args = parser.parse_args()

    print(args)
    shutil.rmtree(args.output, ignore_errors=True)
    Path(args.output).mkdir(parents=True, exist_ok=True)

    for full_path, sub_path, file_name, file_ext in tqdm(list_files(args.input)):
        if file_ext in set(['.avi', '.mp4']):
            try:
                print(f'Processing {full_path}')
                # command = f'vlc {full_path} --intf=dummy --vout=vdummy --video-filter=scene --scene-format=jpg \
                #      --fps-fps=5 --rate={args.rate} --scene-ratio=1 --scene-prefix={file_name}_ --scene-path={args.output} --codec avcodec,none vlc://quit'
                # command = f'ffmpeg -i {full_path} -vf fps={args.rate} {args.output}/{file_name}_%8d.jpg'

                # command = f'ffprobe -v error -select_streams v:0 -show_entries stream=nb_frames -of default=nokey=1:noprint_wrappers=1 {full_path}'
                # status = subprocess.run(shlex.split(
                #         command), check=True, capture_output=True)
                # print(status)

    # https://github.com/kkroening/ffmpeg-python/blob/master/examples/README.md#examples
                probe = ffmpeg.probe(full_path)
                video_stream = next(
                    (stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
                video_duration = float(video_stream['duration'])
                # print(video_stream)
                # continue

                for s in tqdm(range(int(video_duration*args.rate))):
                    t = s/args.rate
                    ffmpeg.input(full_path, ss=t).filter('fps', fps=5, round='up').output(
                        f'{args.output}/{file_name}_{t}_%3d.jpg', vframes=5).run(quiet=True)
            except Exception as e:
                print(e)

    print(f'Output file count:{len(list_files(args.output))}')
