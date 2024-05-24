import xml.etree.ElementTree as ET # Used for parsing XML files
import json # Used for dumping the parsed data to a JSON file
import os # Used for appending the path to the XML and JSON file
from constants import DOWNLOAD_FOLDER_PATH
# Parses the XML file (assumed to be _files.xml) and dumps it to json file.
def parse_xml(identifier):
    
    xml_file = os.path.join(DOWNLOAD_FOLDER_PATH, identifier, "metadata",f"{identifier}_files.xml") # Path to the XML file
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
