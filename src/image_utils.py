import logging
import os

from PIL import Image

from src.config import DeckConfig
from src.filepaths_dto import FilePaths
from src.folder_factory import create_folders
from src.card import Deck


def chunks(file_list, length):
    for i in range(0, len(file_list), length):
        yield file_list[i:i + length]


def merge_to_print_deck(deck_obj: Deck, config: DeckConfig, file_paths: FilePaths):
    logging.info(f'Merging cards to sheets for deck {config.name}')
    objective_cards_list, power_cards_list = list(), list()
    output_folder = os.path.join(file_paths.for_printing_folder, config.name)
    create_folders(file_paths.for_printing_folder, [output_folder])
    for card in deck_obj.cards:
        if card.card_type == 'objective':
            objective_cards_list.append(os.path.join(file_paths.output_folder, card.image_url))
        else:
            power_cards_list.append(os.path.join(file_paths.output_folder, card.image_url))
    obj_name, power_name = deck_obj.name + '_object_', deck_obj.name + '_power_'
    image_combiner(obj_name, objective_cards_list, config, file_paths)
    image_combiner(power_name, power_cards_list, config, file_paths)


def image_combiner(name: str, images_list: list, config: DeckConfig, file_paths: FilePaths, color=(255, 255, 255)):
    y_offset = 0
    canvas_height = int(config.card_height * (config.cards_on_page / config.cards_in_row) + config.gap_size * 2)
    canvas_width = int(config.card_width * config.cards_in_row + config.gap_size * 2)
    chunk_counter = 0
    images = list(chunks(images_list, config.cards_on_page))
    canvas_size = tuple([canvas_width, canvas_height])
    card_size: tuple = tuple([config.card_width, config.card_height])
    for big_chunk in images:
        new_image = Image.new('RGBA', canvas_size, color)
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
        output_folder = os.path.join(file_paths.for_printing_folder, config.name)
        output_file = os.path.join(output_folder, new_image_name)
        new_image.save(output_file)


def generate_objective_cards_back(config: DeckConfig, file_paths: FilePaths):
    images = []
    counter = 0
    color = (158, 129, 97)
    back_file_path = file_paths.objective_card_back
    while counter < config.cards_on_page:
        images.append(back_file_path)
        counter += 1
    file_name = f"{config.name}_objective_backs.png"
    logging.info(f'Generating card backs {file_name}')
    image_combiner(file_name, images, config, file_paths, color)


def generate_power_cards_back(config: DeckConfig, file_paths: FilePaths):
    images = []
    counter = 0
    color = (65, 73, 90)
    back_file_path = file_paths.power_card_back
    while counter < config.cards_on_page:
        images.append(back_file_path)
        counter += 1
    file_name = f"{config.name}_power_backs.png"
    logging.info(f'Generating card backs {file_name}')
    image_combiner(file_name, images, config, file_paths, color)


