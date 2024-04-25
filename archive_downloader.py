from colorama import Fore, Style #Used for colored text output in the console
from bs4 import BeautifulSoup
import requests #Used to download files from URLs
import xml.etree.ElementTree as ET #Used for parsing XML files
import os
import json
#Constructs URLs for _files.xml and _meta.xml files based on the provided archive.org download directory identifier.
def get_identifier_file_xml(item_identifier):
    """Constructs URLs for _files.xml and _meta.xml files for the given item identifier."""
    base_url = f"https://archive.org/download/{item_identifier}/"
    files_url = f"{base_url}{item_identifier}_files.xml"
    meta_url = f"{base_url}{item_identifier}_meta.xml"
    return files_url, meta_url

#Downloads a file from the given URL and saves it with the specified filename. Prints success/failure messages.
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

#Checks if the link follows the format of an archive.org download directory link.
def validate_link(link):
    """Checks if the link is a valid archive.org download directory link."""
    return "https://archive.org/download/" in link

#Extracts the identifier from a valid archive.org download directory link.
def get_directory_identifier(link):
    """Extracts the identifier from the download link."""
    return link.split("/")[-1]

#Prompts the user for input with the specified message and returns the stripped input.
def get_input(prompt):
    """Get user input with specified prompt."""
    return input(prompt).strip()

#Parses the XML file (assumed to be _files.xml) and builds a dictionary representing the directory structure. Prints the structure in a tree-like format using color and styling.
def parse_xml(xml_file):
    """Parses the XML file and dumps it to a json file."""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    file_tree = {}
    print(Fore.MAGENTA + Style.BRIGHT + "Creating Directory Structure" + Style.RESET_ALL)
    print(Fore.GREEN + Style.BRIGHT + "Root(/)" + Style.RESET_ALL)
    for file in root.findall('.//file'):
        name = file.get('name')
        folders = name.split('/')
        current_level = file_tree
        for folder in folders[:-1]: # Iterate through all folders except the last one
            if folder not in current_level:
                current_level[folder] = {}
            current_level = current_level[folder]
        current_level[folders[-1]] = None # The last part is the file name
    with open('file_tree.json', 'w') as json_file:
        json.dump(file_tree, json_file, indent=4)

#Recursively prints the directory tree structure based on the dictionary created in parse_xml. Uses indentation and color coding to differentiate folders and files.
def print_tree(tree, indent=0, depth=0):
    """Recursively prints the tree structure with '/' appended to folders, using color and style."""
    for key, value in tree.items():
        if value: # Check if the current item has child elements (i.e., it's a folder)
            if depth == 0:
                print(Fore.BLUE + Style.BRIGHT +'  ' * indent + key + '/' + Style.RESET_ALL) # Append '/' to folder names and color it BLUE
            else:
                print(Fore.LIGHTCYAN_EX + Style.BRIGHT +'  ' * indent + key + '/' + Style.RESET_ALL) # Color subfolders CYAN
            print_tree(value, indent + 1, depth + 1)
        else:
            print(Style.BRIGHT+'  ' * indent + key + Style.RESET_ALL) # Files are printed without '/'

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
    parse_xml(files_xml)
    
if __name__ == "__main__":
    main()
