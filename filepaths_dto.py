import os


class FilePaths:
    output_folder: str
    decks_folder: str
    resources_folder: str
    cards_folder: str
    for_printing_folder: str

    def __init__(self):
        file_path = os.path.dirname(__file__)
        self.output_folder = os.path.join(file_path, './output')
        self.decks_folder = os.path.join(self.output_folder, 'decks')
        self.resources_folder = os.path.join(file_path, './resources')
        self.cards_folder = os.path.join(self.output_folder, 'cards')
        self.for_printing_folder = os.path.join(self.output_folder, 'for_printing')
