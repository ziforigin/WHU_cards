import os

import selenium

import config
import filepaths_dto
from card_utils import save_all_cards_images_of_all_decks
from deck_utils import save_deck_as_json, get_all_decks_urls_from_deck_list_file
from folder_factory import create_output_folder, create_folders
from image_utils import merge_to_print_all_decks, generate_backs_of_cards
from objects import card
from pages.deck_content_page import Deck_content_page

deck_content_page_url = "https://www.underworldsdb.com/"

def test_download_all_cards_from_json():
    file_paths = filepaths_dto.FilePaths()
    path_to_config = os.path.join(file_paths.resources_folder, 'config.cfg')
    cards_config = config.CardsConfig(path_to_config)
    create_output_folder(file_paths.output_folder)
    create_folders(file_paths.output_folder, [file_paths.decks_folder, file_paths.cards_folder, file_paths.for_printing_folder])
    for deck in get_all_decks_urls_from_deck_list_file(file_paths.resources_folder):
        deck_content_page = Deck_content_page(browser)
        deck_content_page.open_deck_page(deck)
        cards_dict = deck_content_page.gather_all_cards_of_a_deck_by_card_type()
        deck_obj = card.Deck(deck, cards_dict)
        save_deck_as_json(deck, file_paths.decks_folder, deck_obj)
    save_all_cards_images_of_all_decks(file_paths)

    merge_to_print_all_decks(cards_config, file_paths)
    generate_backs_of_cards("objective-back.png", cards_config, file_paths)
    generate_backs_of_cards("power-back.png", cards_config, file_paths)


print("\nstart browser for test..")
browser = selenium.webdriver.chrome.webdriver.WebDriver(executable_path=r"chromedriver.exe")
try:
    test_download_all_cards_from_json()
finally:
    print("\nquit browser..")
    browser.quit()


