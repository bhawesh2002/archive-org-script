import copy
from selection_deselection.filter_priv_files import filter_priv_files


def toggle_selection(selected_files, selection, current_path, directory):
    current_level = selected_files #set the current level to the selected files
    for folder in current_path: #traverse the current path
        if folder not in current_level: #check if the folder is not in the current level
            current_level[folder] = {} #add the folder to the current level
        current_level = current_level[folder] #move to the next level of the current level
    if selection not in current_level:    
        #v0.1.0: 
        #Bug: Old code that uses reference(Shallow Copy) to add selection to selected_files. This will modify `directory` when removing selection.
        #Old Code: 
        #   current_level[selection] = directory[selection] 

        #v0.1.1:
        #Bug Fix: Use Deep Copy to avoid referencing `directory` to add selection to selected_files. This will prevent modifying `directory` when removing selection.
        current_level[selection] = copy.deepcopy(directory[selection]) #copy the selected file to the current level
    else:
        current_level.pop(selection) #remove the selected file from the current level
    #v0.2.0 and before:
    #Old Code: returns selected_files without filtering out private files
    
    #v0.2.1:
    #Bug Fix: call filter_priv_files to filter out private files from the selected files dictionary before returning selected_files
    filter_priv_files(selected_files=selected_files)
    
    return selected_files