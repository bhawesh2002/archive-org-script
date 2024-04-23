import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import curses

def is_downloadable(url):
    """
    Check if a URL is downloadable based on its file extension.
    """
    extensions = {'.m4b', '.mp3','.mp4' ,'.jpg', '.afpk','.pdf', '.gz', '.txt', '.xml', '.zip', '.torrent', '.sqlite'}
    return any(url.endswith(ext) for ext in extensions)

def fetch_folder_contents(link, base_link):
    try:
        # Fetch HTML content of the link
        response = requests.get(link)
        response.raise_for_status()

        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the directory listing table
        directory_table = soup.find('table', class_='directory-listing-table')

        # Extract downloadable items (files and folders)
        downloadable_items = []
        if directory_table:
            rows = directory_table.find_all('tr')
            for row in rows:
                link = row.find('a', href=True)
                if link:
                    href = link['href']
                    url = urljoin(base_link, href)  # Ensure the URL is absolute
                    if "/details/ Go to parent directory" not in href:
                        if url.endswith('/'):
                            folder_name = href.split('/')[-2]  # Extract folder name
                            downloadable_items.append((folder_name, '📁', href))  # Folder
                        elif is_downloadable(url):
                            downloadable_items.append((link.text, '📄', href))  # File

        return downloadable_items

    except requests.RequestException as e:
        print("fetch_folder_contents Error fetching content:", e)
        return []

def display_folder_contents(stdscr, folder_link, start_index, base_link):
    stdscr.clear()
    curses.curs_set(0)
    stdscr.addstr(0, 0, "Press 'q' to exit")
    
    try:
        folder_contents = fetch_folder_contents(folder_link, base_link)
    except Exception as e:
        stdscr.addstr(2, 0, f"display_folder_contents Error fetching folder contents: {e}")
        stdscr.refresh()
        stdscr.getch()
        return

    current_index = start_index
    max_displayable_items = curses.LINES - 3 # Calculate the maximum number of items that can be displayed

    while True:
        for i, (item, icon, folder_href) in enumerate(folder_contents[current_index:current_index+max_displayable_items]):
            if i == 0 and current_index != 0:
                stdscr.addstr(i+2, 0, "↑ Scroll Up", curses.color_pair(1))
            elif i == max_displayable_items - 1 and current_index + max_displayable_items < len(folder_contents):
                stdscr.addstr(i+2, 0, "↓ Scroll Down", curses.color_pair(1))
            else:
                stdscr.addstr(i+2, 0, f"{icon} {item}")

        key = stdscr.getch()

        if key == curses.KEY_UP:
            current_index = max(0, current_index - 1)
        elif key == curses.KEY_DOWN:
            current_index = min(len(folder_contents) - max_displayable_items, current_index + 1)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if folder_contents[current_index][1] == '📁':
                # Use urljoin to ensure the URL is correctly formed
                new_folder_link = urljoin(base_link, folder_contents[current_index][2])
                display_folder_contents(stdscr, new_folder_link, 0, base_link)
        elif key == curses.KEY_BACKSPACE or key == ord('b'):
            return # Go back
        elif key == ord('q') or key == 27: # Esc key
            break

def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)

    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 0, "Press 'q' to exit")
    stdscr.refresh()

    initial_link = "https://archive.org/download/school-of-motion-animation-bootcamp"
    display_folder_contents(stdscr, initial_link, 0, initial_link)

if __name__ == "__main__":
    curses.wrapper(main)