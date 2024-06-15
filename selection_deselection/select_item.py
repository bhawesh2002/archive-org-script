def add_to_selected_files(selected_files, selection, current_path, directory):
    current_level = selected_files #set the current level to the selected files
    for folder in current_path: #traverse the current path
        if folder not in current_level: #check if the folder is not in the current level
            current_level[folder] = {} #add the folder to the current level
        current_level = current_level[folder] #move to the next level of the current level
    current_level[selection] = directory[selection] #add the selection to the current level
    return selected_files