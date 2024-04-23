from colorama import Fore, Style
from bs4 import BeautifulSoup
import requests
import xml.etree.ElementTree as ET
import os

def get_identifier_file_xml(item_identifier):
    """Constructs URLs for _files.xml and _meta.xml files for the given item identifier."""
    base_url = f"https://archive.org/download/{item_identifier}/"
    files_url = f"{base_url}{item_identifier}_files.xml"
    meta_url = f"{base_url}{item_identifier}_meta.xml"
    return files_url, meta_url

def download_file(url, filename):
    """Downloads a file from the given URL."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename} successfully.")
        return True
    else:
        print(f"Failed to download {filename}. Status code: {response.status_code}")
        return False

def parse_files_xml(files_xml):
    """Parse the _files.xml and extract file information."""
    file_structure = {}
    try:
        tree = ET.parse(files_xml)
        root = tree.getroot()
        for file in root.findall('.//file'):
            name = file.get('name')
            if '/' in name:  # If the file is within a folder
                folder, filename = name.split('/', 1)
                if folder not in file_structure:
                    file_structure[folder] = []
                file_structure[folder].append(filename)
            else:
                if 'files' not in file_structure:
                    file_structure['files'] = []
                file_structure['files'].append(name)
    except Exception as e:
        print(f"Error parsing {files_xml}: {e}")
    return file_structure

def display_directory_structure(file_structure):
    """Display the directory structure."""
    print(Fore.YELLOW + Style.BRIGHT + "Directory Structure:" + Style.RESET_ALL)
    for folder, files in file_structure.items():
        print(Fore.CYAN + f"\n{folder}/" + Style.RESET_ALL)
        for filename in files:
            print(f"  {filename}")

def validate_link(link):
    """Checks if the link is a valid archive.org download directory link."""
    return "https://archive.org/download/" in link

def get_directory_identifier(link):
    """Extracts the identifier from the download link."""
    return link.split("/")[-1]

def get_input(prompt):
    """Get user input with specified prompt."""
    return input(prompt).strip()

def main():
    print(Fore.GREEN + Style.BRIGHT + "archive.org downloader" + Style.RESET_ALL)

    valid_link = False
    while not valid_link:
        print(Fore.BLUE + "Enter archive.org download directory link: " + Style.RESET_ALL, end="")
        download_link = get_input(Fore.WHITE + "(Paste the link here)" + Style.RESET_ALL + ": ")

        if validate_link(download_link):
            valid_link = True
        else:
            print(Fore.RED + "Error: Invalid archive.org download directory link format." + Style.RESET_ALL)

    directory_identifier = get_directory_identifier(download_link)
    print(Fore.YELLOW + Style.BRIGHT + "Directory Name: " + Fore.WHITE + Style.RESET_ALL + f"{directory_identifier}")

    # Download _files.xml and _meta.xml
    files_url, meta_url = get_identifier_file_xml(directory_identifier)
    download_file(files_url, f"{directory_identifier}_files.xml")
    download_file(meta_url, f"{directory_identifier}_meta.xml")
    # Assuming the _files.xml file has been downloaded
    files_xml = f"{directory_identifier}_files.xml"

    # Parse _files.xml and extract file information
    file_structure = parse_files_xml(files_xml)
    # Display the directory structure
    display_directory_structure(file_structure)
if __name__ == "__main__":
    main()
