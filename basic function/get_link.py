# Extracts the identifier from a valid archive.org download directory link.
def get_directory_identifier(link):
    return link.split("/")[-1]
