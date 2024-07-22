import curses
from basic_function.construct_download_links import construct_download_links
from basic_function.extract_extensions import extract_extensions
from colors.app_colors import init_colors #import color pairs
from constants import CONTROLS
from displaying.extension_selection_win import extension_selection_win
from displaying.display_help import display_help
from browsing.browser import browser
from selection_deselection.select_extensions import select_extensions
from selection_deselection.select_or_deselect_all import deselect_all, select_all
from selection_deselection.toggle_selection import toggle_selection
def file_browser(stdscr, identifier,filetree):
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
        #v0.3.3:
        #BugFix: Extract the extensions from the filetree in the file_browser
        extensions = []
        extensions = extract_extensions(filetree=filetree,extensions=extensions) #extract the extensions from the filetree

        directory = filetree #set directory equal to the filetree
        current_folder = "" #for tracking the current folder
        current_path = [] #track the current path
        selected_files = {} #track the selected files
        current_opt = 0
        scroll_offset = 0
        visible_lines = (main_ht - 5) #number of lines that can be displayed on the screen
        #note: main_ht - 5 is a constant value that is used to calculate the number of lines that can be displayed on the screen
        #      it is calculated by subtracting the height of the title, border and controls from the height of the main window
        #      Do Not Change this value as it is calculated and changing might cause display isssues
        while True:
            main_win.addstr(1,2,(main_wt - 5) * " ",curses.color_pair(5) | curses.A_BOLD) #clear the previous folder name
            if directory == filetree:
                main_win.addstr(1,2,"Root(/)", curses.color_pair(5) | curses.A_BOLD) #display the current folder name
                selected_files_copy = selected_files #create a copy of the selected files
            else:
                main_win.addstr(1,2,current_folder, curses.color_pair(5) | curses.A_BOLD) #display the current folder name
                selected_files_copy = selected_files #reset the selected files
                for folder in current_path: #traverse the current path to go inside folders
                    for key in selected_files_copy: #traverse the files inside the selecte_files_copy
                        if key == folder: #check if the key in selelcted_files_copy is a folder in the current path
                            selected_files_copy = selected_files_copy[folder] #set the selected_files_copy to the files in the folder in the current path
            browser(main_win,directory=directory,current_opt=current_opt, selected_files=selected_files_copy,scroll_offset= scroll_offset) #create the browser window
            b_key = main_win.getch() #get the key pressed
            main_win.refresh()
            #Control handling
            """
            Control handling:
            The following controls are used to navigate, select, confirm and exit the file browser
            Navigation controls: 's', 'w', 'd', 'a'
            Selection controls: 'Space'
            Confirmation controls: 'Enter'
            Help controls: 'h'
            Exit controls: 'Esc'"""
            #Navigation controls
            """
            Navigation controls:
            The following controls are used to navigate the file browser
               's' - move the cursor down
               'w' - move the cursor up
               'd' - open the selected folder
               'a' - go back to the previous folder
            """
            if b_key == ord('s') and current_opt < len(directory) -1: #check if the key pressed is 's' and move the cursor down
                current_opt += 1
                if current_opt >= scroll_offset + visible_lines:
                    scroll_offset = current_opt - visible_lines + 1
            if b_key == ord('w') and current_opt > 0: #check if the key pressed is 'w' and move the cursor up
                current_opt -= 1
                if current_opt < scroll_offset:
                    scroll_offset = current_opt
            if b_key == ord('d'): #check if the key pressed is 'd' and open the selected folder
                if isinstance(directory[list(directory.keys())[current_opt]],dict):
                    current_folder = list(directory.keys())[current_opt] #get the name of the folder before changing the directory
                    current_path.append(current_folder) #add the folder to the current path
                    directory = directory[current_folder] #change the directory to the selected folder
                    #reset the values
                    current_opt = 0
                    scroll_offset = 0
            if b_key == ord('a'): #check if the key pressed is 'a' and go back to the previous folder
                if directory != filetree: #if the directory is not the filetree or the roo
                    indent_level = len(current_path) #get the current indent level
                    if indent_level >= 1: 
                        current_path.pop() #remove the last folder from the current path
                        directory = filetree #reset the directory to the filetree
                        if len(current_path) > 0: #check if the current path is not empty
                            current_folder = current_path[-1] #get the name of the folder before changing the directory
                        for folder in current_path: #traverse the current path to get the current directory
                            directory = directory[folder] #change the directory to the selected folder
                    #reset the values
                    current_opt = 0
                    scroll_offset = 0
            #Selection controls
            """ 
            Selection controls:
            The following controls are used to select files/folders
               'Space' - toggle the selection of the file/folder
               '0' - deselect all files
               '1' - select all files
               '2' - display the extension selection window
            """
            if b_key == ord(' '):
                highlighted_entity = list(directory.keys())[current_opt] #get the name of the highlighted entity
                #add the highlighted entity to the selected files
                selected_files = toggle_selection(selected_files,selection=highlighted_entity,current_path=current_path,directory=directory)
            
            #v0.2.3:
            #Patch: Implement select_all and deselect_all functions to select/deselect all files and folders in the filetree
            #Changes:
            #    - Call select_all function to select all files and folders when '1' is pressed
            #    - Call deselect_all function to deselect all files and folders when '0' is pressed
            
            if b_key == ord('0'): #check if the key pressed is '0' and deselect all files
                selected_files = deselect_all(selected_files) #deselect all files
            
            if b_key == ord('1'): #check if the key pressed is '1' and select all files
                selected_files = select_all(filetree) #select all files

            #v0.3.0:
            #Minor Feature: Call extension selection window to select files with specific extensions
            #Changes:
            #    - Call extension_selection_win function to open the extension selection window when '2' is pressed
            #    - Call select_extensions function to select files with the selected extensions
            if b_key == ord('2'): #check if the key pressed is '2' and open the advance selection window
                #v0.3.3:
                #BugFix: Correct the call to extension_selection_win function
                selected_extensions= extension_selection_win(parent_win=main_win,extensions=extensions,stdscr=stdscr)
                select_extensions(selected_files=selected_files,filetree=filetree,extensions=selected_extensions) #select the files with the selected extensions
            #Confirmation controls
            """
            Confirmation controls:
            The following controls are used to confirm the selection
               'Enter' - confirm the selection
            """
            if b_key == 10: #check if the key pressed is 'Enter' and confirm the selection
                construct_download_links(identifier,selected_files=selected_files)
                main_win.clear() #clear the window
                main_win.refresh()
                return #return to the main program
            #Help controls
            """
            Help controls:
            The following controls are used to display the help message
               'h' - toggle the help message
            """
            if b_key == ord('h'): #check if the key pressed is 'h' and toggle the help message
                display_help(parent_win=main_win) #display the help message
                main_win.refresh()
            #Exit controls
            """
            Exit controls:
            The following controls are used to exit the file browser
               'Esc' - exit the file browser
            """
            if b_key == ord('\033'): #check if the key pressed is 'Esc' and exit the file browser
                exit(0) #exit the file browser and the program
    except Exception as e:
        raise e