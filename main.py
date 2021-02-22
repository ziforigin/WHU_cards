from src.card_image_utils import save_all_cards_images_for_deck
from src.folder_utils import create_folder
from src.card_sheet_utils import prepare_cards_for_printing, generate_deck_folder_path
from src import page_crawler, config, logger, filepaths_dto


file_paths = filepaths_dto.FilePaths()
logger.configure_logger(file_paths)
create_folder(file_paths.output_folder)
create_folder(file_paths.cards_folder)
create_folder(file_paths.for_printing_folder)
decks = config.load_decks(file_paths.config_path)
for deck_config in decks:
    page = page_crawler.load_deck_page_to_memory(deck_config)
    cards = page_crawler.parse_and_serialize_all_cards_on_page(page)
    save_all_cards_images_for_deck(cards, file_paths)
    deck_folder = generate_deck_folder_path(file_paths, deck_config)
    create_folder(deck_folder)
    prepare_cards_for_printing(cards, deck_config, file_paths)



