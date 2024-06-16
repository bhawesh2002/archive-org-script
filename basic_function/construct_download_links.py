import os
from constants import DOWNLOAD_FOLDER_PATH
from parsing.parse_selected import parse_selected

def construct_download_links(identifier,selected_files):
    file_list = parse_selected(selected_files=selected_files)
    download_links = []
    for file in file_list:
        link = f"https://archive.org/download/{identifier}/{file}"
        download_links.append(link)
    metadata_folder_path = os.path.join(DOWNLOAD_FOLDER_PATH, identifier, "metadata") #create the metadata folder path
    with open(f'{metadata_folder_path}/download_links.txt', 'w') as f:
        for link in download_links:
            f.write(link + '\n')