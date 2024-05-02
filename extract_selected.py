import json

def json_path_to_normal_paths(json_data):
    """
    Converts JSON object paths to normal paths using "/" as the separator.
    
    :param json_data: The JSON data containing multiple nested files.
    :return: A list of normal paths.
    """
    normal_paths = []

    def traverse(data, path):
        if isinstance(data, dict):
            for key, value in data.items():
                traverse(value, path + [key])
        elif isinstance(data, list):
            for index, item in enumerate(data):
                traverse(item, path + [str(index)])
        else:
            # When reaching a leaf node, convert the JSON object path to a normal path
            normal_paths.append('/'.join(path))

    traverse(json_data, [])
    return normal_paths

# Load the JSON data from json_data.json
with open('test.json', 'r') as file:
    json_data = json.load(file)

# Convert the JSON object paths to normal paths
normal_paths = json_path_to_normal_paths(json_data)

# Write the normal paths to extracted_paths.txt
with open('extracted_paths.txt', 'w') as file:
    for path in normal_paths:
        file.write(path + '\n')

print("Extracted paths have been saved to extracted_paths.txt.")
