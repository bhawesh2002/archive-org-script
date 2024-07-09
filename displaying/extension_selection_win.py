#v0.3.0:
#Minor Feature: Implement extension_selection_win function to display the extension selection window

import copy
import curses
from basic_function.extract_extensions import extract_extensions
from colors.app_colors import init_colors

def extension_selection_win(parent_win,filetree):
    """
    Displays the extension selection window.
    Args:
        parent_win (curses window): The parent window.
        filetree (dict): The filetree dictionary.
    Returns:
        list: The list of selected extensions."""
    try:
        init_colors()
        
        #extract the extensions from the filetree
        extensions = []
        extract_extensions(filetree=filetree, extensions = extensions) #extract the extensions from the filetree
        #calculate the height, width of the advance selection window
        ext_sel_win_wt = parent_win.getmaxyx()[1]- 70 #width of the advance selection window with padding of 10 relative to the parent window
        ext_sel_win_ht = parent_win.getmaxyx()[0] -3 #height of the advance selection window with padding of 2 relative to the parent window
        # print("ext_sel_win_ht: ", ext_sel_win_ht)
        #calculate the y,x position of the advance selection window
        ext_sel_win_y = 2 #y position of the advance selection window
        ext_sel_win_x = (parent_win.getmaxyx()[1] - ext_sel_win_wt) // 2 #x position of the advance selection window

        #create the advance selection window centered relative to the parent window
        ext_sel_win = curses.newwin(ext_sel_win_ht, ext_sel_win_wt, ext_sel_win_y, ext_sel_win_x)

        #draw the border
        ext_sel_win.border()

        #display the title
        ext_sel_win.addstr(0, (ext_sel_win_wt - len(" Select Extensions ")) // 2, " Select Extensions ", curses.color_pair(5) | curses.A_BOLD)
        #display the instructions
        ext_sel_win.addstr(1, 2, "Use 'a' and 'd' to navigate | 'spacebar' to select the extensions", curses.color_pair(7) | curses.A_BOLD)
        ext_sel_win.addstr(ext_sel_win_ht-2, (ext_sel_win_wt //2) - (len("Press 'Enter' to confirm selection")), "Press 'ENTER' to confirm selection", curses.color_pair(5) | curses.A_BOLD)
        ext_sel_win.addstr(ext_sel_win_ht-2, (ext_sel_win_wt //2) + 2, "||")
        ext_sel_win.addstr(ext_sel_win_ht-2, (ext_sel_win_wt //2)+ 6, "Press 'BACKSPACE' to go back", curses.color_pair(3) | curses.A_BOLD)
        ext_sel_win.refresh()
        curr_ext = 0
        selected_exts = []
        scroll_offset = 0
        while True:
            extension_win(ext_sel_win,extensions,curr_ext=curr_ext,selected_exts=selected_exts,scroll_offset=scroll_offset)
            key = ext_sel_win.getch()
            """
            Controls:
                - 'd' to navigate to the next extension
                - 'a' to navigate to the previous extension
                - 'spacebar' to select the extension
                - '0' to deselect all extensions
                - '1' to select all extensions
                - '2' or 'BACKSPACE' to quit extension selection window
                - 'Enter' to return the selected extensions
                - 'Esc' to exit the program
            """
            if key == ord('d'):
                curr_ext = (curr_ext + 1) % len(extensions)
            if key == ord('a'):
                curr_ext = (curr_ext - 1) % len(extensions)
            if key == ord(' '):
                if extensions[curr_ext] in selected_exts:
                    selected_exts.remove(extensions[curr_ext])
                else:
                    selected_exts.append(extensions[curr_ext])
            if key == ord('0'): # '0' to deselect all extensions
                selected_exts = []
            if key == ord('1'): # '1' to select all extensions
                selected_exts = copy.deepcopy(extensions)
            if key == ord('2') or key == ord('\b'): # '2' to toggle extension selection window
                ext_sel_win.clear()
                ext_sel_win.refresh()   
                break         
            if key == ord('\n'): # '\n' for 'Enter' key in ASCII
                return selected_exts
            if key == ord('\033'): # '\033' for 'Esc' key in ASCII
                exit(0) #exit the program

    except Exception as e:
        raise e

def extension_win(parent_win,extensions,curr_ext,selected_exts,scroll_offset=0):
    try:    
        init_colors()
        # Get the dimensions of the parent window
        parent_ht, parent_wt = parent_win.getmaxyx()

        # Calculate the dimensions of the new window
        ext_win_ht = parent_ht - 4
        ext_win_wt = parent_wt - 4

        # Create the new window centered inside the parent window
        ext_win = curses.newwin(ext_win_ht, ext_win_wt, 4, 35+2)

        ext_win.border()
        ext_win.refresh()
        x,y = 1,0   
        for idx,ext in enumerate(extensions):
            if x + len(ext) + 4 > ext_win_wt - 2:
                y = y + 1
                x = 1
            if y > ext_win_ht-1:
                continue
            if idx == curr_ext:
                ext_win.attron(curses.A_REVERSE)
                ext_win.addstr(y, x, ext)
                ext_win.attroff(curses.A_REVERSE)
                if ext in selected_exts:
                    ext_win.addstr(y, x-1, "*",curses.color_pair(8) | curses.A_BOLD)
                x = x + len(ext) + 4
            elif ext in selected_exts:
                ext_win.addstr(y, x-1, "*",curses.color_pair(8) | curses.A_BOLD)
                ext_win.addstr(y, x, ext,curses.color_pair(8) | curses.A_BOLD)
                x = x + len(ext) + 4
            else:
                ext_win.addstr(y, x, ext)
                x = x + len(ext) + 4
            
            ext_win.refresh()
    except Exception as e:
        raise e