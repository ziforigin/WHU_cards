import os
import uuid

from PIL import Image

from config import CardsConfig
from deck_utils import load_deck
from folder_factory import create_all_dirs_along_file_path


def chunks(file_list, length):
    for i in range(0, len(file_list), length):
        yield file_list[i:i + length]

def merge_to_print_all_decks(config: CardsConfig):
    objective_cards_list, gambit_cards_list = list(), list()
    decks = os.listdir(decks_folder)
    create_all_dirs_along_file_path(for_printing_folder)
    result_deck_name = str()
    for deck_file in decks:
        file_name = deck_file.replace(".json", "")
        deck_obj = load_deck(file_name)
        merge_all_cards_to_print(deck_obj, objective_cards_list, gambit_cards_list)
        result_deck_name += deck_obj.name[0:3] + '_'
    if len(result_deck_name) > 20:
        result_deck_name = str(uuid.uuid4())
    obj_name, gambit_name = result_deck_name + '_object_', result_deck_name + '_gambit_'
    image_combiner(obj_name, objective_cards_list, config)
    image_combiner(gambit_name, gambit_cards_list, config)


def merge_all_cards_to_print(deck_object, objective_cards_list, gambit_cards_list):
    for card in deck_object.cards:
        if card.card_type == 'objective':
            objective_cards_list.append(os.path.join(output_folder, card.image_url))
        else:
            gambit_cards_list.append(os.path.join(output_folder, card.image_url))


def image_combiner(name: str, images_list, config: CardsConfig, color=(255, 255, 255)):
    y_offset = 0
    canvas_height = config.card_height * (config.cards_on_page / config.cards_in_row) + config.gap_size * 2
    canvas_width = config.card_width * config.cards_in_row + config.gap_size * 2
    chunk_counter = 0
    images = list(chunks(images_list, config.cards_on_page))
    card_size: tuple = (config.card_width, config.card_height)
    for big_chunk in images:
        new_image = Image.new('RGBA', (canvas_width, canvas_height), color)
        cards_row = list(chunks(big_chunk, config.cards_in_row))
        for i in range(len(cards_row)):
            for j in range(len(cards_row[i])):
                picture = Image.open(cards_row[i][j], mode="r")
                if not picture.size == card_size:
                    picture = picture.resize(card_size, Image.ANTIALIAS)
                x_offset = j * (card_size[0] + config.gap_size)
                new_image.paste(picture, (x_offset, y_offset))
            y_offset = (i + 1) * (card_size[1] + config.gap_size)
        y_offset = 0
        chunk_counter += 1
        new_image_name = name + str(chunk_counter) + '.png'
        output_file = os.path.join(for_printing_folder, new_image_name)
        new_image.save(output_file)


def generate_backs_of_cards(back_file_name, config: CardsConfig):
    back = os.path.join(resources_folder, back_file_name)
    images = []
    counter = 0
    while counter < config.cards_on_page:
        images.append(back)
        counter += 1
    folder_name = back_file_name.split('.')
    folder_name = folder_name[0]
    if "objective" in folder_name:
        color = (158, 129, 97)
    elif "power" in folder_name:
        color = (65, 73, 90)
    image_combiner(folder_name, images, config, color)
