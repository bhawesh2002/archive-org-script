#v0.3.0:
#Minor Feature: Implement extract_extensions function to extract all the extensions in the filetree

def extract_extensions(filetree,extensions):
    """
    Extracts all the extensions in the filetree and appends them to the extensions list.
    Args:
        filetree (dict): The filetree dictionary.
        extensions (list): The list of extensions.
    Returns:
        None
    """
    
    exts = extensions

    for key, value in filetree.items():
        if isinstance(value, dict):
            extract_extensions(value,extensions=exts)
        else:
            # Check for compound extensions
            if key.endswith('.tar.gz') or key.endswith('.html.gz') or key.endswith('.json.gz') or key.endswith('.txt.gz') or key.endswith('.tar.bz2') or key.endswith('.tar.xz'):
                ext = '.'.join(key.split('.')[-2:])
            # Check for abbyy extensions
            elif key.endswith('_abbyy.gz'):
                ext = '.'.join(key.split('_')[-1:])
            # Check for normal extensions  
            else:
                ext = key.split('.')[-1]
            #add the ext to the list of extensions if it is does not exist in the list
            if ext not in exts:
                exts.append(ext)