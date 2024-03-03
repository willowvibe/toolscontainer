"""
Created on 02 Mar 2024
@author: Harish NG
This Module contains functions to deal with data and strings
"""


def split_and_validate_extensions(extensions_string):
    """
    function to deal with extensions string
    """
    extensions = extensions_string.strip().split(",")
    valid_extensions = []
    for extension in extensions:
        if len(extension) < 2 or extension[0] != ".":
            raise ValueError(f"Invalid extension: '{extension}"
                             f"'. Extensions must start with a dot (.) and cannot be empty.")
        valid_extensions.append(extension[1:])  # Remove the leading dot
    return valid_extensions
