import curses
from colors.app_colors import init_colors #import color pairs
from constants import CONTROLS
from displaying.display_help import display_help
from displaying.browser import browser

def file_browser(stdscr, identifier,filetree, selected_files):
    try: 
        curses.curs_set(0) #hide the cursor
        init_colors() 
        height,width = stdscr.getmaxyx()
        main_win = curses.newwin(height,width , 0, 0) #create a new window relative to the stdandard screen(stdscr)
        main_win.border() #draw a border around the window
        main_ht, main_wt = main_win.getmaxyx() #get the height and width of the window
        title = f"  File Browser  ({identifier})  "
        main_win.addstr(0,(width - len(title)) // 2,title, curses.color_pair(4) | curses.A_BOLD) #display the title of the window
        main_win.addstr(main_ht-1, 1 , f" {CONTROLS} ", curses.color_pair(5) | curses.A_BOLD) #display the controls
        main_win.refresh() #refresh the window
        help_required = False #initialize the help status
        current_opt = 0
        scroll_offset = 0
        visible_lines = (main_ht - 5) #number of lines that can be displayed on the screen
        #note: main_ht - 4 is a constant value that is used to calculate the number of lines that can be displayed on the screen
        #      it is calculated by subtracting the height of the title, border and controls from the height of the main window
        #      Do Not Change this value as it is calculated and changing might cause display isssues
        while True:
            browser(main_win,directory=filetree,current_opt=current_opt, scroll_offset= scroll_offset) #create the browser window
            b_key = main_win.getch() #get the key pressed
            main_win.refresh()
            if b_key == ord('h'):
                help_required = not help_required #toggle the help message
                display_help(main_ht - 2, (main_wt)//3, 1, main_wt - ((main_wt//3) + 2),help_required) #display the help message
            if b_key == ord('s') and current_opt < len(filetree) -1:
                current_opt += 1
                if current_opt >= scroll_offset + visible_lines:
                    scroll_offset = current_opt - visible_lines + 1
            if b_key == ord('w') and current_opt > 0:
                current_opt -= 1
                if current_opt < scroll_offset:
                    scroll_offset = current_opt
            if b_key == ord('\033'):
                exit(0) #exit the file browser and the program
    except Exception as e:
        raise e