import errno
import logging
import os


def create_output_folder(output_folder):
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
        logging.info(f'Creating folder {output_folder}')


def create_folders(directory_path, folders_list):
    for folder in folders_list:
        if not os.path.exists(os.path.join(directory_path, folder)):
            os.mkdir(os.path.join(directory_path, folder))
            logging.info(f'Creating folders {folder}')


def create_all_dirs_along_file_path(file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
            logging.info(f'Creating folder along the path {file_path}')
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
