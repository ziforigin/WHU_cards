import logging
import os
import requests

from src.filepaths_dto import FilePaths
from src.folder_utils import create_all_dirs_along_file_path
from src.card import Card


def download_card_image(card: Card) -> requests:
    card_download_url = 'https://www.underworldsdb.com/' + card.image_url
    logging.info(f'Downloading card {card.name}')
    return requests.get(card_download_url)


def create_card_file_path(card: Card, file_paths: FilePaths) -> str:
    return os.path.join(file_paths.output_folder, card.image_url)


def save_card_image(image: requests, card_full_path: str, card: Card):
    try:
        with open(card_full_path, 'wb') as file:
            file.write(image.content)
    except IOError as e:
        logging.error(f'Enable to save card {card.name} to {card_full_path}', exc_info=e)


def save_all_cards_images_for_deck(cards: list, file_paths: FilePaths):
    set_of_cards = set()
    for card in cards:
        if card.name in set_of_cards:
            continue
        else:
            image = download_card_image(card)
            card_full_path = create_card_file_path(card, file_paths)
            create_all_dirs_along_file_path(card_full_path)
            save_card_image(image, card_full_path, card)
            set_of_cards.add(card.name)
