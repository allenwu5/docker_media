import json
import shlex
import subprocess
from os import listdir
from os.path import isdir, join, splitext


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


def run_shell_command(command, capture_output=True):
    # https://docs.python.org/3.8/library/subprocess.html
    result = subprocess.run(shlex.split(
        command), check=True, capture_output=capture_output)
    if result.stdout:
        output = json.loads(result.stdout)
    else:
        output = ''
    return output
