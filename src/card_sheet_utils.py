import logging
import os

from PIL import Image

from src.config import DeckConfig
from src.filepaths_dto import FilePaths


def prepare_cards_for_printing(cards: list, deck_config: DeckConfig, file_paths: FilePaths):
    objective_cards_list = separate_objective_cards(cards, file_paths)
    power_cards_list = separate_power_cards(cards, file_paths)
    obj_card_name = generate_objective_cards_name(deck_config)
    power_card_name = generate_power_cards_name(deck_config)
    divide_cards_to_sheets_and_save(obj_card_name, objective_cards_list, deck_config, file_paths)
    divide_cards_to_sheets_and_save(power_card_name, power_cards_list, deck_config, file_paths)
    generate_and_save_objective_cards_back(deck_config, file_paths)
    generate_and_save_power_cards_back(deck_config, file_paths)


def divide_list_to_chunks(file_list: list, length: int) -> list:
    for i in range(0, len(file_list), length):
        yield file_list[i:i + length]


def separate_objective_cards(cards: list, file_paths: FilePaths) -> list:
    logging.info(f'Separating objective cards')
    objective_cards = []
    for card in cards:
        if card.card_type == 'objective':
            objective_cards.append(os.path.join(file_paths.output_folder, card.image_url))
    return objective_cards


def separate_power_cards(cards: list, file_paths: FilePaths) -> list:
    logging.info(f'Separating objective cards')
    power_cards = []
    for card in cards:
        if card.card_type != 'objective':
            power_cards.append(os.path.join(file_paths.output_folder, card.image_url))
    return power_cards


def generate_objective_cards_name(config: DeckConfig) -> str:
    return config.name + '_object_'


def generate_power_cards_name(config: DeckConfig) -> str:
    return config.name + '_power_'


def calculate_canvas_size(config: DeckConfig) -> tuple:
    canvas_height = int(config.card_height * config.cards_in_column + config.gap_size * 2)
    canvas_width = int(config.card_width * config.cards_in_row + config.gap_size * 2)
    canvas_size = tuple([canvas_width, canvas_height])
    return canvas_size


def divide_cards_to_sheets_and_save(name: str, images_list: list, config: DeckConfig, file_paths: FilePaths, color=(255, 255, 255)):
    y_offset = 0
    chunk_counter = 0
    canvas_size = calculate_canvas_size(config)
    images = list(divide_list_to_chunks(images_list, config.cards_in_column * config.cards_in_row))
    card_size: tuple = tuple([config.card_width, config.card_height])
    for big_chunk in images:
        new_image = Image.new('RGBA', canvas_size, color)
        cards_row = list(divide_list_to_chunks(big_chunk, config.cards_in_row))
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


def generate_and_save_objective_cards_back(config: DeckConfig, file_paths: FilePaths):
    color = (158, 129, 97)
    file_name = f"{config.name}_objective_backs.png"
    generate_and_save_cards_back(config, file_paths, color, file_name)


def generate_and_save_power_cards_back(config: DeckConfig, file_paths: FilePaths):
    color = (65, 73, 90)
    file_name = f"{config.name}_power_backs.png"
    generate_and_save_cards_back(config, file_paths, color, file_name)


def generate_and_save_cards_back(config: DeckConfig, file_paths: FilePaths, color: tuple, file_name: str):
    images = []
    counter = 0
    back_file_path = file_paths.objective_card_back
    while counter < (config.cards_in_column * config.cards_in_row):
        images.append(back_file_path)
        counter += 1
    logging.info(f'Generating card backs {file_name}')
    divide_cards_to_sheets_and_save(file_name, images, config, file_paths, color)


