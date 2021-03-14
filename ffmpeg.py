import argparse
import json
import shlex
import shutil
import subprocess
from os import listdir
from os.path import isdir, join, splitext
from pathlib import Path

from tqdm import tqdm


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


def run_shell_command(command):
    # https://docs.python.org/3.8/library/subprocess.html
    result = subprocess.run(shlex.split(
        command), capture_output=True)
    if result.stdout:
        output = json.loads(result.stdout)
    else:
        output = ''
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",
                        help="Input file or folder.")
    parser.add_argument("--output",
                        help="Output folder.")
    parser.add_argument("--fps", type=int,
                        help="")
    parser.add_argument("--to-video",
                        help="")

    args = parser.parse_args()

    print(args)
    shutil.rmtree(args.output, ignore_errors=True)
    Path(args.output).mkdir(parents=True, exist_ok=True)

    if args.to_video:
        shutil.rmtree(args.to_video, ignore_errors=True)
        Path(args.to_video).mkdir(parents=True, exist_ok=True)
    for full_path, sub_path, file_name, file_ext in tqdm(list_files(args.input)):
        if file_ext in set(['.avi', '.mp4']):
            print(f'Processing {full_path}')

            command = f'ffprobe -i {full_path} -v quiet -print_format json -show_format -show_streams -hide_banner'
            result = run_shell_command(command)
            print(result)
            video_duration = float(result['streams'][0]['duration'])

            fps = args.fps
            for s in tqdm(range(int(video_duration))):
                for t in range(fps):
                    st = s + t/fps
                    command = f'ffmpeg -ss {st} -i {full_path} -vframes 1 {args.output}/{file_name}_{s:03d}_{t:03d}.jpg'
                    result = run_shell_command(command)

            if args.to_video:
                command = f'ffmpeg -framerate {fps} -pattern_type glob -i "{args.output}/{file_name}_*.jpg" {args.to_video}/{file_name}.mp4'
                result = run_shell_command(command)
    print(f'Output file count:{len(list_files(args.output))}')
