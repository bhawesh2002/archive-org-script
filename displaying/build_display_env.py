import curses
from colors.app_colors import init_colors #import color pairs
from constants import CONTROLS

def file_browser(stdscr):
    curses.curs_set(0) #hide the cursor
    init_colors() 
    stdscr.clear()
    height, width = stdscr.getmaxyx() #get the height and width of the terminal
    x = (width - len("File Browser"))//2
    y = height -1
    stdscr.addstr(0 , x, "File Browser", curses.color_pair(6) | curses.A_BOLD) #display the program name at the top center
    stdscr.addstr(y, 0, CONTROLS, curses.color_pair(4)) #display the controls at the bottom of the screen
