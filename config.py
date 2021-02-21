import configparser


def load_config(path_to_config):
    config = configparser.ConfigParser()
    config.read(path_to_config)
    return config


def write_config(path_to_config):
    config = configparser.ConfigParser()
    config['CARD_PROPERTIES'] = {}
    config['CARD_PROPERTIES']['card_width'] = '532'
    config['CARD_PROPERTIES']['card_height'] = '744'
    config['PAPER_SHEET_PROPERTIES'] = {}
    config['PAPER_SHEET_PROPERTIES']['gap_size'] = '2'
    config['PAPER_SHEET_PROPERTIES']['cards_in_row'] = '3'
    config['PAPER_SHEET_PROPERTIES']['cards_on_page'] = '9'
    with open(path_to_config, 'w') as configfile:
        config.write(configfile)


class CardsConfig:
    card_width: int
    card_height: int
    gap_between_cards: int
    cards_in_row: int
    cards_in_column: int

    def __init__(self, path_to_config):
        config = load_config(path_to_config)
        self.card_width = config['CARD_PROPERTIES']['card_width']
        self.card_height = config['CARD_PROPERTIES']['card_height']
        self.gap_size = config['PAPER_SHEET_PROPERTIES']['gap_size']
        self.cards_in_row = config['PAPER_SHEET_PROPERTIES']['cards_in_row']
        self.cards_on_page = config['PAPER_SHEET_PROPERTIES']['cards_on_page']
