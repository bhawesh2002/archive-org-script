# from colorama import Fore, Style # Used for colored text output in the console
import os
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
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)

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
def get_input(stdscr):
    # Prompt the user to enter a link
    stdscr.addstr(1,0,"Paste the link here: ", curses.color_pair(4))
    stdscr.refresh()
    # Enable keypad mode to recognize arrow keys
    stdscr.keypad(True)
    return stdscr.getstr().decode('utf-8').strip()

# Parses the XML file (assumed to be _files.xml) and dumps it to json file.
def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    file_tree = {}

    for file in root.findall('.//file'):
        name = file.get('name')
        size_element = file.find('size') # Find the size element
        size = size_element.text if size_element is not None else 'Unknown' # Check if size element is found
        folders = name.split('/')
        current_level = file_tree
        for folder in folders[:-1]: # Iterate through all folders except the last one
            if folder not in current_level:
                current_level[folder] = {}
            current_level = current_level[folder]
        # Include the file name and its size in the dictionary
        current_level[folders[-1]] = size
    
    # Replace "files.xml" with "filetree.json" in the xml_file string
    json_filename = xml_file.replace("files.xml", "filetree.json")
    
    with open(json_filename, 'w') as json_file:
        json.dump(file_tree, json_file, indent=4)

#Prints the structure in a tree-like format using color and styling.
def display_directory_struct(stdscr, directory_dict, selected_option, indent_level=0, scroll_offset=0, visible_lines=0):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    # Print directory
    for idx, (option, child_folder) in enumerate(directory_dict.items()):
        if idx < scroll_offset or idx >= scroll_offset + visible_lines:
            continue # Skip options that are not visible

        x = w//2 - len(option)//2
        y = idx - scroll_offset + 1 # Adjust y position based on scroll_offset

        # Ensure y is within the bounds of the window
        if y < 0 or y >= h:
            continue

        # Ensure x is within the bounds of the window
        if x < 0 or x + len(option) + indent_level * 2 >= w:
            continue

        if idx == selected_option:
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(y, x + indent_level * 2, option)
            stdscr.attroff(curses.A_REVERSE)
        else:
            stdscr.addstr(y, x + indent_level * 2, option)

        if child_folder is not None:
            stdscr.addstr(y, x + len(option) + indent_level * 2, " ->")

    stdscr.refresh()

def load_directory_struct(file_path):
    with open(file_path, "r") as file:
        directory_struct = json.load(file)
    return directory_struct

def main(stdscr):
    curses.echo()
    init_colors() # Initialize color pairs

    stdscr.addstr("archive.org downloader", curses.color_pair(1) | curses.A_BOLD)
    stdscr.refresh()
    
    #validate the link
    valid_link = False
    while not valid_link:
        stdscr.refresh()
        download_link = get_input(stdscr)
        if validate_link(download_link):
            valid_link = True
        else:
            stdscr.addstr(1, 0, " " * 100)
            stdscr.refresh()

            stdscr.addstr(2, 0, "Error: Invalid archive.org download directory link format.", curses.color_pair(2))
            stdscr.refresh()

    #extract the indentifier from the link
    directory_identifier = get_directory_identifier(download_link)
    stdscr.addstr(3, 0, "Directory Name: ", curses.color_pair(3))
    stdscr.addstr(directory_identifier)
    stdscr.refresh()

    # Download _files.xml and _meta.xml
    files_url, meta_url = get_identifier_file_xml(directory_identifier)
    download_file(files_url, f"{directory_identifier}_files.xml")
    download_file(meta_url, f"{directory_identifier}_meta.xml")
    
    # Parse the _files.xml after the file has been downloaded
    files_xml = f"{directory_identifier}_files.xml"
    parse_xml(files_xml)
    
    #display the directory structure
    current_option = 0
    scroll_offset = 0
    indent_level = 0
    parent_folders = [] # Keep track of parent folder
    parent_indices = [] # Keep track of selected indices in parent folder

    #load the json file containing directory structure info
    directory_struct_json = load_directory_struct(f"E:\\Tutorials\\archive org script\\{directory_identifier}_filetree.json")
    
    while True:
        h, w = stdscr.getmaxyx()
        visible_lines = h - 2 # Calculate the number of visible lines
        display_directory_struct(stdscr, directory_struct_json, current_option, indent_level, scroll_offset, visible_lines)

        key = stdscr.getch()

        if key == curses.KEY_UP and current_option > 0:
            current_option -= 1
            if current_option < scroll_offset:
                scroll_offset = current_option
        elif key == curses.KEY_DOWN and current_option < len(directory_struct_json) - 1:
            current_option += 1
            if current_option >= scroll_offset + visible_lines:
                scroll_offset = current_option - visible_lines + 1
        elif key == curses.KEY_RIGHT:
            selected_option = list(directory_struct_json.keys())[current_option]
            child_folder = directory_struct_json[selected_option]
            if child_folder is not None:
                parent_folders.append(directory_struct_json) # Store current folder as parent
                parent_indices.append(current_option) # Store current selected index as parent index
                indent_level += 1
                directory_struct_json = child_folder
                current_option = 0
        elif key == curses.KEY_LEFT and indent_level > 0:
            indent_level -= 1
            directory_struct_json = parent_folders.pop() # Retrieve previous folder from parent_folders
            current_option = parent_indices.pop() # Retrieve previous selected index from parent_indices
        elif key == curses.KEY_ENTER or key in [10, 13]:
            selected_option = list(directory_struct_json.keys())[current_option]
            child_folder = directory_struct_json[selected_option]
            if child_folder is not None:
                parent_folders.append(directory_struct_json) # Store current folder as parent
                parent_indices.append(current_option) # Store current selected index as parent index
                directory_struct_json = child_folder
                current_option = 0
            else:
                stdscr.clear()
                stdscr.addstr(0, 0, "You selected: " + selected_option)
                stdscr.refresh()
                stdscr.getch()
        elif key == ord('q'):
            break
        elif key == curses.KEY_PPAGE: # Scroll up
            if scroll_offset > 0:
                scroll_offset -= 1
        elif key == curses.KEY_NPAGE: # Scroll down
            if current_option < len(directory_struct_json) - 1:
                scroll_offset += 1


if __name__ == "__main__":
    curses.wrapper(main)
