import argparse
import math
import shutil
from pathlib import Path

from tqdm import tqdm

from common import list_files, run_shell_command


def get_video_info(full_path):
    command = f'ffprobe -i {full_path} -v quiet -print_format json -show_format -show_streams -hide_banner'
    result = run_shell_command(command)
    video_streams = [s for s in result['streams']
                     if s['codec_type'] == 'video']
    video_stream = video_streams[0]
    video_duration = float(video_stream['duration'])
    video_frames = int(video_stream['nb_frames'])
    video_fps = video_frames / video_duration
    return video_duration, video_fps


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
    parser.add_argument("--tool", default="vlc",
                        help="")

    args = parser.parse_args()

    shutil.rmtree(args.output, ignore_errors=True)
    Path(args.output).mkdir(parents=True, exist_ok=True)

    sample_fps = args.fps
    if args.to_video:
        shutil.rmtree(args.to_video, ignore_errors=True)
        Path(args.to_video).mkdir(parents=True, exist_ok=True)
    for full_path, sub_path, file_name, file_ext in tqdm(list_files(args.input)):
        if file_ext in set(['.avi', '.mp4']):
            print(f'To images: {full_path}')

            video_duration, video_fps = get_video_info(full_path)

            step = math.ceil(video_fps / sample_fps)
            if args.tool == "ffmpeg":
                for s in tqdm(range(int(video_duration))):
                    for t in range(sample_fps):
                        st = s + t/sample_fps
                        command = f'ffmpeg -ss {st} -i {full_path} -qmin 1 -q:v 1 -vframes 1 {args.output}/{file_name}_{st:08.2f}.jpg'
                        result = run_shell_command(command)
            elif args.tool == "vlc":
                command = f"vlc {full_path} --intf=dummy --rate=5 --video-filter=scene --vout=dummy --scene-format=jpg \
                    --scene-ratio={step} --scene-path={args.output}  --scene-prefix={file_name}_ vlc://quit"
                result = run_shell_command(command)

    print(f'Output file count:{len(list_files(args.output))}')
    if args.to_video:
        for full_path, sub_path, file_name, file_ext in tqdm(list_files(args.input)):
            if file_ext in set(['.avi', '.mp4']):
                print(f'To video: {full_path}')
                command = f'ffmpeg -framerate {sample_fps} -pattern_type glob -i "{args.output}/{file_name}_*.jpg" {args.to_video}/{file_name}.mp4'
                result = run_shell_command(command)
