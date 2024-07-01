#v0.2.0 and before:
#Old versions: Does not contain the functionality to filter out private files from the selected files dictionary

#v0.2.1:
#Bug Fix: Implement filter_priv_files function to filter out private files from the selected files dictionary

def filter_priv_files(selected_files):
    """
    Uses:
        Filters out private files from the selected files dictionary.

    Functioning:
        It uses list comprehension to identify private files and stores their keys in a list called `privates`.
        If the value of a key in the selected files dictionary is a dictionary, the function calls itself 
        recursively to filter out private files from the nested dictionary.

    Args:
        selected_files (dict): A dictionary of selected files where the key is the file name
        and the value is a string containing the file size and private status separated by '|'.
        
    Returns:
    None: The function modifies the input dictionary in place, removing any
          entries that are marked as private.

    """
    #Identify private files using list comprehension
    privates = [key for key, value in selected_files.items() 
                if isinstance(value, str) and value.split('|')[1] == 'true']

    #Recursively filter private files from nested dictionaries
    for key in list(selected_files):
        if isinstance(selected_files[key], dict):
            filter_priv_files(selected_files[key])

    #Remove private files from the selected files dictionary
    for key in privates:
        selected_files.pop(key)