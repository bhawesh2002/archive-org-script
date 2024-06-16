import curses
import os
from basic_function.load_download_links import load_download_links
from colors.app_colors import init_colors
from constants import DOWNLOAD_FOLDER_PATH
from downloading.download_file import download_file

def create_content_folder(identifier):
    content_folder_path = os.path.join(DOWNLOAD_FOLDER_PATH, identifier, "content")
    os.makedirs(content_folder_path, exist_ok=True)
    return content_folder_path

def downloader(stdscr,identifier):
    try:
        curses.curs_set(0) #hide the cursor
        init_colors() #initialize the colors
        height,width = stdscr.getmaxyx() #get the height and width of the terminal
        downloader_win = curses.newwin(height,width,0,0) #create a new window
        downloader_win.border() #draw a border around the window
        downloader_win.addstr(0,width//2 - len(" Downloader ")," Downloader ",curses.color_pair(4) | curses.A_BOLD) #display the title of the window
        downloader_win.refresh() #refresh the window
        links = load_download_links(identifier) #load the download links
        content_folder_path = create_content_folder(identifier)
        for link in links:
            download_file(url=link,downloader_win=downloader_win,download_path=content_folder_path)
        downloader_win.addstr(height//2,(width-len("Download Complete"))//2,"Download Complete", curses.color_pair(5) | curses.A_BOLD) #display the download complete message
        downloader_win.addstr((height//2)+1,(width-len("Press any Key to EXIT"))//2,"Press any Key to EXIT", curses.color_pair(8)) #display the download complete message
        downloader_win.getch()
    except Exception as e:
        raise e