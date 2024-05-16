import curses

#converts bytes to MBs
def convert_bytes_to_mb(size):
    """Convert bytes to megabytes."""
    return size / (1024 * 1024)

#Prints the structure in a tree-like format using color and styling.
def display_directory_struct(stdscr, directory_dict, selected_files, current_option, identifier_name, current_path=[], indent_level=0, scroll_offset=0, visible_lines=0):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    for idx, (option, child_folder) in enumerate(directory_dict.items()):
        if idx < scroll_offset or idx >= scroll_offset + visible_lines:
            continue

        x = w//2 - len(option)//2
        y = idx - scroll_offset + 1

        if y < 0 or y >= h:
            continue

        if x < 0 or x + len(option) + indent_level * 2 >= w:
            continue
    
        if option in selected_files or '/'.join(current_path + [option]) in selected_files:
            if idx == current_option:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x + indent_level * 2, "*", curses.color_pair(3))
                stdscr.addstr(y, x + indent_level * 2 + 1, option)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x + indent_level * 2, "*", curses.color_pair(3))
                stdscr.addstr(y, (x + indent_level * 2) + 1, option)
        elif idx == current_option:
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(y, x + indent_level * 2, option)
            stdscr.attroff(curses.A_REVERSE)
        else:
            stdscr.addstr(y, x + indent_level * 2, option)

        if isinstance(child_folder, dict): #if child_folder is a dictionary object i.e a folder with nested folder/files
            stdscr.addstr(y, x + (len(option) + indent_level * 2) +1, " ->")   #then display a arrow "->"
        elif isinstance(child_folder, str): #else if child_folder is a string(i.e, size of file) which is associated with child_folder which is name of file
            try:
                file_size_mb = convert_bytes_to_mb(int(child_folder))
                stdscr.addstr(y, x + (len(option) + indent_level * 2) +1, f" ({file_size_mb:.2f} MB)")
            except ValueError:
                stdscr.addstr(y, x + (len(option) + indent_level * 2) +1, " Size: Unknown")
    
    dir_name_label = "Directory Name:"
    stdscr.addstr(h - 2, 0, dir_name_label, curses.color_pair(3))
    stdscr.addstr(h - 2, 16, identifier_name)
    footer_text = "Navigation: Up/Down to navigate, Right to enter directory, Left to go back, Space to select/deselect, q to quit"
    stdscr.addstr(h - 1, 0, footer_text, curses.color_pair(4))
    stdscr.refresh()
