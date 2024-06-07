import curses #for creating TUI
import time #for utilizing delays
from constants import PROGRAM_NAME
from colors.app_colors import init_colors #import color pairs
from displaying.welcome_message import welcome_message #import welcome message
from error_messages.error_messages import resize_window_err_msg, keyboard_interrupt_msg #import error message
from basic_function.get_identifier import get_identifier #import get_identifier
from basic_function.download_metadata import download_metadata #import load_directory
import queue # for passing messages between threads
from parsing.parse_xml import parse_xml #import parse xml
from basic_function.load_filetree import load_filetree
from displaying.file_browser import file_browser #import build_display_env to build the display environment

def main(stdscr):
    curses.curs_set(0) #hide the cursor
    init_colors() 
    height, width = stdscr.getmaxyx() #get the height and width of the terminal
    
    #Program logic
    try:
        welcome_message(stdscr, PROGRAM_NAME) #display the welcome message        
        stdscr.addstr(PROGRAM_NAME, curses.color_pair(6) | curses.A_BOLD) #display the program name
        download_status = False #initialize the download status
        while not download_status: #loop until the download is successful
            identifier = get_identifier(stdscr) #get the identifier
            download_status = download_metadata(stdscr, identifier, queue.Queue()) #download the metadata files
        parse_xml(identifier) #parse the xml file
        filetree = load_filetree(identifier) #load the file tree
        time.sleep(1) #wait for 1 second
        stdscr.clear() #clear the screen
        stdscr.refresh() #refresh the screen
        file_browser(stdscr,identifier=identifier,filetree=filetree,selected_files="") #open the file browser
        stdscr.refresh() #refresh the screen
    #handle keyboard interrupt
    except KeyboardInterrupt as e:
        stdscr.clear() #clear the screen
        stdscr.addstr(height//2, (width - len(keyboard_interrupt_msg))//2, keyboard_interrupt_msg, curses.color_pair(3) | curses.A_BOLD) #display the exit message
        stdscr.refresh()
        time.sleep(0.5) #wait for 0.5 seconds
        exit(0)
    #handle other errors
    except Exception as e:
        stdscr.clear() 
        x = (width -len(str(e)))//2 #center the error message
        stdscr.addstr(height//2,x, f"{e}", curses.color_pair(2) | curses.A_BOLD) #display the error message
        stdscr.refresh()

    # Logic for the key press
    while True:
        key = stdscr.getch() #wait for the user to press a key
        stdscr.refresh()
        if key == ord('\033'):  # '\033' for 'Esc' key in ASCII
            exit(0) #exit the program
if __name__ == "__main__":
    curses.wrapper(main)
