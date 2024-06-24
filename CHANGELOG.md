# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2024-06-24
### Added
1. Updated logic to include more detailed status information based on access permissions.(`parse_xml.py`)
2. Enhanced file information display with a visual indicator for private files.(`browser.py`)
    - Files marked as private now display a lock symbol (🔒) next to their size.
### Changes from Previous Release
1. __Minor Feature__: Improved user experience by visually distinguishing private files.



## [0.1.1] - 2024-06-20

### Added
1. Support to toggle selection/deselection of files using the spacebar(toggle_selection.py).
    - Rename the file `select_item.py` to `toggle_selection.py`.
    - Rename the function `addadd_to_selected_files` to `toggle_selection`.
    - Use Deep Copy instead of Shallow Copy to avoid modifying the original list.
2. Modify import statements and call modified function name(file_browser.py).
### Changes from Previous Release
1. __Bug Fix__: Fixed the issue where the user could not <u>_deselect_</u> a file/folder once it was selected.

## [0.1.0] - 2024-06-17

### Added
- Initial release of the script.
- Feature to prompt the user to enter an Archive.org identifier.
- Validation of the Archive.org identifier.
- Downloading and displaying metadata for the identifier.
- Text-based User Interface (TUI) for browsing files and directories within the identifier.
- Navigation using arrow keys and selection using the space bar.
- Confirmation of file selection with the Enter key.
- Downloading selected files.
- Displaying a "Download Successful" status after downloads are complete.

