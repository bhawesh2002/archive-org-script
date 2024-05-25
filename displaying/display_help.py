import curses
from colors.app_colors import init_colors
from constants import HELP_TEXT

def display_help(stdscr):
    stdscr.addstr(0 , 0, "Help", curses.color_pair(6) | curses.A_BOLD)
    for i, line in enumerate(HELP_TEXT):
        stdscr.addstr(0 + i, 0, line, curses.color_pair(5))
    return