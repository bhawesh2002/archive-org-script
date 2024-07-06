# v0.2.1 and before:
# Old versions: Does not contain the functionality to filter out empty directories from the selected files dictionary

# v0.2.2:
# Bug Fix: Implement filter_empty_dirs function to filter out empty directories from the selected files dictionary

def filter_empty_dirs(selected_files):
    """
    Uses:
        Filters out empty directories from the selected files dictionary.
        
        Functioning:
            It uses list comprehension to identify empty directories and stores their keys in a list called `empty_dirs`.
            If the value of a key in the selected files dictionary is a dictionary, the function calls itself 
            recursively to filter out empty directories from the nested dictionary.
        Args:
            selected_files (dict): A dictionary of selected files where the key is the file name
            and the value is a dictionary containing the file size and private status separated by '|'.
            
        Returns:
            None: The function modifies the input dictionary in place, removing any
                  entries that are empty directories.
        
        """
    
    #Identify empty directories using list comprehension
    empty_dirs = [key for key, value in selected_files.items() if isinstance(value, dict) and not value]

    #Recursive Step: Remove empty directories from nested dictionaries
    for key in list(selected_files):
        if isinstance(selected_files[key], dict):

            if selected_files[key]: #check if the directory is not empty
                filter_empty_dirs(selected_files[key]) #then recursively call the function to filter out empty directories

                if not selected_files[key]: #check if the directory is empty after filtering
                    empty_dirs.append(key) #then add the directory to the list of empty directories

    #Remove empty directories from the selected files dictionary
    for key in empty_dirs:
        selected_files.pop(key)
