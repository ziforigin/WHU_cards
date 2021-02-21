import os

import config
from card_utils import save_all_cards_images_of_all_decks
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

    def test_download_all_cards_from_json(self, browser):
        path_to_config = os.path.join(resources_folder, 'config.cfg')
        cards_config = config.CardsConfig(path_to_config)
        create_output_folder(output_folder)
        create_folders(output_folder, [decks_folder, cards_folder, for_printing_folder])
        for deck in get_all_decks_urls_from_deck_list_file(resources_folder):
            deck_content_page = Deck_content_page(browser)
            deck_content_page.open_deck_page(deck)
            cards_dict = deck_content_page.gather_all_cards_of_a_deck_by_card_type()
            deck_obj = card.Deck(deck, cards_dict)
            save_deck_as_json(deck, decks_folder, deck_obj)
        save_all_cards_images_of_all_decks()

        merge_to_print_all_decks(cards_config)
        generate_backs_of_cards("objective-back.png", cards_config)
        generate_backs_of_cards("power-back.png", cards_config)


