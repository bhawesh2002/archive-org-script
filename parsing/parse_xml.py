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

    for file in root.findall('.//file'): # Find all 'file' elements in the XML file
        name = file.get('name') # Get the 'name' attribute of the file element
        size = file.find('size') # Find the 'size' element
        private = file.find('private') # Find the 'private' element
        size = size.text if size is not None else 'Unknown' # Check if size is found
        #0.1.1:
        #Info: Only includes the size of the file

        #0.2.0: 
        #Minor Feature: Include the size and private status of the file
        private = private.text if private is not None else 'false' # Check if private is found
        folders = name.split('/') # Split the file path into folders
        current_level = file_tree # Start at the root level of the dictionary
        for folder in folders[:-1]: # Iterate through all folders except the last one as it is the file name
            if folder not in current_level: # Check if the folder is already in the dictionary
                current_level[folder] = {} # Create an empty dictionary for the folder
            current_level = current_level[folder] # Move to the next level of the dictionary
        # Include the file name and its size | private in the dictionary
        current_level[folders[-1]] = f"{size}|{private}"
    
    # Replace "files.xml" with "filetree.json" in the xml_file string
    json_filename = xml_file.replace("files.xml", "filetree.json")
    
    with open(json_filename, 'w') as json_file:
        json.dump(file_tree, json_file, indent=4)
