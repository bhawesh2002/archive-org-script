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
from displaying.build_display_env import file_browser #import build_display_env to build the display environment
from displaying.display_help import display_help #import display_directory_struct to display the directory structure
# import os #for creating directories for dwonaloded files
# from basic_function.get_directory_identifier import get_directory_identifier #import get_directory_identifier
# from download_metadata.download_metadata import download_metadata_files #import download metadata
# from selection_deselection import toggle_item #for creation of TUI


def main(stdscr):
    curses.curs_set(0) #hide the cursor
    init_colors() 
    height, width = stdscr.getmaxyx() #get the height and width of the terminal
    
    #Program logic
    try:
        welcome_message(stdscr, PROGRAM_NAME) #display the welcome message        
        stdscr.addstr(PROGRAM_NAME, curses.color_pair(6) | curses.A_BOLD) #display the program name
        download_status = False #initialize the download status
        while not download_status:
            identifier = get_identifier(stdscr) #get the identifier
            download_status = download_metadata(stdscr, identifier, queue.Queue()) #download the metadata files
        parse_xml(identifier) #parse the xml file
        time.sleep(1) #wait for 1 second
        stdscr.clear() #clear the screen
        file_browser(stdscr) #open the file browser
        stdscr.refresh()
    #handle keyboard interrupt
    except KeyboardInterrupt as e:
        stdscr.clear() #clear the screen
        stdscr.addstr(height//2, (width - len(keyboard_interrupt_msg))//2, keyboard_interrupt_msg, curses.color_pair(3) | curses.A_BOLD) #display the exit message
        stdscr.refresh()
        time.sleep(0.5)
        exit(0)
    #handle other errors
    except Exception as e:
        stdscr.clear() 
        x = (width -len(str(e)))//2 #center the error message
        stdscr.addstr(height//2,x, f"{e}", curses.color_pair(2) | curses.A_BOLD) #display the error message
        # stdscr.addstr(height//2 + 1,(width - len(resize_window_err_msg))//2, f"{resize_window_err_msg}") #display the solution for the error
        stdscr.refresh()

    # Logic for the key press
    while True:
        key = stdscr.getch()
        stdscr.refresh()
        if key == ord('\033'):  # '\033' for 'Esc' key in ASCII
            exit(0)
        if key == ord('h'): # 'h' for help
            stdscr.clear()
            try:
                display_help(stdscr)
                stdscr.refresh()
            except Exception as e:
                stdscr.clear() 
                x = (width -len(str(e)))//2 #center the error message
                stdscr.addstr(height//2,x, f"{e}", curses.color_pair(2) | curses.A_BOLD) #display the error message
                stdscr.addstr(height//2 + 1,(width - len(resize_window_err_msg))//2, f"{resize_window_err_msg}") #display the solution for the error
                stdscr.refresh()
            while True:
                key = stdscr.getch()
                if key == ord('h'):# 'h' to toggle help
                    stdscr.clear()
                    file_browser(stdscr, PROGRAM_NAME)
                    stdscr.refresh()
                    break
                if key == ord('\033'):  # '\033' for 'Esc' key in ASCII
                    exit(0)
    # Ensure the script_downloads folder exists
    # script_downloads_path = "script_downloads"
    # os.makedirs(script_downloads_path, exist_ok=True)

    #validate the link
    # valid_link = False
    # while not valid_link:
    #     stdscr.refresh()
    #     download_link = get_ip(stdscr)
    #     if validate_link(download_link):
    #         valid_link = True
    #         stdscr.refresh()
    #         stdscr.addstr(2, 0, "Success: Valid archive.org download directory link entered.", curses.color_pair(5))
    #     else:
    #         stdscr.addstr(1, 0, " " * 100)
    #         stdscr.refresh()

    #         stdscr.addstr(2, 0, "Error: Invalid archive.org download directory link format.", curses.color_pair(2))
    #         stdscr.refresh()

    # #extract the indentifier from the link
    # directory_identifier = get_directory_identifier(download_link)
    # # Create a folder named after the identifier inside script_downloads
    # identifier_folder_path = os.path.join(script_downloads_path, directory_identifier)
    # os.makedirs(identifier_folder_path, exist_ok=True)
    # # Create a metadata folder inside identifier_folder_path
    # identifier_metadata_path = os.path.join(identifier_folder_path, 'metadata')
    # os.makedirs(identifier_metadata_path, exist_ok=True)

    # stdscr.addstr(3, 0, "Directory Name: ", curses.color_pair(3))
    # stdscr.addstr(directory_identifier)
    # stdscr.refresh()

    # # Download _files.xml and _meta.xml
    # download_metadata_files(directory_identifier, identifier_metadata_path)
    # # download_metadata_file(meta_url, f"{directory_identifier}_meta.xml", identifier_metadata_path)
    
    # # Parse the _files.xml after the file has been downloaded
    # files_xml = f"{identifier_metadata_path}/{directory_identifier}_files.xml"
    # parse_xml(files_xml)
    
    # #display the directory structure
    # current_option = 0
    # scroll_offset = 0
    # indent_level = 0
    # current_path = []
    # selected_files = [] #array containing the selected files

    # directory_struct_json = load_directory(f"{identifier_metadata_path}/{directory_identifier}_filetree.json")
    
    # while True:
    #     h, w = stdscr.getmaxyx()
    #     visible_lines = h - 4
    #     display_directory_struct(stdscr, directory_struct_json, selected_files, current_option, "identifier", current_path=current_path, indent_level=indent_level, scroll_offset=scroll_offset, visible_lines=visible_lines)

    #     key = stdscr.getch()

    #     if key == curses.KEY_UP and current_option > 0:
    #         current_option -= 1
    #         if current_option < scroll_offset:
    #             scroll_offset = current_option
    #     elif key == curses.KEY_DOWN and current_option < len(directory_struct_json) - 1:
    #         current_option += 1
    #         if current_option >= scroll_offset + visible_lines:
    #             scroll_offset = current_option - visible_lines + 1
    #     elif key == curses.KEY_RIGHT:
    #         selected_option = list(directory_struct_json.keys())[current_option]
    #         child_folder = directory_struct_json[selected_option]
    #         if isinstance(child_folder, dict):
    #             current_path.append(selected_option)
    #             indent_level += 1
    #             directory_struct_json = child_folder
    #             current_option = 0
    #             print("current_path:", current_path)
    #     elif key == curses.KEY_LEFT and indent_level > 0:
    #         indent_level -= 1
    #         current_path.pop()
    #         print("current_path:", current_path)
    #         directory_struct_json = load_directory(f"{identifier_metadata_path}/{directory_identifier}_filetree.json")
    #         for folder in current_path:
    #             directory_struct_json = directory_struct_json[folder]
    #         current_option = 0
        
    #     #save the file by adding it to selected_files list
    #     elif key == ord(' '):
    #         selected_option = list(directory_struct_json.keys())[current_option]
    #         toggle_item(selected_files, current_path, selected_option, directory_struct_json)

    #     elif key == curses.KEY_ENTER or key in [10, 13]:
    #         selected_option = list(directory_struct_json.keys())[current_option]
    #         child_folder = directory_struct_json[selected_option]
    #         if isinstance(child_folder, dict):
    #             current_path.append(selected_option)
    #             directory_struct_json = child_folder
    #             current_option = 0
    #     #Quit the program
    #     elif key == ord('q'):
    #         print("selected_files: ", selected_files)
    #         break
    #     #Enable Scrolling
    #     elif key == curses.KEY_PPAGE:
    #         if scroll_offset > 0:
    #             scroll_offset -= 1
    #     elif key == curses.KEY_NPAGE:
    #         if current_option < len(directory_struct_json) - 1:
    #             scroll_offset += 1

if __name__ == "__main__":
    curses.wrapper(main)
