import logging
import requests
from bs4 import BeautifulSoup

from src.card import Card

card_types = {
    'objective': 1,
    'ploy': 2,
    'upgrade': 3
}

def open_deck_page(deck_config):
    page = requests.get(deck_config.link)
    soup = BeautifulSoup(page.content, 'html.parser')
    logging.info(f'Opening deck page {deck_config.name}')
    return soup


def image_src_url_from_data_content(data_content_attribute: str):
    image_uri = data_content_attribute.replace("<img class='img-fluid' src='", "").replace("'>", "")
    return image_uri


def gather_all_cards_of_a_deck_by_card_type(soup: BeautifulSoup):
    cards_list = list()
    cards_blocks_with_headers = soup.find_all(name='div', attrs={'class': 'col-lg'})
    for card_type in card_types:
        cards_block = cards_blocks_with_headers[card_types[card_type]].find(name='div')
        child_elements = cards_block.find_all(name='a', attrs={'class': 'alert-link d-none d-lg-inline'})
        for child in child_elements:
            card_name = child['title']
            logging.info(f'Saving {card_name} card to memory')
            image_url = image_src_url_from_data_content(child['data-content'])
            new_card = Card(card_name, image_url, card_type)
            cards_list.append(new_card)
    return cards_list
