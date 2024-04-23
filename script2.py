from colorama import Fore, Style  # Import colorama for colored text
import shutil  # For getting terminal size (not used now)

print(Fore.GREEN + Style.BRIGHT + "archive.org downloader" + Style.RESET_ALL)  # Green message

valid_link = False
while not valid_link:
    # Link Validation message (blue)
    print(Fore.BLUE + "Enter archive.org download directory link: " + Style.RESET_ALL, end="")

    # User Input (white not possible, but message before)
    download_link = input(Fore.WHITE + "(Paste the link here)" + Style.RESET_ALL + ": ")

    # Link Validation
    if "https://archive.org/download/" in download_link:
        valid_link = True  # Link is valid, break the loop
    else:
        print(Fore.RED + "Error: Invalid archive.org download directory link format." + Style.RESET_ALL)

# Extract identifier (assuming the format is correct)
identifier = download_link.split("/")[-1]

print(Fore.YELLOW + Style.BRIGHT + f"{'Directory Name: '}" + Fore.WHITE + Style.RESET_ALL + f"{identifier}", end="")
