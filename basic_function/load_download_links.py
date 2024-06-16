import os
from constants import DOWNLOAD_FOLDER_PATH


def load_download_links(identifier):
    metadata_folder = os.path.join(DOWNLOAD_FOLDER_PATH,identifier,"metadata")
    download_links = []
    with open(f'{metadata_folder}/download_links.txt','r') as f:
        for line in f:
            download_links.append(line.strip())
    return download_links