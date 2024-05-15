# from colorama import Fore, Style # Used for colored text output in the console
import os #for creating directories for dwonaloded files
import requests # Used to download files from URLs
import xml.etree.ElementTree as ET # Used for parsing XML files
import json #to dump json file
import curses #for creation of TUI

# Initialize color pairs for curses
def init_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)

# Downloads a file from the given URL and saves it with the specified filename. Prints success/failure messages.
def download_metadata_files(item_identifier, destination_folder):
    base_url = f"https://archive.org/download/{item_identifier}/"
    directory_file = f"{item_identifier}_files.xml" #name of *_files.xml conaining info about all the files in directory
    meta_file = f"{item_identifier}_meta.xml" #name of *_meta.xml containing info about the collection
    for metadata_file in [directory_file,meta_file]:
        url = f"{base_url}/{metadata_file}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                os.makedirs(destination_folder, exist_ok=True)
                file_path = os.path.join(destination_folder, metadata_file)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                    print(f"Successfully downloaded {metadata_file}")
            else:
                print(f"Failed to download {metadata_file}. Status code: {response.status_code}")
                return False
        except Exception as e:
            print("An error occurred while downloading file:", metadata_file, ":", e)
            return False
    
    return True
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

#converts bytes to MBs
def convert_bytes_to_mb(size):
    """Convert bytes to megabytes."""
    return size / (1024 * 1024)

def select_item(selected_files, current_path, selected_option, directory_dict):
    full_path = '/'.join(current_path + [selected_option])
    if isinstance(directory_dict[selected_option], dict):
        # If the selected item is a folder, recursively select all files within it
        for item in directory_dict[selected_option]:
            select_item(selected_files, current_path + [selected_option], item, directory_dict[selected_option])
    else:
        # If the selected item is a file, add it to the selected files
        selected_files.append(full_path)

#function to toggle the selection of file
def toggle_item(selected_files, current_path, selected_option, directory_dict):
    full_path = '/'.join(current_path + [selected_option])
    if full_path in selected_files:
        selected_files.remove(full_path)
    else:
        # If the selected item is a folder, toggle its selection along with all files within it
        if isinstance(directory_dict[selected_option], dict):
            for item in directory_dict[selected_option]:
                select_item(selected_files, current_path + [selected_option], item, directory_dict[selected_option])
        else:
            # If the selected item is a file, add it to the selected files
            selected_files.append(full_path)

