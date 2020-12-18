import json
import os
from selenium.webdriver.common.by import By
from objects.card import Card

output_folder = os.path.join(os.path.dirname(__file__), './../output')
decks_folder = os.path.join(output_folder, 'decks')
resources_folder = os.path.join(os.path.dirname(__file__), './../resources')
cards_folder = os.path.join(output_folder, 'cards')
for_printing_folder = os.path.join(output_folder, 'beastgrave_universal_3x3')

class Deck_content_page:

    deck_content_page_url = "https://www.underworldsdb.com/"

    card_types = {
        "objective": "div.col-lg:nth-child(2) > div",
        "ploy": "div.col-lg:nth-child(3) > div",
        "upgrade": "div.col-lg:nth-child(4) > div"
    }

    card_node = (By.CLASS_NAME, "alert-link.d-none.d-lg-inline")

    def __init__(self, browser):
        self.browser = browser

    def get_deck_url_from_deck_list_file(self, deck_name):
        with open(os.path.join(resources_folder, 'decks_list.json')) as opened_file:
            chosen_decks = json.load(opened_file)
            return chosen_decks[deck_name]

    def open_deck_page(self, deck_name):
        self.browser.get(self.get_deck_url_from_deck_list_file(deck_name))


    def get_image_elements(self, web_elements_dict):
        result_dict = dict()
        elements_list = self.browser.find_elements(*self.card_node)
        for element in elements_list:
            if element.get_attribute("data-original-title") in web_elements_dict:
                result_dict[element.get_attribute("data-original-title")] = element
        return result_dict


    def gather_all_cards_of_a_deck_by_card_type(self):
        cards_list = list()
        for card_type in self.card_types:
            web_element = self.browser.find_element_by_css_selector(self.card_types[card_type])
            child_elements = web_element.find_elements_by_xpath(".//a[contains(@class, 'alert-link d-none d-lg-inline')]")
            for child in child_elements:
                card_name = child.get_attribute("data-original-title")
                image_url = self.image_src_url_from_data_content(child.get_attribute("data-content"))
                #If I'll need at some point to write restricted\banned\free card attribute:
                # try:
                #     child_siblings = child.find_element_by_xpath("./following-sibling::span/*[@title=\"Restricted\"]")
                #     restricted = True
                # except Exception:
                #     restricted = False
                new_card = Card(card_name, image_url, card_type)
                cards_list.append(new_card)
        return cards_list

    def image_src_url_from_data_content(self, data_content_atribute: str):
        image_uri = data_content_atribute.replace("<img class='img-fluid' src='", "").replace("'>", "")
        return image_uri
