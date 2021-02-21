import os
import json

from main import resources_folder


def get_config_path():
    return os.path.join(resources_folder, 'config.json')


def load_config(path_to_config):
    global config
    with open(path_to_config) as opened_file:
        return json.load(opened_file)

