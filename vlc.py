import argparse
import shutil
from os import listdir
from os.path import isdir, join, splitext
from pathlib import Path

import ffmpeg
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

                # https://github.com/kkroening/ffmpeg-python/blob/master/examples/README.md#examples
                probe = ffmpeg.probe(full_path)
                video_stream = next(
                    (stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
                video_duration = float(video_stream['duration'])

                fps = args.rate
                for s in tqdm(range(int(video_duration))):
                    ffmpeg.input(full_path, ss=s).filter('fps', fps=fps, round='up').output(
                        f'{args.output}/{file_name}_{s:03d}_%3d.jpg', vframes=fps).run(quiet=True)
            except Exception as e:
                print(e)

    print(f'Output file count:{len(list_files(args.output))}')
