import os

import config
from card_utils import save_all_cards_images_of_all_decks
from config import get_config_path
from config import load_config
from deck_utils import save_deck_as_json, get_all_decks_urls_from_deck_list_file
from folder_factory import create_output_folder, create_folders
from image_utils import merge_to_print_all_decks, generate_backs_of_cards
from objects import card
from pages.deck_content_page import Deck_content_page

deck_content_page_url = "https://www.underworldsdb.com/"

output_folder = os.path.join(os.path.dirname(__file__), './output')
decks_folder = os.path.join(output_folder, 'decks')
resources_folder = os.path.join(os.path.dirname(__file__), './resources')
cards_folder = os.path.join(output_folder, 'cards')
for_printing_folder = os.path.join(output_folder, 'upgrades_3x3')


class Tests:
    config = None
    load_config(get_config_path)

    def test_download_all_cards_from_json(self, browser):
        load_config()
        create_output_folder()
        create_folders(output_folder, [decks_folder, cards_folder, for_printing_folder])

        for deck in get_all_decks_urls_from_deck_list_file():
            deck_content_page = Deck_content_page(browser)
            deck_content_page.open_deck_page(deck)
            cards_dict = deck_content_page.gather_all_cards_of_a_deck_by_card_type()
            deck_obj = card.Deck(deck, cards_dict)
            save_deck_as_json(deck, deck_obj)
        save_all_cards_images_of_all_decks()

        merge_to_print_all_decks(int(config['card_width']), int(config['card_height']), int(config['gap_size']),
                                      int(config['cards_in_row']), int(config['cards_on_page']))
        generate_backs_of_cards("objective-back.png", int(config['card_width']), int(config['card_height']),
                                     int(config['gap_size']),
                                     int(config['cards_in_row']), int(config['cards_on_page']))
        generate_backs_of_cards("power-back.png", int(config['card_width']), int(config['card_height']),
                                     int(config['gap_size']),
                                     int(config['cards_in_row']), int(config['cards_on_page']))
