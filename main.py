import selenium

import config
import filepaths_dto
from card_utils import save_all_cards_images_for_deck
from folder_factory import create_output_folder, create_folders
from image_utils import merge_to_print_deck, generate_objective_cards_back, generate_power_cards_back
from objects import card
from pages.deck_content_page import DeckContentPage

deck_content_page_url = "https://www.underworldsdb.com/"


def download_all_cards():
    file_paths = filepaths_dto.FilePaths()
    create_output_folder(file_paths.output_folder)
    create_folders(file_paths.output_folder, [file_paths.cards_folder, file_paths.for_printing_folder])
    decks = config.load_decks(file_paths.config_path)
    for deck_config in decks:
        deck_content_page = DeckContentPage(browser)
        deck_content_page.open_deck_page(deck_config)
        cards_dict = deck_content_page.gather_all_cards_of_a_deck_by_card_type()
        deck_obj = card.Deck(deck_config.name, cards_dict)
        save_all_cards_images_for_deck(deck_obj, file_paths)
        merge_to_print_deck(deck_obj, deck_config, file_paths)
        generate_objective_cards_back(deck_config, file_paths)
        generate_power_cards_back(deck_config, file_paths)


print("\nstart browser for test..")
browser = selenium.webdriver.chrome.webdriver.WebDriver(executable_path=r"chromedriver.exe")
try:
    download_all_cards()
finally:
    print("\nquit browser..")
    browser.quit()


