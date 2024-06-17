
# Archive Org Downloader

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The **Archive Org Downloader** script is a command-line tool designed to simplify downloading files from Archive.org using a specified identifier. It uses the curses library aand provides a user-friendly Terminal User Interface (TUI) which eases the browsing and selection process. Users can easily navigate through the available files, choose the ones they want to download, and download to their local system.

## Features
- **User-Friendly TUI**: Utilizes the curses library to provide a Text User Interface (TUI) for easy interaction.
- **Browse Files**: Navigate through all files available under a specified Archive.org identifier.
- **Multi-Select**: Allows users to select multiple files for downloading at once.
- **Downloading**: Downloads selected files and saves them to a specified directory.
- **Progress Display**: Shows download progress for each file, giving users real-time feedback.

## Installation

### Prerequisites
Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

### Clone the Repository
Clone the repository to your local machine using:

```bash
git clone https://github.com/bhawesh2002/archive-org-script.git
cd archive-org-script
```
### Install Dependencies
Install the required dependencies using pip:
```bash
pip install -r requirements.txt
```
### Running the Script
After installing the dependencies, you can run the script with:
```bash
python main.py
```
    
## Usage/Examples

### 1. Run the script
```bash
python main.py
```

### 2. Entering the Archive.org Link
Upon running the script, you will be prompted to enter the Archive.org link associated with the identifier you wish to browse and download files from

### 3. Validating the Link and Downloading Metadata
The script will validate the provided link and proceed to download the necessary metadata for the specified identifier. If the link is invalid the script will ask you to re-enter the download link.

### 4. File Browser Interface
After downloading the metadata, the script will open a file browser interface. Use the following controls to navigate:
```
Arrow Keys: Navigate up and down through files and folders.

Spacebar: Select files/folders.

Enter: Confirm your selection and proceed to download.
```
Scroll down to view the complete controls

### 5. Selecting Files/Folders
When in File Browser navigate to the desired file or folder using the arrow keys. Press the `spacebar` to select it. You can select multiple items if needed. Selected items will be appended with a cyan asterisk (*)

### 6. Initiating Downloads
Once you have selected the files and folders you want to download, press `Enter` to start the download process. The script will begin downloading the selected items.

### 7. Monitoring Download Progress
As the script downloads each file, it will display progress updates, showing the status of each download. Only the file being downloaded will be displayed along with the download progress.

### 8. Download Completion
Upon completing the downloads, the script will display a "Download Successful" message.

### 9. Exiting the Program
Press any key to exit the program and return to the command prompt.

## File Browser Controls
### Navigation Controls: The following controls are used to navigate within the file browser
- `w`: Move the cursor up.
- `s`: Move the cursor down.
- `a`: Go back to the previous folder
- `d`: Open the highlighted folder
### Selection controls: The following controls are used to select files/folders
- `Space`: Select highlighted file/folder 
### Confirmation controls: The following controls are used to confirm the selection
- `Enter` - Confirm the selection and start downloading

### Help controls:The following controls are used to display the help message
- `h` - Toggle the help message

### Exit controls: The following controls are used to exit the file browser
- `Esc` - Exit the file browser

## Contributing

We welcome contributions to improve the project! Here's how you can get started:

- Fork the repository and clone it to your local machine.
- Create a new branch (`git checkout -b feature-branch`).
- Make your changes and commit them (`git commit -am 'Add new feature'`).
- Push to the branch (`git push origin feature-branch`).
- Open a pull request and describe your changes.

## License
This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License - see the LICENSE file for details.

## Acknowledgements

### Archive.org
We gratefully acknowledge Archive.org for providing extensive archival resources and APIs that have been instrumental in the development of this project. Archive.org's commitment to preserving digital content and making it universally accessible has greatly enriched the capabilities of our script. Their platform has facilitated seamless access to historical and cultural materials, enabling users to explore and utilize vast collections of data and media.

## Changelog
See the [CHANGELOG.md](https://github.com/bhawesh2002/archive-org-script/blob/main/CHANGELOG.md) file for details on changes and updates.

### Latest Release : [0.1.0] - 2024-06-17