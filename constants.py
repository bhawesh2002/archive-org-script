import os

PROGRAM_NAME = "Archive.org Dwonloader" #program name
DOWNLOAD_FOLDER_PATH = os.path.join(os.getcwd(), "Archives") #download folder path
CONTROLS = "Controls: [WSAD Keys] to navigate, [SPACEBAR] to select, [ENTER] to download, [H] to display help message, [ESC] to quit" #controls message
EXTENSION_SEL_CONTROLS = "[WSAD keys] to navigate, [SPACEBAR] to select the extension"
EXTENSION_CONFIRMATION_MESSAGE = "[ENTER] to confirm selection,[BACKSPACE] to go back"
#help message
HELP_TEXT = [
        "W: Navigate up",
        "S: Navigate down",
        "A: Go back to the previous folder",
        "D: Open the highlighted folder",
        "SPACEBAR: Select the highlighted file/folder",
        "NUM 1: Select all files/folders",
        "NUM 0: Deselect all files/folders",
        "NUM 2: Open Extensions Selection Menu",
        "ENTER: Download the selected files/folders",
        "H: Display help message",
        "ESC: Quit the program",
    ]