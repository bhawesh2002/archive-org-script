import curses

# Prompts the user for input with the specified message and returns the stripped input.
def get_ip(stdscr):
    
    stdscr.addstr(1,0,"Paste the link here: ", curses.color_pair(3)) # Prompt the user to enter a link
    stdscr.refresh()

    curses.echo() # Enable echoing of characters for the user to see the input
    curses.curs_set(1) # Show the cursor
    stdscr.keypad(True) # Enable keypad mode to recognize arrow keys

    # Get the link from the user
    link = stdscr.getstr().decode('utf-8').strip()

    curses.noecho() # Disable echoing of characters
    curses.curs_set(0) # Hide the cursor
    stdscr.keypad(False) # Disable keypad mode

    return link # Return the link entered by the user