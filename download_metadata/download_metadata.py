import os #for creating directories for dwonaloded files
import requests # Used to download files from URLs

# Downloads a file from the given URL and saves it with the specified filename. Prints success/failure messages.
def download_metadata_files(item_identifier, destination_folder):
    base_url = f"https://archive.org/download/{item_identifier}/"
    directory_file = f"{item_identifier}_files.xml" #name of *_files.xml conaining info about all the files in directory
    meta_file = f"{item_identifier}_meta.xml" #name of *_meta.xml containing info about the collection
    for metadata_file in [directory_file,meta_file]:
        url = f"{base_url}/{metadata_file}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                os.makedirs(destination_folder, exist_ok=True)
                file_path = os.path.join(destination_folder, metadata_file)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                    print(f"Successfully downloaded {metadata_file}")
            else:
                print(f"Failed to download {metadata_file}. Status code: {response.status_code}")
                return False
        except Exception as e:
            print("An error occurred while downloading file:", metadata_file, ":", e)
            return False
        
    return True