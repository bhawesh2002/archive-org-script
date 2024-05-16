def select_item(selected_files, current_path, selected_option, directory_dict):
    full_path = '/'.join(current_path + [selected_option])
    if isinstance(directory_dict[selected_option], dict):
        # If the selected item is a folder, recursively select all files within it
        for item in directory_dict[selected_option]:
            select_item(selected_files, current_path + [selected_option], item, directory_dict[selected_option])
    else:
        # If the selected item is a file, add it to the selected files
        selected_files.append(full_path)
