# Checks if the link follows the format of an archive.org download directory link.
def validate_link(link):
    return "https://archive.org/download/" in link
