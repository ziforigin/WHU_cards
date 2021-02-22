import logging
import requests
from bs4 import BeautifulSoup

from src.card import Card

card_types = {
    'objective': 1,
    'ploy': 2,
    'upgrade': 3
}


def load_deck_page_to_memory(deck_config) -> BeautifulSoup:
    page = requests.get(deck_config.link)
    soup = BeautifulSoup(page.content, 'html.parser')
    logging.info(f'Opening deck page {deck_config.name}')
    return soup


def get_image_url_from_web_element(data_content_attribute: str) -> str:
    image_uri = data_content_attribute.replace("<img class='img-fluid' src='", "").replace("'>", "")
    return image_uri


def serialize_web_element_to_card_object(web_element: BeautifulSoup, card_type: str) -> Card:
    card_name = web_element['title']
    logging.info(f'Saving {card_name} card to memory')
    image_url = get_image_url_from_web_element(web_element['data-content'])
    return Card(card_name, image_url, card_type)


def parse_and_serialize_all_cards_on_page(soup: BeautifulSoup) -> list:
    cards_list = list()
    cards_blocks_with_headers = soup.find_all(name='div', attrs={'class': 'col-lg'})
    for card_type in card_types:
        cards_block = cards_blocks_with_headers[card_types[card_type]].find(name='div')
        child_elements = cards_block.find_all(name='a', attrs={'class': 'alert-link d-none d-lg-inline'})
        for child in child_elements:
            new_card = serialize_web_element_to_card_object(child, card_type)
            cards_list.append(new_card)
    return cards_list
