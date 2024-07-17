#v0.3.0:
#Minor Feature: Implement extract_extensions function to extract all the extensions in the filetree

#v0.3.3:
#Patch: Use supported_extensions file to extract only the supported extensions from the filetree
def extract_extensions(filetree,extensions):
    """
    Extracts all the supported extensions from the filetree and returns them.
    Args:
        filetree (dict): The filetree dictionary.
        extensions (list): The list of extensions.
    Returns:
        list: The list of extensions.
    """
    
    supported_extensions = [] #list of supported extensions
    with open('supported_extensions','r') as f:
        for line in f:
            if line.startswith(';'): #skip comments
                continue
            else:
                supported_extensions.append(line.strip())
            
    exts = extensions
    for key, value in filetree.items():
        if isinstance(value, dict):
            extract_extensions(value,extensions=exts) #recursively extract extensions
        else:
            for ext in supported_extensions:
                if key.endswith(ext):# if the file ends with the extension
                    exts.append(ext.removeprefix('.') if ext.startswith('.') else ext) #append the extension to the list removing the '.' if it exists
    
    extensions = list(set(exts)) #remove duplicates
    extensions.sort() #sort the extensions
    
    return extensions #return the extensions