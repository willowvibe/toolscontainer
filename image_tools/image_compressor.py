"""
Created on Mar 2024
@author: Harish NG
This module deals with compressing and decompressing of image files
"""

import os
from PIL import Image
from support_modules.file_handler import FileHandler # pylint: disable=E0401


def compress_image(image_path, output_path, ratio):
    """
    Compresses a single image based on the specified ratio and saves it.

    Args:
      image_path: Path to the image file.
      output_path: Path to save the compressed image.
      ratio: A float between 0 and 1 representing the compression ratio.
    """
    try:
        img = Image.open(image_path)

        width, height = img.size

        new_width = int(width * ratio)
        new_height = int(height * ratio)

        # Resize the image
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        resized_img.save(output_path, optimize=True, quality=90)

        print(f"Compressed '{image_path}' to '{output_path}'")
    except Exception as e: # pylint: disable=W0718
        print(f"Error compressing '{image_path}': {e}")


def compress_images(input_folder, output_folder, ratio):
    """
  Compresses all images in a folder by a given ratio and saves them in another folder.

  Args:
    input_folder: Path to the folder containing the images to compress.
    output_folder: Path to the folder where the compressed images will be saved.
    ratio: A float between 0 and 1 representing the compression ratio.
  """
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    file_dir = FileHandler(input_folder)

    # Check if the input folder exists
    if not file_dir.check_directory():
        print(f"Error: Input folder '{input_folder}' does not exist.")
        return

    # Find all image files (.jpg, .jpeg, .png)
    image_files = file_dir.find_files_with_extensions((".jpg", ".jpeg", ".png"))

    # Check if there are any images
    if not image_files:
        print(f"No image files found in '{input_folder}'.")
        return

    # Process each image file
    for image_path in image_files:
        # Check if the image file has data (not empty)
        if not file_dir.has_data(image_path):
            print(f"Skipping '{image_path}' as it has no data.")
            continue

        # Generate the output path
        output_path = os.path.join(output_folder, os.path.basename(image_path))

        # Compress the image
        compress_image(image_path, output_path, ratio)
