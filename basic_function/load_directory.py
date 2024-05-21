import os # for creating directories for downloaded files
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

# def download_metadata_files(identifier):
    # download_folder_path = create_download_folder()
    # identifier_folder = os.path.join(download_folder_path, identifier)
    # os.mkdir(identifier_folder)
    # files_xml_size, meta_xml_size = get_metadata_size(identifier)
    # try:
        # meta_xml = response = requests.get(f"https://archive.org/download/{identifier}/{identifier}_meta.xml", stream=True)
        # if meta_xml.status_code == 200:
            # meta_xml_file_path = os.path.join(identifier_folder, f"{identifier}_meta.xml")
            # with open(meta_xml_file_path, 'wb') as f:
                # f.write(response.content)
        # files_xml = response = requests.get(f"https://archive.org/download/{identifier}/{identifier}_files.xml", stream=True)
        # if files_xml.status_code == 200:
            # files_xml_file_path = os.path.join(identifier_folder, f"{identifier}_files.xml")
            # with open(files_xml_file_path, 'wb') as f:
                # f.write(response.content)
                # 
    # except requests.RequestException as e:
        # raise e
# 
# def create_download_folder():
    # script_path = os.path.abspath(__file__)
    # grandparent_dir = os.path.dirname(os.path.dirname(script_path))
    # downloads_folder_path = os.path.join(grandparent_dir, 'Downloads')
    # Create the Downloads folder if it doesn't exist
    # os.makedirs(downloads_folder_path, exist_ok=True)
    # return downloads_folder_path