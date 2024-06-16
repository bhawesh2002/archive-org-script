def parse_selected(selected_files, path=''):
    file_paths = []
    for key, value in selected_files.items():
        current_path = path + key
        if isinstance(value, dict):
            file_paths.extend(parse_selected(value, current_path + '/'))
        else:
            file_paths.append(current_path)
    return file_paths