from colorama import Fore, Style # Used for colored text output in the console
from bs4 import BeautifulSoup
import requests # Used to download files from URLs
import xml.etree.ElementTree as ET # Used for parsing XML files
import json
import curses

# Initialize color pairs for curses
def init_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

# Constructs URLs for _files.xml and _meta.xml files based on the provided archive.org download directory identifier.
def get_identifier_file_xml(item_identifier):
    base_url = f"https://archive.org/download/{item_identifier}/"
    files_url = f"{base_url}{item_identifier}_files.xml"
    meta_url = f"{base_url}{item_identifier}_meta.xml"
    return files_url, meta_url

# Downloads a file from the given URL and saves it with the specified filename. Prints success/failure messages.
def download_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename} successfully.") #print success message
        return True
    else:
        print(f"Failed to download {filename}. Status code: {response.status_code}") #print error message
        return False

# Checks if the link follows the format of an archive.org download directory link.
def validate_link(link):
    return "https://archive.org/download/" in link

# Extracts the identifier from a valid archive.org download directory link.
def get_directory_identifier(link):
    return link.split("/")[-1]

# Prompts the user for input with the specified message and returns the stripped input.
def get_input(stdscr, prompt):
    stdscr.addstr(0, 0, prompt)
    stdscr.refresh()
    return stdscr.getstr().decode('utf-8').strip()

# Parses the XML file (assumed to be _files.xml) and builds a dictionary representing the directory structure. Prints the structure in a tree-like format using color and styling.
def parse_xml(xml_file):
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

def display_directory_struct(stdscr, directory_dict, selected_option, indent_level=0, scroll_offset=0):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    visible_lines = h - 2 # Subtract 2 for the border
    for idx, (option, child_folder) in enumerate(directory_dict.items()):
        if idx < scroll_offset or idx >= scroll_offset + visible_lines:
            continue # Skip options that are not visible
        x = w // 2 - len(option) // 2
        y = idx - scroll_offset + 1 # Adjust y position based on scroll_offset
        if y < 0 or y >= h:
            continue
        if x < 0 or x + len(option) + indent_level * 2 >= w:
            continue
        if idx == selected_option:
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(y, x + indent_level * 2, option, curses.color_pair(4))
            stdscr.attroff(curses.A_REVERSE)
        else:
            stdscr.addstr(y, x + indent_level * 2, option, curses.color_pair(4))
        if child_folder is not None:
            stdscr.addstr(y, x + len(option) + indent_level * 2, " ->", curses.color_pair(4))
    stdscr.refresh()

def load_directory_struct(file_path):
    with open(file_path, "r") as file:
        directory_struct = json.load(file)
    return directory_struct

def main(stdscr):
    init_colors() # Initialize color pairs
    curses.curs_set(0) # Hide the cursor
    current_option = 0
    scroll_offset = 0
    indent_level = 0
    parent_folders = [] # Keep track of parent folder
    parent_indices = [] # Keep track of selected indices in parent folder

    stdscr.addstr(0, 0, "archive.org downloader", curses.color_pair(1))
    stdscr.refresh()

    valid_link = False
    while not valid_link:
        stdscr.addstr(1, 0, "Enter archive.org download directory link: ", curses.color_pair(1))
        stdscr.refresh()
        download_link = get_input(stdscr, Fore.WHITE + "(Paste the link here)" + Style.RESET_ALL + ": ")
        if validate_link(download_link):
            valid_link = True
        else:
            stdscr.addstr(2, 0, "Error: Invalid archive.org download directory link format.", curses.color_pair(2))
            stdscr.refresh()

    directory_identifier = get_directory_identifier(download_link)
    stdscr.addstr(3, 0, "Directory Name: " + directory_identifier, curses.color_pair(3))
    stdscr.refresh()

    # Download _files.xml and _meta.xml
    files_url, meta_url = get_identifier_file_xml(directory_identifier)
    download_file(files_url, f"{directory_identifier}_files.xml")
    download_file(meta_url, f"{directory_identifier}_meta.xml")
    # Assuming the _files.xml file has been downloaded
    files_xml = f"{directory_identifier}_files.xml"
    parse_xml(files_xml)
    directory_struct_json = load_directory_struct("E:\\Tutorials\\archive org script\\file_tree.json")
    while True:
        display_directory_struct(stdscr, directory_struct_json, current_option, indent_level, scroll_offset)
        key = stdscr.getch()
        # Handle key presses for navigation
        # Implement your key handling logic here

if __name__ == "__main__":
    curses.wrapper(main)