#Prints the structure in a tree-like format using color and styling.
def display_directory_struct(stdscr, directory_dict, selected_files, current_option, identifier_name, current_path=[], indent_level=0, scroll_offset=0, visible_lines=0):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    for idx, (option, child_folder) in enumerate(directory_dict.items()):
        if idx < scroll_offset or idx >= scroll_offset + visible_lines:
            continue

        x = w//2 - len(option)//2
        y = idx - scroll_offset + 1

        if y < 0 or y >= h:
            continue

        if x < 0 or x + len(option) + indent_level * 2 >= w:
            continue
    
        if option in selected_files or '/'.join(current_path + [option]) in selected_files:
            if idx == current_option:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x + indent_level * 2, "*", curses.color_pair(3))
                stdscr.addstr(y, x + indent_level * 2 + 1, option)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x + indent_level * 2, "*", curses.color_pair(3))
                stdscr.addstr(y, (x + indent_level * 2) + 1, option)
        elif idx == current_option:
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(y, x + indent_level * 2, option)
            stdscr.attroff(curses.A_REVERSE)
        else:
            stdscr.addstr(y, x + indent_level * 2, option)

        if isinstance(child_folder, dict): #if child_folder is a dictionary object i.e a folder with nested folder/files
            stdscr.addstr(y, x + (len(option) + indent_level * 2) +1, " ->")   #then display a arrow "->"
        elif isinstance(child_folder, str): #else if child_folder is a string(i.e, size of file) which is associated with child_folder which is name of file
            try:
                file_size_mb = convert_bytes_to_mb(int(child_folder))
                stdscr.addstr(y, x + (len(option) + indent_level * 2) +1, f" ({file_size_mb:.2f} MB)")
            except ValueError:
                stdscr.addstr(y, x + (len(option) + indent_level * 2) +1, " Size: Unknown")
    
    dir_name_label = "Directory Name:"
    stdscr.addstr(h - 2, 0, dir_name_label, curses.color_pair(3))
    stdscr.addstr(h - 2, 16, identifier_name)
    footer_text = "Navigation: Up/Down to navigate, Right to enter directory, Left to go back, Space to select/deselect, q to quit"
    stdscr.addstr(h - 1, 0, footer_text, curses.color_pair(4))
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
    
    # Ensure the script_downloads folder exists
    script_downloads_path = "script_downloads"
    os.makedirs(script_downloads_path, exist_ok=True)

    #validate the link
    valid_link = False
    while not valid_link:
        stdscr.refresh()
        download_link = get_input(stdscr)
        if validate_link(download_link):
            valid_link = True
            stdscr.refresh()
            stdscr.addstr(2, 0, "Success: Valid archive.org download directory link entered.", curses.color_pair(5))
        else:
            stdscr.addstr(1, 0, " " * 100)
            stdscr.refresh()

            stdscr.addstr(2, 0, "Error: Invalid archive.org download directory link format.", curses.color_pair(2))
            stdscr.refresh()

    #extract the indentifier from the link
    directory_identifier = get_directory_identifier(download_link)
    # Create a folder named after the identifier inside script_downloads
    identifier_folder_path = os.path.join(script_downloads_path, directory_identifier)
    os.makedirs(identifier_folder_path, exist_ok=True)
    # Create a metadata folder inside identifier_folder_path
    identifier_metadata_path = os.path.join(identifier_folder_path, 'metadata')
    os.makedirs(identifier_metadata_path, exist_ok=True)

    stdscr.addstr(3, 0, "Directory Name: ", curses.color_pair(3))
    stdscr.addstr(directory_identifier)
    stdscr.refresh()

    # Download _files.xml and _meta.xml
    download_metadata_files(directory_identifier, identifier_metadata_path)
    # download_metadata_file(meta_url, f"{directory_identifier}_meta.xml", identifier_metadata_path)
    
    # Parse the _files.xml after the file has been downloaded
    files_xml = f"{identifier_metadata_path}/{directory_identifier}_files.xml"
    parse_xml(files_xml)
    
    #display the directory structure
    current_option = 0
    scroll_offset = 0
    indent_level = 0
    current_path = []
    selected_files = [] #array containing the selected files

    directory_struct_json = load_directory_struct(f"{identifier_metadata_path}/{directory_identifier}_filetree.json")
    
    while True:
        h, w = stdscr.getmaxyx()
        visible_lines = h - 4
        display_directory_struct(stdscr, directory_struct_json, selected_files, current_option, "identifier", current_path=current_path, indent_level=indent_level, scroll_offset=scroll_offset, visible_lines=visible_lines)

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
            if isinstance(child_folder, dict):
                current_path.append(selected_option)
                indent_level += 1
                directory_struct_json = child_folder
                current_option = 0
                print("current_path:", current_path)
        elif key == curses.KEY_LEFT and indent_level > 0:
            indent_level -= 1
            current_path.pop()
            print("current_path:", current_path)
            directory_struct_json = load_directory_struct(f"{identifier_metadata_path}/{directory_identifier}_filetree.json")
            for folder in current_path:
                directory_struct_json = directory_struct_json[folder]
            current_option = 0
        
        #save the file by adding it to selected_files list
        elif key == ord(' '):
            selected_option = list(directory_struct_json.keys())[current_option]
            toggle_item(selected_files, current_path, selected_option, directory_struct_json)

        elif key == curses.KEY_ENTER or key in [10, 13]:
            selected_option = list(directory_struct_json.keys())[current_option]
            child_folder = directory_struct_json[selected_option]
            if isinstance(child_folder, dict):
                current_path.append(selected_option)
                directory_struct_json = child_folder
                current_option = 0
        #Quit the program
        elif key == ord('q'):
            print("selected_files: ", selected_files)
            break
        #Enable Scrolling
        elif key == curses.KEY_PPAGE:
            if scroll_offset > 0:
                scroll_offset -= 1
        elif key == curses.KEY_NPAGE:
            if current_option < len(directory_struct_json) - 1:
                scroll_offset += 1

if __name__ == "__main__":
    curses.wrapper(main)
