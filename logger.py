import logging
import sys

from filepaths_dto import FilePaths


def configure_logger(file_path: FilePaths):
    logging.basicConfig(filename=file_path.log_path, filemode='w', level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
