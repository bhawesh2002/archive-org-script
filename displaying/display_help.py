import curses
from colors.app_colors import init_colors
from constants import HELP_TEXT

def display_help(stdscr):
    try: 
        stdscr.addstr(0,0,"Help\n", curses.color_pair(5) | curses.A_BOLD)
        stdscr.addstr(1,0,"----------------------\n", curses.color_pair(5) | curses.A_BOLD)
        y = stdscr.getyx()[0] #get the position of cursor
        for i,line in enumerate(HELP_TEXT):
            stdscr.addstr(y + i, 0, line, curses.color_pair(5))
    except Exception as e:
        raise e