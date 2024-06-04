import curses
from colors.app_colors import init_colors #import color pairs
from constants import CONTROLS
from displaying.display_help import display_help

def file_browser(stdscr):
    try: 
        curses.curs_set(0) #hide the cursor
        init_colors() 
        height,width = stdscr.getmaxyx()
        main_win = curses.newwin(height,width , 0, 0) #create a new window relative to the stdandard screen(stdscr)
        main_win.border() #draw a border around the window
        main_ht, main_wt = main_win.getmaxyx() #get the height and width of the window
        main_win.addstr(0,(width - len("  File Browser  ")) // 2,"  File Browser  ", curses.color_pair(4) | curses.A_BOLD) #display the title of the window
        main_win.addstr(main_ht-1, 1 , f" {CONTROLS} ", curses.color_pair(5) | curses.A_BOLD) #display the controls
        main_win.refresh() #refresh the window
        help_required = False #initialize the help status
        while True:
            b_key = main_win.getch() #get the key pressed
            main_win.refresh()
            if b_key == ord('h'):
                help_required = not help_required #toggle the help message
                display_help(main_ht - 2, (main_wt)//3, 1, main_wt - ((main_wt//3) + 2),help_required) #display the help message
            if b_key == ord('\033'):
                break #exit the file browser
    except Exception as e:
        raise e

