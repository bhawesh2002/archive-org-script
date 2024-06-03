import curses
from colors.app_colors import init_colors
from constants import HELP_TEXT

def display_help(help_win_ht, help_win_wt, y,x):
    try: 
        init_colors()
        help_win = curses.newwin(help_win_ht, help_win_wt, y, x) #create a new window for displaying help

        #display help contents
        for i,line in enumerate(HELP_TEXT):
            help_win.addstr(y + i, 0, f"   {line}", curses.color_pair(5))
        #draw the border
        help_win.border()
        #display the help message
        help_win.addstr(0, (help_win_wt - len("  Help  "))//2, "  Help  ", curses.color_pair(5) | curses.A_BOLD)
        help_win.refresh()
    except Exception as e:
        raise e