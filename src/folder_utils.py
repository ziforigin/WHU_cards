import logging
import os


def create_folder(folder: str):
    if not os.path.exists(folder):
        logging.info(f'Creating folder {folder}')
        try:
            os.mkdir(folder)
        except IOError as e:
            logging.error(f'Unable to create folder {folder}', exc_info=e)


def create_all_dirs_along_file_path(file_path):
    if not os.path.exists(file_path):
        logging.info(f'Creating folder along the path {file_path}')
        try:
            os.makedirs(os.path.dirname(file_path))
        except IOError as e:
            logging.error(f'Unable to create folders along the path {file_path}', exc_info=e)
