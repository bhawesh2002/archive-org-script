# Checks if the link follows the format of an archive.org download directory link.
def construct_link(link):
    # If the link is directory identifier only, add the necessary prefix
    if "https://archive.org/" not in link:
        link = f"https://archive.org/dwonload/{link}"
        return link
    elif "https://archive.org/details/" in link:
        link = link.replace("https://archive.org/details/", "https://archive.org/download/")
        return link
    elif "https://archive.org/download/" in link:
        return link

# def validate_link(link):
#     return "https://archive.org/download/" in link

