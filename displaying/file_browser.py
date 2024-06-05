import curses
from colors.app_colors import init_colors #import color pairs
from constants import CONTROLS
from displaying.display_help import display_help

def file_browser(stdscr, identifier_name,filetree, selected_files):
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
        current_opt=0 #initialize current option to 0
        while True:
            browser_window(main_win,filetree,current_opt,selected_files) #create the browser window
            b_key = main_win.getch() #get the key pressed
            main_win.refresh()
            if b_key == ord('h'):
                help_required = not help_required #toggle the help message
                display_help(main_ht - 2, (main_wt)//3, 1, main_wt - ((main_wt//3) + 2),help_required) #display the help message
            if b_key == ord('s'): #if 's' is pressed, move to the next option
                current_opt += 1
            if b_key == ord('w') and current_opt > 0: #if 'w' is pressed, move to the previous option
                current_opt -= 1
            if b_key == ord('\033'):
                exit(0) #exit the file browser and the program
    except Exception as e:
        raise e

def browser_window(main_win,filetree,current_opt,selected_files):
    try:
        main_ht, main_wt = main_win.getmaxyx() #get the height and width of the window
        browser_win = curses.newwin(main_ht - 2, main_wt-5, 1, 2) #create a new window for displaying help
        height, width = browser_win.getmaxyx()
        max_visible_lines = height-1 #max number of items that can be displayed on the screen
        for idx,(key,value) in enumerate(filetree.items()):
            if idx > max_visible_lines:
                continue
            if idx == current_opt:
                browser_win.attron(curses.A_REVERSE)
                browser_win.addstr(idx,0,key)
                browser_win.attroff(curses.A_REVERSE)
            else:
                browser_win.addstr(idx,0,key)
            if isinstance(value,dict): #if value is a dictionary object i.e a folder with nested folder/files
                browser_win.addstr(idx,len(key)+1,"-->")
            elif isinstance(value,str): #else if child_folder is a string(i.e, size of file) which is associated with key which is name of file
                browser_win.addstr(idx,len(key)+1,f"({value})")
        browser_win.refresh()
    except Exception as e:
        raise e