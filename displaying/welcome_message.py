import curses
from colors.app_colors import init_colors
import pyfiglet

def welcome_message(stdscr,welcome_message=""):
    init_colors()
    ascii_art = pyfiglet.figlet_format(welcome_message)
    stdscr.addstr(ascii_art, curses.color_pair(1) | curses.A_BOLD)
    stdscr.refresh()
    stdscr.getch()