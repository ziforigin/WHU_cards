import os
import requests

from folder_factory import create_all_dirs_along_file_path
from objects.card import Card


def save_card_image(card: Card, output_folder):
    card_full_path = os.path.join(output_folder, card.image_url)
    card_download_url = "https://www.underworldsdb.com/" + card.image_url
    if not os.path.exists(card_full_path):
        print("downloading card %s..." % card.name)
        create_all_dirs_along_file_path(card_full_path)
        image = requests.get(card_download_url)
        with open(card_full_path, 'wb') as file:
            file.write(image.content)


def save_all_cards_images_for_deck(deck_obj, file_paths):
    set_of_cards = set()
    for card in deck_obj.cards:
        if card.name in set_of_cards:
            continue
        else:
            save_card_image(card, file_paths.output_folder)
            set_of_cards.add(card.name)
