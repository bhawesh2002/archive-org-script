# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2024-07-09

### Added
1. Implement `extract_extension` function to extract the extension of the selected files.(`extract_extension.py`)
2. Implement `select_extensions` function to select files based on their extension.(`select_extensions.py`)
3. Implement `extension_selection_window` function to display the extension selection window.(`extension_selection_window.py`)
4. Call `extension_selection_window` function in `file_browser` when '2' key is pressed.(`file_browser.py`)
5. Call `select_extensions` function in `file_browser` to select files based on their extension.(`file_browser.py`)
### Changes from Previous Release
1. __Minor Feature__: Added the ability to select files based on their extension using the '2' key.
2. __Minor Feature__: Improved user experience by providing an extension selection window to filter files based on their extension.

## [0.2.3] - 2024-07-08

### Added
1. Implement `select_all` and `deselect_all` functions to select/deselect all files and folders in the filetree(`select_or_deselect_all.py`).
2. Use `1` and `0` keys to select and deselect all files and folders(`file_browser.py`).
3. Call `select_all` and `deselect_all` functions in `file_browser` when '1' and '0' keys are pressed(`file_browser.py`).
### Changes from Previous Release
1. __Patch__: Added the ability to select/deselect all files and folders in the filetree using the '1' and '0' keys, respectively.

## [0.2.2] - 2024-07-06

### Added
1. Implemented `filter_empty_dirs` function to remove empty directories from selected files.(`filter_empty_dirs.py`)
2. Call `filter_empty_dirs` function in `toggle_selection` function to remove empty dirs from selected files.(`toggle_selection.py`)
### Changes from Previous Release
1. __Bug Fix__: Fixed the issue where empty directories appeared **selected** (appended by cyan color asterisk) when browsing files.


## [0.2.1] - 2024-07-01

### Added
1. Implemented `filter_priv_files` function to remove private files from selected files.(`filter_priv_files.py`)
2. Call `filter_priv_files` function in `toggle_selection` function to remove private files from selected files.(`toggle_selection.py`)
### Changes from Previous Release
1. __Bug Fix__: Fixed the issue where private files were being included in the list of selected files.


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

