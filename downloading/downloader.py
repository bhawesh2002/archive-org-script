import curses
from colors.app_colors import init_colors

def downloader(stdscr,identifier,links):
    try:
        curses.curs_set(0) #hide the cursor
        init_colors() #initialize the colors
        height,width = stdscr.getmaxyx() #get the height and width of the terminal
        downloader_win = curses.newwin(height,width,0,0) #create a new window
        downloader_win.border() #draw a border around the window
        downloader_win.addstr(0,width//2 - len("Downloader"),"Downloader",curses.color_pair(7) | curses.A_BOLD) #display the title of the window
        downloader_win.refresh() #refresh the window
    except Exception as e:
        raise e