import os

PROGRAM_NAME = "Archive.org Dwonloader" #program name
DOWNLOAD_FOLDER_PATH = os.path.join(os.getcwd(), "Archives") #download folder path
CONTROLS = "Controls: [Arrow Keys] to navigate, [Space] to select, [Esc] to exit, 'h' to toggle help" #controls message
#help message
HELP_TEXT = [
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
        "h: Toggle help",
    ]