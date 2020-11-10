import errno
import json
import os
import uuid
import requests
from PIL import Image
from fixtures import browser
from objects.card import Card, Deck
from pages.deck_content_page import Deck_content_page
from pages import deck_content_page
from objects import card
from utils.json_serializer import JsonEncoder

deck_content_page_url = "https://www.underworldsdb.com/"

output_folder = os.path.join(os.path.dirname(__file__), './output')
decks_folder = os.path.join(output_folder, 'decks')
resources_folder = os.path.join(os.path.dirname(__file__), './resources')
cards_folder = os.path.join(output_folder, 'cards')
for_printing_folder = os.path.join(output_folder, 'for_printing')

class Tests:

    config = None

    def load_config(self):
        global config
        with open(os.path.join(resources_folder, 'config.json')) as opened_file:
            config = json.load(opened_file)

    def save_deck_as_json(self, deck_name, deck_obj):
        file_name = deck_name + '.json'
        file_path = os.path.join(decks_folder, file_name)
        with open(file_path, 'w') as json_file:
            json.dump(deck_obj, json_file, cls=JsonEncoder, indent=4)

    def create_folders(self, directory_path, folders_list):
        for folder in folders_list:
            if not os.path.exists(os.path.join(directory_path, folder)):
                os.mkdir(os.path.join(directory_path, folder))

    def create_all_dirs_along_filepath(self, filepath):
        if not os.path.exists(os.path.dirname(filepath)):
            try:
                os.makedirs(os.path.dirname(filepath))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

    def get_all_decks_urls_from_deck_list_file(self):
        with open(os.path.join(resources_folder, 'decks_list.json')) as opened_file:
            chosen_decks = json.load(opened_file)
            return chosen_decks

    def save_card_image(self, card: Card):
        card_full_path = os.path.join(output_folder, card.image_url)
        card_download_url = "https://www.underworldsdb.com/" + card.image_url
        if not os.path.exists(card_full_path):
            print("downloading card %s..." % card.name)
            self.create_all_dirs_along_filepath(card_full_path)
            image = requests.get(card_download_url)
            with open(card_full_path, 'wb') as file:
                file.write(image.content)

    def save_all_cards_images_of_all_decks(self):
        list_of_decks = os.listdir(decks_folder)
        set_of_cards = set()
        for name in list_of_decks:
            short_name = name.replace(".json", "")
            deck_obj = self.load_deck(short_name)
            for card in deck_obj.cards:
                if card.name in set_of_cards:
                    continue
                else:
                    self.save_card_image(card)
                    set_of_cards.add(card.name)

    def load_deck(self, deck_name: str) -> Deck:
        deck_name += '.json'
        file = os.path.join(decks_folder, deck_name)
        with open(file, 'r') as opened_file:
            deck_obj = Deck.decode_from_json(deck_name, json.load(opened_file))
        return deck_obj

    def merge_to_print_all_decks(self, card_width, card_height, gap_size, cards_in_row, cards_on_page):
        objective_cards_list, gambit_cards_list = list(), list()
        decks = os.listdir(decks_folder)
        self.create_all_dirs_along_filepath(for_printing_folder)
        result_deck_name = str()
        for deck_file in decks:
            file_name = deck_file.replace(".json", "")
            deck_obj = self.load_deck(file_name)
            self.merge_all_cards_to_print(deck_obj, objective_cards_list, gambit_cards_list)
            result_deck_name += deck_obj.name[0:3] + '_'
        if len(result_deck_name) > 20:
            result_deck_name = str(uuid.uuid4())
        obj_name, gambit_name = result_deck_name + '_object_', result_deck_name + '_gambit_'
        self.image_combiner(obj_name, objective_cards_list, (card_width, card_height), cards_in_row, cards_on_page, gap_size)
        self.image_combiner(gambit_name, gambit_cards_list, (card_width, card_height), cards_in_row, cards_on_page, gap_size)

    def merge_all_cards_to_print(self, deck_object, objective_cards_list, gambit_cards_list):
        for card in deck_object.cards:
            if card.card_type == 'objective':
                objective_cards_list.append(os.path.join(output_folder, card.image_url))
            else:
                gambit_cards_list.append(os.path.join(output_folder, card.image_url))

    def image_combiner(self, name: str, images: list, card_size: tuple, cards_in_row: int, cards_on_page: int, margin: int, color=(255, 255, 255)):
        y_offset = 0
        canvas_width = card_size[0] * cards_in_row + margin * 2
        canvas_height = card_size[1] * int(cards_on_page/cards_in_row) + margin * 2
        chunk_counter = 0
        images = list(self.chunks(images, 16))
        for big_chunk in images:
            new_image = Image.new('RGBA', (canvas_width, canvas_height), color)
            cards_row = list(self.chunks(big_chunk, 4))
            for i in range(len(cards_row)):
                for j in range(len(cards_row[i])):
                    picture = Image.open(cards_row[i][j], mode="r")
                    if not picture.size == card_size:
                        picture = picture.resize(card_size, Image.ANTIALIAS)
                    x_offset = j * (card_size[0] + margin)
                    new_image.paste(picture, (x_offset, y_offset))
                y_offset = (i + 1) * (card_size[1] + margin)
            y_offset = 0
            chunk_counter += 1
            new_image_name = name + str(chunk_counter) + '.png'
            output_file = os.path.join(for_printing_folder, new_image_name)
            new_image.save(output_file)

    def chunks(self, file_list, length):
        for i in range(0, len(file_list), length):
            yield file_list[i:i + length]

    def generate_backs_of_cards(self, back_file_name, card_width, card_height, gap_size, cards_in_row, cards_on_page):
        back = os.path.join(resources_folder, back_file_name)
        images = []
        counter = 0
        while counter < 16:
            images.append(back)
            counter += 1
        folder_name = back_file_name.split('.')
        folder_name = folder_name[0]
        if "objective" in folder_name:
            color = (158, 129, 97)
        elif "power" in folder_name:
            color = (65, 73, 90)
        self.image_combiner(folder_name, images, (card_width, card_height), cards_in_row, cards_on_page, gap_size, color)


    def test_download_all_cards_from_json(self, browser):
        self.load_config()
        self.create_folders(output_folder, [decks_folder, cards_folder, for_printing_folder])
        for deck in self.get_all_decks_urls_from_deck_list_file():
            deck_content_page = Deck_content_page(browser)
            deck_content_page.open_deck_page(deck)
            cards_dict = deck_content_page.gather_all_cards_of_a_deck_by_card_type()
            deck_obj = card.Deck(deck, cards_dict)
            self.save_deck_as_json(deck, deck_obj)
        self.save_all_cards_images_of_all_decks()
        self.merge_to_print_all_decks(int(config['card_width']), int(config['card_height']), int(config['gap_size']),
                                      int(config['cards_in_row']), int(config['cards_on_page']))
        self.generate_backs_of_cards("objective-back.png", int(config['card_width']), int(config['card_height']), int(config['gap_size']),
                                      int(config['cards_in_row']), int(config['cards_on_page']))
        self.generate_backs_of_cards("power-back.png", int(config['card_width']), int(config['card_height']),
                                     int(config['gap_size']),
                                     int(config['cards_in_row']), int(config['cards_on_page']))

