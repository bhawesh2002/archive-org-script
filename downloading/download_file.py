import os
import requests

from constants import DOWNLOAD_FOLDER_PATH

def download_file(url,downloader_win,download_path):
    HEADERS = {
            'Accept-Encoding': 'identity' # Avoid content encoding when fetching the headers
    }
    filename = url.split("/")[-1]
    try:
        response = requests.get(url,stream=True, headers=HEADERS)
        if response.status_code == 200:
            filesize = response.headers.get('Content-Length', None)
            bytes_downloaded = 0
            with open(f"{download_path}/{filename}", 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        bytes_downloaded += len(chunk)
                        downloader_win.addstr(2,2,f'Downloading {filename} - {bytes_downloaded}/{filesize}')
                        downloader_win.clrtoeol()
                        downloader_win.refresh()
                f.close()
    except requests.HTTPError as http_err:
        downloader_win.addstr(2,2,f'HTTP error occurred: {http_err}')
        downloader_win.refresh()
    except Exception as e:
        downloader_win.addstr(2,2,f'An error occurred: {e}')
        downloader_win.refresh()
