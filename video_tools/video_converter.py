import os
import pathlib
from converter import Converter
from tqdm import tqdm


def convert_video(input_file, output_file, output_format="mp4", on_progress=None):
    """
    Converts a video file to the specified format.

    Args:
      input_file: Path to the input video file.
      output_file: Path to the output video file.
      output_format: Desired output format (default: mp4).
      on_progress: Callback function to track conversion progress (optional).
    """
    # Check if input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    # Create Converter object
    conv = Converter()

    # Convert the video with progress tracking
    try:
        conv.convert(input_file, output_file, {
            'format': output_format,
            'on_progress': on_progress
        })
    except Exception as e:
        print(f"Error converting video: {e}")


def convert_videos(input_dir, output_dir, output_format="mp4"):
    """
    Converts video files in the input directory to the specified format in the output directory.

    Args:
      input_dir: Path to the directory containing video files.
      output_dir: Path to the output directory.
      output_format: Desired output format (default: mp4).
    """

    # Create input and output directories if they don't exist
    pathlib.Path(input_dir).mkdir(parents=True, exist_ok=True)
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(('.avi', '.mov', '.mkv', '.mp4', '.flv', '.webm')):  # Check for common video formats
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, os.path.splitext(filename)[0] + f".{output_format}")
            try:
                # Create a progress bar for the current file conversion
                with tqdm(total=100) as pbar:
                    # Update the progress bar as the conversion progresses
                    def on_progress(progress):
                        pbar.update(progress * 100)

                    convert_video(input_file, output_file, output_format, on_progress=on_progress)
            except Exception as e:
                print(f"Error converting {filename}: {e}")


