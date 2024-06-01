import curses
import requests #for making HTTP requests

# Get the identifier from the download link
def get_identifier(stdscr):
    user_ip = user_input(stdscr) #get the download link from the user
    identifier = user_ip.split("/")[-1] #extract the identifier from the link
    return identifier

#User input function to get the download link from the user
def user_input(stdscr):
    stdscr.addstr(1,0,"Paste the link here: ", curses.color_pair(4)) # Prompt the user to enter a link
    stdscr.refresh()

    stdscr.clrtoeol()# Clear the input area of any previous input
    
    curses.echo() # Enable echoing of characters for the user to see the input
    curses.curs_set(1) # Show the cursor
    stdscr.keypad(True) # Enable keypad mode to recognize arrow keys

    # Get the link from the user
    user_ip = stdscr.getstr().decode('utf-8').strip()

    curses.noecho() # Disable echoing of characters
    curses.curs_set(0) # Hide the cursor
    stdscr.keypad(False) # Disable keypad mode
    stdscr.refresh()

    return user_ip