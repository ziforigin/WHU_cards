import configparser


def load_config(path_to_config):
    config = configparser.ConfigParser()
    config.read(path_to_config)
    return config


def load_decks(path_to_config):
    config = load_config(path_to_config)
    decks_list = []
    for deck_name in config.sections():
        decks_list.append(DeckConfig(path_to_config, deck_name))
    return decks_list


class DeckConfig:
    name: str
    link: str
    card_width: int
    card_height: int
    gap_between_cards: int
    cards_in_row: int
    cards_in_column: int

    def __init__(self, path_to_config, deck_name):
        config = load_config(path_to_config)
        self.name = deck_name
        self.link = config[deck_name]['link']
        self.card_width = int(config[deck_name]['card_width'])
        self.card_height = int(config[deck_name]['card_height'])
        self.gap_size = int(config[deck_name]['gap_size'])
        self.cards_in_row = int(config[deck_name]['cards_in_row'])
        self.cards_on_page = int(config[deck_name]['cards_on_page'])
