import curses
import os
import time # for creating directories for downloaded files
import requests # for downloading the file
import threading # for running the download in a separate thread
from constants import DOWNLOAD_FOLDER_PATH # Import the download folder path

# Headers to avoid content encoding
HEADERS = {
        'Accept-Encoding': 'identity'
}

# Create a folder to store the downloaded files
def create_metadata_folder(identifier):
     # Create a folder named after the identifier inside script_downloads in the current working directory
    metadata_folder_path = os.path.join(DOWNLOAD_FOLDER_PATH, identifier, "metadata")
    os.makedirs(metadata_folder_path, exist_ok=True)
    return metadata_folder_path

# Function to download the metadata files(will run in background)
def download_metadata_files(stdscr,identifier,queue,):
    status = False # Set the status to False by default
    try: 
        y = stdscr.getyx()[0] # Get the current y position of the cursor
        # Download *_meta.xml
        meta_xml_request = requests.get(f"https://archive.org/download/{identifier}/{identifier}_meta.xml", headers=HEADERS, allow_redirects=True)
        # If the download is successful, save the files to the metadata folder
        if meta_xml_request.status_code == 200:
            metadata_folder_path = create_metadata_folder(identifier) #create the download folder
            meta_xml_size = meta_xml_request.headers.get('Content-Length', None) # Get the size of the meta.xml file
            meta_downloaded_size = 0
            with open(f"{metadata_folder_path}/{identifier}_meta.xml", 'wb') as meta_xml:
                for chunk in meta_xml_request.iter_content(chunk_size=10): # Write the file in 10 byte chunks
                    if chunk:
                        meta_xml.write(chunk)
                        meta_downloaded_size += len(chunk)
                        stdscr.addstr(y+1,0,f"{identifier}_meta.xml: {meta_downloaded_size}/{meta_xml_size} bytes", curses.color_pair(4) | curses.A_BOLD)
                        stdscr.refresh()
                meta_xml.close() # Close the file after writing
            status = True # Set the status to True if the download is successful
        else:
            status = False # Set the status to False if the download fails
        
        # Download *_files.xml
        files_xml_request = requests.get(f"https://archive.org/download/{identifier}/{identifier}_files.xml", headers=HEADERS, allow_redirects=True)
        # If the download is successful, save the files to the metadata folder
        if files_xml_request.status_code == 200:
            files_xml_size = files_xml_request.headers.get('Content-Length', None) # Get the size of the files.xml file
            files_downloaded_size = 0
            with open(f"{metadata_folder_path}/{identifier}_files.xml", 'wb') as files_xml:
                for chunk in files_xml_request.iter_content(chunk_size=10): # Write the file in 10 byte chunks
                    if chunk:
                        files_xml.write(chunk)
                        files_downloaded_size += len(chunk)
                        stdscr.addstr(y+2,0,f"{identifier}_files.xml: {files_downloaded_size}/{files_xml_size} bytes", curses.color_pair(4) | curses.A_BOLD)
                        stdscr.refresh()
                files_xml.close() # Close the file after writing
            status = True # Set the status to True if the download is successful
        else:
            status = False # Set the status to False if the download fails

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
            stdscr.deleteln()
            stdscr.addstr(y,0,"Metadata Downloaded Successfully\n", curses.color_pair(5) | curses.A_BOLD)
            time.sleep(0.5)
            stdscr.refresh()
            return True # Return True if the download is successful

        # If the download fails, display an error message and exit the program
        else:
            y = stdscr.getyx()[0]
            stdscr.deleteln()
            stdscr.deleteln()
            stdscr.addstr(y,0,f"Metadata Download Failed", curses.color_pair(3) | curses.A_BOLD)
            stdscr.refresh()
            time.sleep(1)
            stdscr.deleteln()
            stdscr.addstr(y,0,"Re-enter Download Link", curses.color_pair(4) | curses.A_BOLD)
            return False # Return False if the download fails

    except Exception as e:
        raise e