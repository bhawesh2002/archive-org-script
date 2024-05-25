import os

PROGRAM_NAME = "Archive.org Dwonloader" #program name
DOWNLOAD_FOLDER_PATH = os.path.join(os.getcwd(), "Archives") #download folder path
CONTROLS = "Controls: [Arrow Keys] to navigate, [Enter] to select, [Esc] to exit, F1 for help" #controls message
#help message
HELP_TEXT = [
        "Help",
        "----",
        "NAVIGATION",
        "Arrow keys: Navigate the file browser",
        "Enter: Open the selected item",
        "Space: Selete a file or folder",
        "Backspace: Go Back",
        "Esc: Quit the program",
        "s: Search for an item",
        "d: Download the selected item",
        "r: Refresh the display",
        "c: Clear the search results",
        "F1: Display this help message",
    ]