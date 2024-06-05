import json
import os

from constants import DOWNLOAD_FOLDER_PATH

def load_filetree(identifier):
    """Loads the filetree.json file for the given identifier."""
    filetree_path = os.path.join(DOWNLOAD_FOLDER_PATH, identifier, "metadata",f"{identifier}_filetree.json") # Path to the filetree.json file
    with open(filetree_path, 'r') as filetree:
        return json.load(filetree)