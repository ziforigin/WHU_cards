import os


class FilePaths:
    output_folder: str
    resources_folder: str
    cards_folder: str
    for_printing_folder: str
    config_path: str
    objective_card_back: str
    power_card_back: str

    def __init__(self):
        file_path = os.path.dirname(__file__)
        self.output_folder = os.path.join(file_path, './output')
        self.resources_folder = os.path.join(file_path, './resources')
        self.cards_folder = os.path.join(self.output_folder, 'cards')
        self.for_printing_folder = os.path.join(self.output_folder, 'for_printing')
        self.config_path = os.path.join(self.resources_folder, 'config.cfg')
        self.objective_card_back = os.path.join(self.resources_folder, 'objective-back.png')
        self.power_card_back = os.path.join(self.resources_folder, 'power-back.png')
