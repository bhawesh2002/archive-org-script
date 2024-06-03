import curses
from colors.app_colors import init_colors #import color pairs
from constants import CONTROLS

def file_browser(stdscr):
    try: 
        curses.curs_set(0) #hide the cursor
        init_colors() 
        height,width = stdscr.getmaxyx()
        browser_win = curses.newwin(height,width , 0, 0) #create a new window relative to the stdandard screen(stdscr)
        browser_win.border() #draw a border around the window
        browser_ht, browser_wt = browser_win.getmaxyx() #get the height and width of the window
        browser_win.addstr(0,(width - len("  File Browser  ")) // 2,"  File Browser  ", curses.color_pair(4) | curses.A_BOLD) #display the title of the window
        browser_win.addstr(browser_ht-1, 1 , f" {CONTROLS} ", curses.color_pair(5) | curses.A_BOLD) #display the controls
        browser_win.refresh() #refresh the window
    except Exception as e:
        raise e

