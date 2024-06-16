import os
from constants import DOWNLOAD_FOLDER_PATH


def load_download_links(identifier):
    metadata_folder = os.path.join(DOWNLOAD_FOLDER_PATH,identifier,"metadata")
    download_links = []
    with open(f'{metadata_folder}/download_links.txt','r') as f:
        download_links = f.read().split("\n")
    return download_links