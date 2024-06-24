import curses

#fundtion that creates a browser which allows user to browse the files and folders
def browser(main_win,directory,current_opt,selected_files ,scroll_offset):
    """Function to create a browser window that allows the user to browse the files and folders
    Args:
        main_win : curses window object
            The main window object inside which the browser window will be displayed
        directory : dict
            A dictionary object containing the folder structure and files
        current_opt : int
            The index of the currently selected item in the browser window
        scroll_offset : int
            The scroll offset of the browser window      
    """
    try:
        main_ht, main_wt = main_win.getmaxyx() #get the height and width of the main window
        browser_win = curses.newwin(main_ht - 3, main_wt-5, 2, 2) #create a new window for displaying help
        height, width = browser_win.getmaxyx()
        # max_visible_lines = height - 1 #max number of items that can be displayed on the screen at a time
        for idx,(key,value) in enumerate(directory.items()):
            # if idx < scroll_offset or idx >= scroll_offset + max_visible_lines:
                # continue
            y = (idx - scroll_offset) + 1
            if y <= 0 or y > (height - 2):
                continue
            if idx == current_opt:
                browser_win.attron(curses.A_REVERSE)
                browser_win.addstr(y,2,key)
                browser_win.attroff(curses.A_REVERSE)
                if key in selected_files:
                    browser_win.addstr(y,1,"*",curses.color_pair(6) | curses.A_BOLD)
            elif key in selected_files:
                browser_win.addstr(y,1,"*",curses.color_pair(6) | curses.A_BOLD)
                browser_win.addstr(y,2,key)
            else:
                browser_win.addstr(y,2,key)
            if isinstance(value,dict): #if value is a dictionary object i.e a folder with nested folder/files
                browser_win.addstr(y,len(key)+2,"-->")
            elif isinstance(value,str): #else if child_folder is a string(i.e, size of file) which is associated with key which is name of file
                #0.1.1:
                #Info: Only displays the size of the file
                #Old Code: 
                #   browser_win.addstr(y,len(key)+2,f'({value})')
                
                #0.2.0:
                #Minor Feature: If the file is private then display a lock icon including the size
                size,private = value.split("|") #split the value into size and private
                browser_win.addstr(y,len(key)+2,f'({size})') #display the size of the file
                if private == 'true': 
                    #display LOCK in if the file is private
                    LOCK = '\U0001F512' #unicode character for lock
                    browser_win.addstr(y,len(key)+2+len(size)+2,LOCK)
        browser_win.refresh()
    except Exception as e:
        raise e