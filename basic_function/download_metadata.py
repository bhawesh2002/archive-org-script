import curses
import os
import time # for creating directories for downloaded files
import requests # for downloading the file
import threading # for running the download in a separate thread
from constants import DOWNLOAD_FOLDER_PATH # Import the download folder path

# Get the size of the metadata files
def get_metadata_size(identifier):
    # Headers to avoid content encoding
    headers = {
        'Accept-Encoding': 'identity'
    }
    try:
        files_response = requests.head(f"https://archive.org/download/{identifier}/{identifier}_files.xml", headers=headers, allow_redirects=True)
        meta_response = requests.head(f"https://archive.org/download/{identifier}/{identifier}_meta.xml", headers=headers, allow_redirects=True)
        if files_response.status_code == 200 and meta_response.status_code == 200:
            files_xml_size = files_response.headers.get('Content-Length', None) # Get the size of the files.xml file
            meta_xml_size = meta_response.headers.get('Content-Length', None) # Get the size of the meta.xml file
            return files_xml_size, meta_xml_size
        else:
            return False
    except requests.RequestException as e:
        raise e

# Create a folder to store the downloaded files
def create_metadata_folder(identifier):
     # Create a folder named after the identifier inside script_downloads in the current working directory
    metadata_folder_path = os.path.join(DOWNLOAD_FOLDER_PATH, identifier, "metadata")
    os.makedirs(metadata_folder_path, exist_ok=True)
    return metadata_folder_path

# Function to download the metadata files(will run in background)
def download_metadata_files(stdscr,identifier,queue,):
    metadata_folder_path = create_metadata_folder(identifier) #create the download folder
    attempts = 0 # Number of attempts to download the files
    status = False # Status of the download
    try: 
        while not status:
            if attempts >= 3:
                y = stdscr.getyx()[0]
                stdscr.addstr(y,0,f"Error: Maximum Attempts Reached\n", curses.color_pair(4))
                break
            attempts += 1
            # Download the *_meta.xml file
            meta_response = requests.get(f"https://archive.org/download/{identifier}/{identifier}_meta.xml", stream=True)
            if meta_response.status_code == 200:
                with open(f"{metadata_folder_path}/{identifier}_meta.xml", 'wb') as f:
                    f.write(meta_response.content)
                    f.close()
            else:
                continue # If the download fails, try again
            # Download the *_files.xml file
            files_response = requests.get(f"https://archive.org/download/{identifier}/{identifier}_files.xml", stream=True)
            if files_response.status_code == 200:
                with open(f"{metadata_folder_path}/{identifier}_files.xml", 'wb') as f:
                    f.write(files_response.content)
                    f.close()
            else:
                continue # If the download fails, try again

            status = True # If the download is successful, set status to True
    except requests.HTTPError as http_err: # Handle HTTP errors
        print(f'HTTP error occurred: {http_err}')
        raise http_err
    except ConnectionError as conn_err: # Handle connection errors
        print(f'Connection error occurred: {conn_err}')
        raise conn_err
    except requests.Timeout as timeout_err: # Handle timeout errors
        print(f'Timeout error occurred: {timeout_err}')
        raise timeout_err
    except requests.RequestException as req_err: # Handle request errors
        print(f'Request error occurred: {req_err}')
        raise req_err
    except Exception as err: # Handle other errors
        print(f'An error occurred: {err}')
        raise err

    
    queue.put(status) # Send a message to the main thread that the download is done

#Use multithreading to download the metadata files in the background
def download_metadata(stdscr,identifier, queue):
    try:
        # Get the size of the metadata files
        files_xml_size, meta_xml_size = get_metadata_size(identifier) # Get the size of the metadata files
        
        bg_download = threading.Thread(target=download_metadata_files, args=(stdscr,identifier,queue,)) # Run the download in a separate thread
        bg_download.setDaemon(True) # Set the thread as a daemon thread to shut down thread it when the main thread exits
        bg_download.start() # Start the download
        status_msg = "Downloading metadata files"
        y = stdscr.getyx()[0]
        stdscr.addstr(y,0,status_msg, curses.color_pair(4) | curses.A_BOLD)
        while bg_download.is_alive(): # While the download is running in background display a status message
            stdscr.addstr(y,len(status_msg),".", curses.color_pair(4) | curses.A_BOLD)
            stdscr.refresh()
            time.sleep(0.2)
            stdscr.addstr(y,len(status_msg),"..", curses.color_pair(4) | curses.A_BOLD)
            stdscr.refresh()
            time.sleep(0.2)
            stdscr.addstr(y,len(status_msg),"...", curses.color_pair(4) | curses.A_BOLD)
            stdscr.refresh()
            time.sleep(0.2)
            stdscr.addstr(y,len(status_msg),"   ", curses.color_pair(4) | curses.A_BOLD)
            stdscr.refresh()
            time.sleep(0.2)

         
        result = queue.get() # Get the result of the download
        # If the download is successful, display a success message
        if result: 
            stdscr.deleteln()
            stdscr.addstr(y,0,"Metadata Downloaded Successfully\n", curses.color_pair(5) | curses.A_BOLD)
            time.sleep(0.5)
            stdscr.refresh()

        # If the download fails, display an error message and exit the program
        else:
            y = stdscr.getyx()[0]
            stdscr.deleteln()
            stdscr.addstr(y,0,f"Metadata Download Failed\n", curses.color_pair(3) | curses.A_BOLD)
            stdscr.addstr(y,0,"Exiting...\n", curses.color_pair(3) | curses.A_BOLD)
            stdscr.refresh()
            time.sleep(1)
            exit(0)

    except Exception as e:
        raise e