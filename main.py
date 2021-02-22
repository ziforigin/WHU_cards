from src.card_image_utils import save_all_cards_images_for_deck
from src.folder_utils import create_output_folders, create_deck_folder
from src.card_sheet_utils import prepare_cards_for_printing
from src.page_crawler import parse_all_cards_in_deck
from src import config, logger, filepaths_dto


file_paths = filepaths_dto.FilePaths()
logger.configure_logger(file_paths)
create_output_folders(file_paths)
decks = config.load_decks(file_paths.config_path)
for deck_config in decks:
    cards = parse_all_cards_in_deck(deck_config)
    save_all_cards_images_for_deck(cards, file_paths)
    create_deck_folder(file_paths, deck_config)
    prepare_cards_for_printing(cards, deck_config, file_paths)



