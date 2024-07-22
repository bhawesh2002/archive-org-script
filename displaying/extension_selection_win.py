# Old
# v0.3.0:
#Minor Feature: Implement extension_selection_win function to display the extension selection window

#v0.3.1:
#Bug Fix: Fix the issue with the extension selection window not displaying the extensions correctly
#Bug Fix: Fix calculations responsible for centering the extension selection window
#Patch: Allow the user to navigate the extension selection window using the 'w', 's', 'a', 'd' keys

import copy
import curses
from basic_function.extract_extensions import extract_extensions
from colors.app_colors import init_colors
from constants import EXTENSION_CONFIRMATION_MESSAGE, EXTENSION_SEL_CONTROLS

#v0.3.3:
#BugFix: Pass extensions to the extension_selection_win as parameter to improve performance.
def extension_selection_win(parent_win,extensions,stdscr):
    """
    Displays the extension selection window.
    Is responsible for interacting with the user to select the extensions.
    Args:
        parent_win (curses window): The parent window.
        filetree (dict): The filetree dictionary.
        stdscr (curses window): The standard screen window.
    Returns:
        list: The list of selected extensions."""
    try:
        init_colors()
        
        #calculate the extensions per row/no of columnss
        longest_ext_len = len(max(extensions,key=len)) #find the length of longest extension
        value = ((parent_win.getmaxyx()[1]//(longest_ext_len +  4)))if ((parent_win.getmaxyx()[1]//(longest_ext_len +  4))) > 1 else 2 #calculate value based on longest_ext_len, minimum value should be 2
        exts_per_row = value if ((longest_ext_len + 4) * 7) > parent_win.getmaxyx()[1] else 7  #set the no of columns/extensions per row to value if longest_ext_len exceeds width of parent win else stick to the default value of 7

        #calculate the number of rows
        no_of_rows= 0
        for i in range(len(extensions)):
            if i%exts_per_row == 0:
                no_of_rows = no_of_rows + 1
        #calculate the height, width of the extension selection window
        ext_sel_win_wt = (longest_ext_len + 4) * exts_per_row + 2 #length of the longest extension + 4 padding multiplied by the number of extensions per row plus 2 for spacing
        ext_sel_win_ht = (2 + no_of_rows + 1) if (parent_win.getmaxyx()[0] > (no_of_rows + 3)) else (parent_win.getmaxyx()[0] - 2) #resize the extension selection window if the height of the parent window is less than the number of rows
        #calculate the y,x position of the extension selection window
        ext_sel_win_y = 1 #y position of the extension selection window
        ext_sel_win_x = (parent_win.getmaxyx()[1] - ext_sel_win_wt)//2 #x position of the extension selection window

        #create the extension selection window centered relative to the parent window
        ext_sel_win = curses.newwin(ext_sel_win_ht, ext_sel_win_wt, ext_sel_win_y, ext_sel_win_x)

        #draw the border
        ext_sel_win.border()

        #display the title
        ext_sel_win.addstr(0, (ext_sel_win_wt - len(" Select Extensions ")) // 2, " Select Extensions ", curses.color_pair(5) | curses.A_BOLD)
        #display the instructions
        ext_sel_win.addstr(1, (ext_sel_win_wt - len(EXTENSION_SEL_CONTROLS))//2, EXTENSION_SEL_CONTROLS, curses.color_pair(7) | curses.A_BOLD)
        ext_sel_win.addstr(ext_sel_win_ht-1, (ext_sel_win_wt //2) - (len(EXTENSION_CONFIRMATION_MESSAGE.split(',')[0])), EXTENSION_CONFIRMATION_MESSAGE.split(',')[0], curses.color_pair(5) | curses.A_BOLD)
        ext_sel_win.addstr(ext_sel_win_ht-1, (ext_sel_win_wt //2) + 1, "||")
        ext_sel_win.addstr(ext_sel_win_ht-1, (ext_sel_win_wt //2)+ 4, EXTENSION_CONFIRMATION_MESSAGE.split(',')[1], curses.color_pair(3) | curses.A_BOLD)
        ext_sel_win.refresh()
         
        curr_ext = 0 #track the current extension
        selected_exts = [] #track the selected extensions
        scroll_offset = 0
        while True:
            extension_win(ext_sel_win,extensions,curr_ext=curr_ext,selected_exts=selected_exts,exts_per_row=exts_per_row,scroll_offset=scroll_offset,stdscr=stdscr)
            key = ext_sel_win.getch()
            """
            Controls:
                - 'w' to navigate up
                - 's' to navigate down
                - 'a' to navigate to the previous extension
                - 'd' to navigate to the next extension
                - 'spacebar' to select the extension
                - '0' to deselect all extensions
                - '1' to select all extensions
                - '2' or 'BACKSPACE' to quit extension selection window
                - 'Enter' to return the selected extensions
                - 'Esc' to exit the program
            """
            if key == ord('w'):
                if curr_ext- exts_per_row <0:
                    pass
                else:
                    curr_ext = curr_ext- exts_per_row
            if key == ord('s'):
                if curr_ext + exts_per_row >= len(extensions):
                    pass
                else:
                    curr_ext = curr_ext+ exts_per_row
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
                ext_sel_win.clear()
                ext_sel_win.refresh()
                return selected_exts
            if key == ord('\033'): # '\033' for 'Esc' key in ASCII
                exit(0) #exit the program

    except Exception as e:
        raise e

def extension_win(parent_win,extensions,curr_ext,selected_exts,scroll_offset,stdscr,exts_per_row = 7):
    """
    Function that displays the extensions in the extension selection window. 
    Is responsible for layout and visual representation of the extensions.
    Args:
        parent_win (curses window): The parent window.
        extensions (list): The list of extensions.
        curr_ext (int): The index of the current extension.
        selected_exts (list): The list of selected extensions.
        scroll_offset (int): The scroll offset.
        stdscr (curses window): The standard screen window.
        exts_per_row (int): The number of extensions per row.
    Returns:
        None"""
    try:    
        init_colors()
        # Get the dimensions of the parent window
        parent_ht, parent_wt = parent_win.getmaxyx()

        # Calculate the width, height and position of the new window
        ext_win_ht = parent_ht - 3 # minus 3 for the title, controls and confirmation message
        ext_win_wt = parent_wt - 4
        y_pos = 3
        x_pos = (stdscr.getmaxyx()[1]-parent_wt)//2+2 #x_pos relative to stdscr and parent window required to center the window 
        # Create the new window centered inside the parent window
        ext_win = curses.newwin(ext_win_ht, ext_win_wt, y_pos, x_pos)
        ext_win.refresh()

        x,y = 1,0 #track the x,y position of the cursor
        spacing= len(max(extensions,key=len)) + 4 #spacing between the extensions 4 more than the length of the longest extension
        for idx,ext in enumerate(extensions):
            if idx > 0 and idx % exts_per_row == 0: #move to the next row and reset x position
                y = y + 1
                x = 1
            if y > ext_win_ht-1: #if the y position exceeds the height of the window, continue
                continue
            if idx == curr_ext: #highlight the current extension
                ext_win.attron(curses.A_REVERSE)
                ext_win.addstr(y, x, ext)
                ext_win.attroff(curses.A_REVERSE)
                if ext in selected_exts: #if the extension is selected and highlighted, display a '*' before the extension
                    ext_win.addstr(y, x-1, "*",curses.color_pair(8) | curses.A_BOLD)
            elif ext in selected_exts: #if the extension is selected, display a '*' before the extension
                ext_win.addstr(y, x-1, "*",curses.color_pair(8) | curses.A_BOLD)
                ext_win.addstr(y, x, ext,curses.color_pair(8) | curses.A_BOLD)
            else: #display the extension
                ext_win.addstr(y, x, ext)
            
            x = x + spacing #increment the x position by the spacing

            ext_win.refresh()
    
    except Exception as e:
        raise e