import json

def load_directory(file_path):
    with open(file_path, "r") as file:
        directory_struct = json.load(file)
    return directory_struct
