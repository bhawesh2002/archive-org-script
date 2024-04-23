from textual.app import App

class ArchiveDownloader(App):
    async def on_mount(self):
        pass

if __name__ == "__main__":
    app = ArchiveDownloader()
    app.run()
