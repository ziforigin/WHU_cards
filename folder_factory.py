import errno
import os

from main import output_folder


def create_output_folder():
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)


def create_folders(directory_path, folders_list):
    for folder in folders_list:
        if not os.path.exists(os.path.join(directory_path, folder)):
            os.mkdir(os.path.join(directory_path, folder))


def create_all_dirs_along_filepath(filepath):
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
