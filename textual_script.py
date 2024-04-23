import requests
from tqdm import tqdm  #For progress bar
from textual.app import App

class ArchiveDownloader(App):
    async def on_mount(self):
        self.title = "archive.org downloader"

if __name__ == "__main__":
    app = ArchiveDownloader()
    app.run()
