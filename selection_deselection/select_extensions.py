#v0.3.0:
#Minor Feature: Implement select_extensions function to select files with the specified extensions from the filetree which are then appended to the selected_files dictionary
import copy

from selection_deselection.filter_empty_dirs import filter_empty_dirs
from selection_deselection.filter_priv_files import filter_priv_files

def select_extensions(selected_files, filetree, extensions):
    """
    Selects files with the specified extensions from the filetree and appends them to the selected_files dictionary.
    Args:
        selected_files (dict): The selected files dictionary.
        filetree (dict): The filetree dictionary.
        extensions (list): The list of extensions.
    Returns:
        None"""
    #v0.3.1:
    #Bux Fix: Fixed the error when passing empty extensions list throws NoneType error 
    #         by adding a check for extensions list before iterating over it.

    #v0.3.0:
    #Bug: NoneType error when passing empty extensions list
    if extensions is not None:
        for key, value in filetree.items():
            if isinstance(value, dict):
                #if the folder is not in the selected_files dictionary, create it
                if key not in selected_files:
                    selected_files[key] = {}
                #recursively select extensions within the folder
                select_extensions(selected_files[key], value, extensions)
            else:
                # add files ending with the specified extensions to the selected_files dictionary
                if any(key.endswith(ext) for ext in extensions):
                    selected_files[key] = copy.deepcopy(value)

    #filter private files then filter empty folders from selected_files
    filter_priv_files(selected_files=selected_files)
    filter_empty_dirs(selected_files=selected_files)
