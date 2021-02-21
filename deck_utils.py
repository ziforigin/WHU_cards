import json
import os

from json_serializer import JsonEncoder
from objects.card import Deck


def save_deck_as_json(deck_name, decks_folder, deck_obj):
    file_name = deck_name + '.json'
    file_path = os.path.join(decks_folder, file_name)
    with open(file_path, 'w') as json_file:
        json.dump(deck_obj, json_file, cls=JsonEncoder, indent=4)


def get_all_decks_urls_from_deck_list_file(resources_folder):
    with open(os.path.join(resources_folder, 'decks_list.json')) as opened_file:
        chosen_decks = json.load(opened_file)
        return chosen_decks


def load_deck(deck_name: str, decks_folder: str) -> Deck:
    deck_name += '.json'
    file = os.path.join(decks_folder, deck_name)
    with open(file, 'r') as opened_file:
        deck_obj = Deck.decode_from_json(deck_name, json.load(opened_file))
    return deck_obj
