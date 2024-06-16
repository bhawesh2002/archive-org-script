import os
import requests

from constants import DOWNLOAD_FOLDER_PATH

def download_file(url, identifier, filename):
    HEADERS = {
            'Accept-Encoding': 'identity' # Avoid content encoding when fetching the headers
    }
    status = False # Set the status to False by default
    try:
        file = requests.get(url,stream=True,headers=HEADERS)
        if file.status_code == 200:
            file_size = file.headers.get('Content-Length', None)
            bytes_downloaded = 0
            with open(f"{DOWNLOAD_FOLDER_PATH}/{identifier}/'content'/{filename}", 'wb') as f:
                for chunk in file.iter_content(chunk_size=10): # Write the file in 10 byte chunks
                    if chunk:
                        f.write(chunk)
                        bytes_downloaded += len(chunk)
                
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

