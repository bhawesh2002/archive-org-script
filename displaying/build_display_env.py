import curses
from colors.app_colors import init_colors #import color pairs
from constants import CONTROLS

def file_browser(stdscr, identifier):
    curses.curs_set(0) #hide the cursor
    init_colors() 
    stdscr.clear()
    height, width = stdscr.getmaxyx() #get the height and width of the terminal
    stdscr.addstr(0 , (width - len("File Browser"))//2, "File Browser", curses.color_pair(6) | curses.A_BOLD) #display the program name at the top center
    y = height -1
    stdscr.addstr(height -1, 0, CONTROLS, curses.color_pair(4)) #display the controls at the bottom of the screen
    