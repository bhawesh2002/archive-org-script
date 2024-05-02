import json

def extract_keys_and_parents(obj, target_keys, path=None):
    """
    Recursively searches for target keys in a JSON object and returns their paths.
    
    :param obj: The JSON object to search.
    :param target_keys: The list of keys to find.
    :param path: The current path to the key (default None).
    :return: A dictionary containing found values and their paths.
    """
    if path is None:
        path = []

    results = {}
    
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in target_keys:
                results[k] = (v, path + [k])
            elif isinstance(v, (dict, list)):
                nested_results = extract_keys_and_parents(v, target_keys, path + [k])
                if nested_results:
                    results.update(nested_results)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            nested_results = extract_keys_and_parents(item, target_keys, path + [i])
            if nested_results:
                results.update(nested_results)
    
    return results

def list_to_nested_dict(input_list):
    """
    Converts a list to a nested dictionary based on the pattern:
    [
        "value",
        ["key1", "key2",..., "keyN"]
    ] -> {
        "key1": {
            "key2": {
              ...
                "keyN": "value"
            }
        }
    }
    """
    if len(input_list) < 2:
        raise ValueError("Input list must contain at least two elements")
    
    value = input_list[0]
    keys = input_list[1:]
    
    if len(keys) == 1:
        return {keys[0]: value}
    else:
        return {keys[0].replace('_', '.'): list_to_nested_dict([value] + keys[1:])}

def merge_nested_dicts(d1, d2):
    """
    Recursively merges two nested dictionaries.
    
    :param d1: The first nested dictionary.
    :param d2: The second nested dictionary.
    :return: The merged nested dictionary.
    """
    if not isinstance(d1, dict) or not isinstance(d2, dict):
        return d2
    
    merged = d1.copy()
    for key, value in d2.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_nested_dicts(merged[key], value)
        else:
            merged[key] = value
    return merged

# Load the JSON data from test.json
with open('test.json', 'r') as file:
    data = json.load(file)

# Define the target keys you want to extract
target_keys = ['1.jpg','2.jpg', '01.mp4']
# Extract the keys and their paths
results = extract_keys_and_parents(data, target_keys)

# Check if any of the target keys were found
if results:
    transformed_data = {}
    for key, (value, path) in results.items():
        # Merge extracted data into a single nested structure
        transformed_data = merge_nested_dicts(transformed_data, list_to_nested_dict([value] + path))
    
    # Save the transformed data to extracted.json
    with open('extracted.json', 'w') as file:
        json.dump(transformed_data, file, indent=4)
    print("Keys and their paths were successfully extracted, transformed, and saved to extracted.json.")
else:
    print("None of the target keys were found in the JSON data.")