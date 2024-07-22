# v0.3.4
# Bug Fix: Modify the display_help function to take a parent window as an argument
#          Calculate the ddimensions of the help window based on HELP_TEXT
#          Quit the help window when the user presses any key        

#Old Code:
#v0.3.3:
#BugFix: Fix the issue with the display_help function not displaying the help text

import curses
from colors.app_colors import init_colors
from constants import HELP_TEXT

def display_help(parent_win):
    try: 
        init_colors() #initialize the color pairs

        #Calculate the dimensions of the help window
        help_win_wt = len(max(HELP_TEXT, key=len)) + 4 #width of the help window (length of the longest line in the help text + 4 for padding on both sides)
        help_win_ht = len(HELP_TEXT) + 4 #height of the help window
        
        #Calculate the x and y position of the help window
        parent_win_wt = parent_win.getmaxyx()[1] #get the width of the main window
        x_pos=parent_win_wt - (help_win_wt + 2) #x position of the help window
        y_pos=1

        #create a new window for displaying help
        help_win = curses.newwin(help_win_ht, help_win_wt, y_pos, x_pos) #create a new window for displaying help
        help_win.refresh()
        
        #draw the border
        help_win.border()

        #display the HELP message
        help_win.addstr(0, (help_win_wt - len(" HELP "))//2, " HELP ", curses.color_pair(5) | curses.A_BOLD)
        
        #display help contents
        for i,line in enumerate(HELP_TEXT):
            help_win.addstr(y_pos + i, 2, line, curses.color_pair(5) | curses.A_BOLD)

        #display the PRESS ANY KEY TO CONTINUE... message
        help_win.addstr(y_pos + len(HELP_TEXT),2, (help_win_wt - 4) * "-", curses.color_pair(5) | curses.A_BOLD)
        help_win.addstr(y_pos + len(HELP_TEXT) + 1,(help_win_wt//2- (len("PRESS ANY KEY TO CONTINUE...")//2)), "PRESS ANY KEY TO CONTINUE...", curses.color_pair(5) | curses.A_BOLD)
        
        help_win.refresh()

        #wait for the user to press a key
        key = help_win.getch()
        if key == ord('\033'): #check if the key pressed is 'Esc'
            help_win.clear()
            help_win.refresh()
            exit(0) #exit the program
        else:
            help_win.clear() #clear the help window
            help_win.refresh() #refresh the help window
        
    except Exception as e:
        raise e