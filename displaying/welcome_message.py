import curses
from colors.app_colors import init_colors
import time #for creating a delay
import pyfiglet #for creating ASCII art

def welcome_message(stdscr,welcome_message=""):
    try:    
        init_colors()
        ascii_art = pyfiglet.figlet_format(welcome_message)
        height, width = stdscr.getmaxyx()
        # Calculate the position to center the text
        start_y = height // 2 - len(ascii_art.splitlines()) // 2
        start_x = width // 2 - max(len(line) for line in ascii_art.splitlines()) // 2

         # Display the ASCII art
        for i, line in enumerate(ascii_art.splitlines()):
            stdscr.addstr(start_y + i, start_x, line, curses.color_pair(4)| curses.A_BOLD)
        
        stdscr.refresh()
        time.sleep(0.3) #delay for 0.3 seconds
        stdscr.clear()
        stdscr.refresh()
    except Exception as e:
        raise e #raise the exception to be caught in main.py