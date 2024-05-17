import curses
from colors.app_colors import init_colors

def welcome_message(stdscr):
    init_colors()
    stdscr.addstr("archive.org downloader", curses.color_pair(1) | curses.A_BOLD)
    stdscr.refresh()
    stdscr.getch()