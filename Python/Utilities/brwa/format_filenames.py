""" 
This script removes spaces from the filenames of all PDF files in a specified directory.
It renames the files by replacing spaces with nothing (i.e., removing them).
you can use the script to replace other characters by changing the `replace` method argument.
beware using this script, as it will overwrite the original filenames.
It is recommended to create a backup of the files before running the script.

Removing periods from filenames is not recommended, as it may cause issues with file extensions.

Oder of opperations
1 - new_name = name.replace(" ", "_") # replaces spaces with underscores
2 - new_name = name.replace(".", "_") # replaces periods with underscores
3 - new_name = name.replace("__", "_") # replaces double underscores with single underscores
                                       # replacing periods with underscores can sometime 
                                       # create double underscores.
4 - new_name = name.replace("_-", "") # replaces underscore-dash with nothing
5 - new_name = name.replace(",", "") # replaces commas with nothing
6 - new_name = new_name.replace("(", "")  # Step 5: Replace parentheses with nothing
7 - new_name = new_name.replace(")", "")  # Step 5: Replace parentheses with nothing

 """
import os


def remove_spaces_from_filenames(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            name, ext = os.path.splitext(filename)
            
            # Perform replacements in the specified order
            new_name = name.replace(" ", "_")  # Step 1: Replace spaces with underscores
            new_name = new_name.replace(".", "_")  # Step 2: Replace periods with underscores
            new_name = new_name.replace("__", "_")  # Step 3: Replace double underscores with single underscores
            new_name = new_name.replace("_-", "")  # Step 4: Replace underscore-dash with underscore
            new_name = new_name.replace(",", "")  # Step 5: Replace commas with nothing
            new_name = new_name.replace("(", "")  # Step 5: Replace parentheses with nothing
            new_name = new_name.replace(")", "")  # Step 5: Replace parentheses with nothing
            new_name = new_name.replace("#", "")  # Step 5: Replace pound sign with nothing
                      
            new_filename = f"{new_name}{ext}"  # Preserve the file extension
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
            print(f"Renamed: {filename} -> {new_filename}")

# Specify the directory containing the PDF files
directory_path = r"\\nu\gis\Projects\2025_Projects\202507_images\images\Easment"
if os.path.exists(directory_path):
    remove_spaces_from_filenames(directory_path)
else:
    print(f"Directory does not exist: {directory_path}")

