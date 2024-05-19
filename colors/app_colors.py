import curses

# Initialize color pairs for curses
def init_colors():
    curses.start_color()
    curses.init_pair(0, curses.COLOR_BLACK, curses.COLOR_BLACK) # White
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK) # Blue
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK) # Red
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)# Yellow
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)# Green
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)# Cyan
    curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)# Blue
    curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_BLACK)# Magenta
    
