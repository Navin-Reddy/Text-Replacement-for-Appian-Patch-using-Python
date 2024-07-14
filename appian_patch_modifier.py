# This code is an example of a script that takes a zip file containing an "Appian Patch" directory and performs text replacement on certain files within the directory.
# After replacement, the script creates a new zip archive of the modified patch directory, a "Customization File.properties" file, and a readme file
# containing a list of modified objects and change log. Finally, it prints the location of the patch files.

import os
import shutil
import re
from pathlib import Path
from zipfile import ZipFile

# Variables for the patch folder and custom data file
patch_folder_name = "Appian Patch"
custom_data_file = "Customization File.properties"
custom_data = "importSetting.FORCE_UPDATE=true"

# List of folders to search for the text to replace
folders_to_search = ["content", "recordType", "processModel"]
encoding = "ISO-8859-1"

# Prompt user for the patch zip file and create the result folder
patch_zip_file = Path(input("Enter Patch Directory: "))
result_folder = Path(os.path.join(os.path.expanduser('~'), 'Documents', "PatchFiles"))
os.makedirs(result_folder, exist_ok=True)
root_directory = Path(result_folder)

# Prompt user for the search and replace text
search_text = input("Enter Search Text: ").split(",")
replace_text = input("Enter Replace Text: ").split(",")

# Set to keep track of modified objects and dictionary for change log
modified_objects = set()
change_log = {}

# Remove the previous patch folder and extract the new one from the zip file
shutil.rmtree(root_directory / patch_folder_name, ignore_errors=True)
with ZipFile(patch_zip_file, "r") as z_object:
    z_object.extractall(path=root_directory / patch_folder_name)

# Create a dictionary for the search and replace text and loop through the folders
replace_dict = dict(zip(search_text, replace_text))
for folder in folders_to_search:
    path = root_directory / patch_folder_name / folder
    if os.path.exists(path):
        content_files = os.scandir(path)
        for item in content_files:
            if item.is_file():
                # Open and read the file, replace the text, and update the change log
                with open(item.path, "r", encoding=encoding) as file:
                    data = file.read()
                    for search, replace in replace_dict.items():
                        if search in data:
                            data = data.replace(search, replace)
                            if folder == "content":
                                temp = re.search("<name>(.*)</name>", data).group(1)
                            elif folder == "recordType":
                                temp = re.search("<a:pluralName>(.*)</a:pluralName>", data).group(1)
                            elif folder == "processModel":
                                temp = re.search(r'<value><!\[CDATA\[(.*)\]\]></value>', data).group(1)
                            modified_objects.add(temp)
                            if temp in change_log:
                                change_log[temp] += f", {search} --> {replace}"
                            else:
                                change_log[temp] = f"{search} --> {replace}"
                # Write the modified data back to the file
                with open(item.path, "w", encoding=encoding) as file:
                    file.write(data)

# Create a zip archive of the patch folder and delete the original folder
shutil.make_archive(root_directory / patch_folder_name, "zip", root_directory / patch_folder_name)
shutil.rmtree(root_directory / patch_folder_name, ignore_errors=True)

# Create the custom data file
with open(root_directory / custom_data_file, "w", encoding=encoding) as file:
    file.write(custom_data)

# Delete and create the readme file with the list of modified objects and change log
if os.path.exists(root_directory / "readme.txt"):
    os.remove(root_directory / "readme.txt")
with open(root_directory / "readme.txt", "w", encoding=encoding) as file:
    file.write("Objects Modified:\n")
    for i, obj in enumerate(modified_objects):
        file.write(f" {i + 1}. {obj}\n")
    file.write("\n")
    file.write("Change Log:\n")
    for i, obj in enumerate(modified_objects):
        file.write(f"{i + 1}. {obj} : {change_log[obj]}\n")

# Print the location of the patch files
print("\nSuccess!!!, Patch Files are available in the below folder \n", root_directory.as_posix())
