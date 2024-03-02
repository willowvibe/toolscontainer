"""
Created on 02 Mar 2024
@author: Harish NG
This module contains functions to handle file and directory errors
"""

import os


class FileHandler:
    """
    This class can handle file and directory errors
    """
    def __init__(self, path):
        self.path = path

    def check_directory(self):
        """Checks if the directory exists."""
        if not os.path.exists(self.path):
            return False
        else:
            return True

    def find_files_with_extensions(self, extensions):
        """Finds files with the specified extensions in the directory."""
        self.check_directory()  # Ensure directory exists before proceeding
        files_with_extensions = []
        for file in os.listdir(self.path):
            if any(file.endswith(ext) for ext in extensions):
                filepath = os.path.join(self.path, file)
                if os.path.isfile(filepath):  # Ensure it's a file, not a directory
                    files_with_extensions.append(filepath)
        return files_with_extensions

    def has_data(self, file_path):
        """Checks if the file has data (non-zero size)."""
        return (os.path.exists(os.path.join(self.path, file_path))
                and os.path.getsize(os.path.join(self.path, file_path)) > 0)

    def data_check(self, extensions):
        """Checks if all files with the specified extensions have data."""
        files_in_dir = self.find_files_with_extensions(extensions)
        return all(self.has_data(file) for file in files_in_dir)
