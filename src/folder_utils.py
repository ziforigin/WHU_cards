import logging
import os

from src.config import DeckConfig
from src.filepaths_dto import FilePaths


def create_output_folders(file_paths: FilePaths):
    create_folder(file_paths.output_folder)
    create_folder(file_paths.cards_folder)
    create_folder(file_paths.for_printing_folder)


def create_deck_folder(file_paths: FilePaths, config: DeckConfig):
    deck_folder = generate_deck_folder_path(file_paths, config)
    create_folder(deck_folder)


def generate_deck_folder_path(file_paths: FilePaths, config: DeckConfig) -> str:
    return os.path.join(file_paths.for_printing_folder, config.name)


def create_folder(folder: str):
    if not os.path.exists(folder):
        logging.info(f'Creating folder {folder}')
        try:
            os.mkdir(folder)
        except IOError as e:
            logging.error(f'Unable to create folder {folder}', exc_info=e)


def remove_file_name_from_path(file_path):
    file_name = os.path.basename(file_path)
    return file_path.replace(file_name, '')


def create_all_dirs_along_file_path(file_path):
    folder_path = remove_file_name_from_path(file_path)
    if not os.path.exists(folder_path):
        logging.info(f'Creating folder along the path {folder_path}')
        try:
            os.makedirs(os.path.dirname(file_path))
        except IOError as e:
            logging.error(f'Unable to create folders along the path {folder_path}', exc_info=e)
