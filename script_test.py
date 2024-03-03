"""
Sample script for testing the functionality of the tools container
"""

# pylint: disable=E0401
from support_modules import file_handler, data_handler

path = input("Enter the Path of the file to be checked: ")
file_type = input("Enter the file type of the file to be checked: ")
file_type = data_handler.split_and_validate_extensions(file_type)

try:
    fh = file_handler.FileHandler(path)
    files_ext = fh.find_files_with_extensions(file_type)
    if fh.check_directory() and files_ext:
        print("Given Directory exits\n")
        print("Given extensions has these files ", files_ext, "\n")
        for file in files_ext:
            if fh.has_data(file):
                print(file, "Has Data ", "\n")
            else:
                print(file, "is empty", "\n")
    else:
        print("No such file")
except FileNotFoundError:
    print("No such directory")
