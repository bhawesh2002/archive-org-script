# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.4] - 2024-07-22

## Added
1. Calculate the no of extensions per row and width of extension_selection_win relative to parent window based on the length of longest extension(`extension_selection_win.py`)
2. Modify `display_help` function to take only parent_win as argument(`display_help.py`)
3. Calculate the dimensions of the help window based on the help text(`display_help.py`)
4. Quit the help window when any key is pressed(`display_help.py`)
5. Modify `file_browser` to correctly call `display_help`(`file_browser.py`)
## Changes from previous release
1. __Bug Fix__: Modify `extension_selection_win` to resize itself if default value of 7 results in error by calculating the appropriate value of no of extensions per row.
2. __Bug Fix__: Fix the bug where the help window was not been displayed correctly when `h` was pressed.

## [0.3.3] - 2024-07-17

## Added
1. Create `supported_extensions` file containing the list of supported file formats as specified in https://help.archive.org/help/files-formats-and-derivatives-file-definitions-2/.(`supported_extensions`)
2. Use the `supported_extensions` file to extract extensions from filetree.(`extract_extension.py`)
3. Pass 'extensions' list as a parameter in `extension_selection_window` function.(`extension_selection_win.py`)
4. Call `extract_extensions` function with in `file_browser`.(`file_browser.py`)
5. Correctly call `extension_selection_window` function with the `extensions` list as a parameter in `file_browser`.(`file_browser.py`)
### Changes from Previous Release
1. __Patch__: Added the list of supported file formats to the `supported_extensions` file as specified in the Archive.org documentation.
2. __Patch__: Used the `supported_extensions` file to extract extensions from the filetree.
3. __Bug_Fix__: Passed the `extensions` list as a parameter in the `extension_selection_window` function to improve performance
4. __Bug_Fix__: Call the `extract_extensions` function in the `file_browser`.
5. __Bug_Fix__: Correctly called the `extension_selection_window` function with the `extensions` list as a parameter in the `file_browser`.

## [0.3.2] - 2024-07-15

### Added
1. Allow the user to navigate the extension selection window using the 'w', 's', 'a', 'd' keys. (`extension_selection_win.py`)
2. Fix the issue with the extension selection window not displaying the extensions correctly. (`extension_selection_win.py`)
3. Center the extension selection window on the screen using stdscr as additional parameter. (`extension_selection_win.py`)
4. Call the `extension_selection_window` function with the correct parameters. (`file_browser.py`)
### Changes from Previous Release
__Bug Fix__: Fix the layout of the extension selection window
__Bug Fix__: Fix calculations responsible for centering the extension selection window
__Patch__: Allow the user to navigate the extension selection window using the 'w', 's', 'a', 'd' keys
__Patch__: Improved the visual indication of selected extensions and the current extension.

## [0.3.1] - 2024-07-15
### Added
1. Fix NoneType error when passing empty extensions list by adding None check.(`select_extensions.py`)
### Changes from Previous Release
1. __Bug Fix__: Fixed the NoneType error when passing an empty extensions list.

## [0.3.0] - 2024-07-15

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

