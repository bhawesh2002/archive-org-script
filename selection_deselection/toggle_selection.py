import select_item #importing the select_item module

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
