import copy

from selection_deselection.filter_empty_dirs import filter_empty_dirs
from selection_deselection.filter_priv_files import filter_priv_files

#v0.2.2 and before:
#Old versions: Does not contain the functionality to select/deselect all files and folders

#v0.2.3:
#Patch: Implement select_all and deselect_all functions to select/deselect all files and folders in the filetree
#Changes:
#    - Implement select_all function to select all files and folders in the filetree
#    - Implement deselect_all function to deselect all files and folders in the selected files dictionary

def select_all(filetree):
    """
    Selects all files and folders in the filetree.

    Args:
        selected_files (dict): A dictionary of selected files

    Returns:
        dict: A dictionary containing all files and folders in the filetree.
    """
    all_files = copy.deepcopy(filetree) #copy the filetree to all_files to select all files
    filter_priv_files(selected_files=all_files) #filter out private files from the selected files
    filter_empty_dirs(selected_files=all_files) #filter out empty directories from the selected files
    return all_files

def deselect_all(selected_files):
    """
    Deselects all files and folders in the selected files dictionary.

    Args:
        selected_files (dict): A dictionary of selected files

    Returns:
        dict: An empty dictionary representing no selected files.
    """
    deselected_files = selected_files #copy the selected files
    deselected_files.clear() #clear the deselected_files dictionary to deselect all files
    return deselected_files