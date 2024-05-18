import curses
from colors.app_colors import init_colors
import pyfiglet #for creating ASCII art

def welcome_message(stdscr,welcome_message=""):
    try:    
        init_colors()
        ascii_art = pyfiglet.figlet_format(welcome_message)
        stdscr.addstr(ascii_art, curses.color_pair(1) | curses.A_BOLD)
        stdscr.refresh()
    except Exception as e:
        raise e #raise the exception to be caught in main.py