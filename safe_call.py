import curses #for creating terminal GUI
from error_messages.error_messages import keyboard_interrupt_msg #import keyboard interrupt message

def safe_call(stdscr,func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except KeyboardInterrupt as e:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        x = (width - len(keyboard_interrupt_msg))//2
        stdscr.addstr(height//2, x, keyboard_interrupt_msg, curses.color_pair(3) | curses.A_BOLD)
        stdscr.refresh()
    except Exception as e:
        stdscr.clear() 
        height, width = stdscr.getmaxyx()
        x = (width -len(str(e)))//2 #center the error message
        stdscr.addstr(height//2,x, f"{e}", curses.color_pair(2) | curses.A_BOLD) #display the error message
        stdscr.refresh