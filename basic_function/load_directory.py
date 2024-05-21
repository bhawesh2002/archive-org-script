import curses
import os
import requests # for downloading the file

def get_metadata_size(identifier):
    # Headers to avoid content encoding
    headers = {
        'Accept-Encoding': 'identity'
    }
    try:
        files_response = requests.head(f"https://archive.org/download/012665756885/012665756885_files.xml", headers=headers, allow_redirects=True)
        meta_response = requests.head(f"https://archive.org/download/012665756885/012665756885_meta.xml", headers=headers, allow_redirects=True)
        if files_response.status_code == 200 and meta_response.status_code == 200:
            files_xml_size = files_response.headers.get('Content-Length', None) # Get the size of the files.xml file
            meta_xml_size = meta_response.headers.get('Content-Length', None) # Get the size of the meta.xml file
            return files_xml_size, meta_xml_size
        else:
            return False
    except requests.RequestException as e:
        raise e

def create_download_folder(identifier):
    # Create a folder named after the identifier inside script_downloads
    download_folder_path = os.path.join(os.getcwd(), "Script Downloads", identifier)
    os.makedirs(download_folder_path, exist_ok=True)
    return download_folder_path

# Download the metadata files
def download_metadata_files(stdscr,identifier):
    download_folder_path = create_download_folder(identifier) #create the download folder
    attempts = 0 # Number of attempts to download the files
    status = False # Status of the download
    try: 
        while not status:
            if attempts >= 3:
                stdscr.addstr(f"Error: Unable to download {identifier}_meta.xml and {identifier}_files.xml\n", curses.color_pair(2))
                break
            attempts += 1
            # Download the *_meta.xml file
            meta_response = requests.get(f"https://archive.org/download/{identifier}/{identifier}_meta.xml", stream=True)
            if meta_response.status_code == 200:
                with open(f"{download_folder_path}/{identifier}_meta.xml", 'wb') as f:
                    f.write(meta_response.content)
                    f.close()
            else:
                stdscr.addstr(f"Error: Unable to download {identifier}_meta.xml\n", curses.color_pair(2))
            # Download the *_files.xml file
            files_response = requests.get(f"https://archive.org/download/{identifier}/{identifier}_files.xml", stream=True)
            if files_response.status_code == 200:
                with open(f"{download_folder_path}/{identifier}_files.xml", 'wb') as f:
                    f.write(files_response.content)
                    f.close()
            else:
                stdscr.addstr(f"Error: Unable to download {identifier}_files.xml\n", curses.color_pair(2))
    except requests.RequestException as e:
        raise (f"download_metadata_files:{e}")
    
    return status # Return the status of the download