import curses

# Prompts the user for input with the specified message and returns the stripped input.
def get_ip(stdscr):
    # Prompt the user to enter a link
    stdscr.addstr(1,0,"Paste the link here: ", curses.color_pair(4))
    stdscr.refresh()
    # Enable keypad mode to recognize arrow keys
    stdscr.keypad(True)
    return stdscr.getstr().decode('utf-8').strip()