# Appian Patch File Modifier

This script is designed to modify files within an "Appian Patch" directory contained in a zip file. It performs text replacements in specified folders and creates a new zip archive of the modified patch directory. Additionally, it generates a "Customization File.properties" file and a readme file documenting the changes made.

## Features

- **Text Replacement**: Allows users to specify search and replace text across designated folders (`content`, `recordType`, `processModel`) within the Appian Patch.
- **Change Log**: Automatically tracks modified objects and logs changes for each object.
- **Output Files**:
  - **Modified Patch**: A new zip archive of the modified "Appian Patch" directory.
  - **Customization File**: Includes a predefined customization setting.
  - **Readme**: Lists all modified objects and provides a detailed change log.

## Usage

1. **Input**: Provide a zip file containing the "Appian Patch" directory.
2. **Text Replacement**: Enter the search and replace text when prompted.
3. **Output**: After execution, the modified files are stored in a folder named "PatchFiles" within your documents directory.

## Setup and Execution

### Requirements

- Python 3.x
- Libraries: `os`, `shutil`, `re`, `pathlib`, `zipfile`

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

### Run

1. Execute the script:

   ```bash
   python appian_patch_modifier.py
   ```

2. Follow the prompts to provide input and monitor the script's progress.

## Notes

- Ensure that your zip file contains the expected "Appian Patch" directory structure.
- Customize the `folders_to_search`, `search_text`, and `replace_text` lists as per your project requirements.

## Contributors

- https://github.com/prasannaKumarLS
- https://github.com/Navin-Reddy
