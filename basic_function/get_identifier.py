import curses
import requests #for making HTTP requests

# Get the identifier from the download link
def get_identifier(stdscr):
    download_link = get_link(stdscr)
    identifier = download_link.split("/")[-1] #extract the identifier from the link
    return identifier

# return a valid dwonload link
def get_link(stdscr):
    while True:
        link = user_input(stdscr) #get the link from the user
        download_link = construct_download_link(link) #construct the link
        
        if validate_link(download_link):
            stdscr.refresh()
            break
        else:
            stdscr.addstr(2, 0, "Error: Input not valid", curses.color_pair(3) | curses.A_BOLD) #display error message
            stdscr.refresh()

    return download_link

def user_input(stdscr):
    stdscr.addstr(1,0,"Paste the link here: ", curses.color_pair(4)) # Prompt the user to enter a link
    stdscr.refresh()

    curses.echo() # Enable echoing of characters for the user to see the input
    curses.curs_set(1) # Show the cursor
    stdscr.keypad(True) # Enable keypad mode to recognize arrow keys

    # Get the link from the user
    link = stdscr.getstr().decode('utf-8').strip()

    curses.noecho() # Disable echoing of characters
    curses.curs_set(0) # Hide the cursor
    stdscr.keypad(False) # Disable keypad mode
    stdscr.refresh()
    return link

# Checks if the link follows the format of an archive.org download directory link.
def construct_download_link(link):
    # If the link is directory identifier only, add the necessary prefix
    if "https://archive.org/" not in link:
        link = f"https://archive.org/download/{link}"
        return link
    # If the link is a details page, replace the details with download
    elif "https://archive.org/details/" in link:
        link = link.replace("https://archive.org/details/", "https://archive.org/download/")
        return link
    # If the link is a download link, return the link
    elif "https://archive.org/download/" in link:
        return link

# Checks if the link exists or not
def validate_link(download_link):
    try:
        response = requests.head(download_link) #send a HEAD request to the link for validating link
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError as e:
        raise e