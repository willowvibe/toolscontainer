import os
import sys
import logging
import argparse
from moviepy.editor import VideoFileClip
from concurrent.futures import ThreadPoolExecutor

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from utils import constants
video_formats = constants.video_formats
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=r'logs\conversion.log',  # Log to a file named conversion.log
    filemode='a'  # Append mode, so log file is not overwritten
)


def convert_video(input_path, output_path, codec):
    try:
        clip = VideoFileClip(input_path)
        clip.write_videofile(output_path, codec=codec, verbose=False, logger=None)
        logging.info(f"Successfully converted '{input_path}' to '{output_path}'")
    except Exception as e:
        logging.error(f"Failed to convert '{input_path}'. Error: {e}")
    finally:
        if 'clip' in locals():
            clip.close()


def convert_videos(input_folder, output_folder, output_format=".mp4", preferred_codec=None, callback=None):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = [f for f in os.listdir(input_folder)
             if os.path.isfile(os.path.join(input_folder, f))
             and os.path.splitext(f)[1].lower() in video_formats.keys()]

    total_files = len(files)

    for index, file in enumerate(files):
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, os.path.splitext(file)[0] + output_format)
        codec = preferred_codec if preferred_codec else 'libx264'  # Simplified codec selection for demonstration

        # Call callback with "start" status
        if callback:
            callback(file, "start", index + 1, total_files)

        try:
            clip = VideoFileClip(input_path)
            clip.write_videofile(output_path, codec=codec, verbose=False, logger=None)

            # Call callback with "done" status
            if callback:
                callback(file, "done", index + 1, total_files)
        except Exception as e:
            # Call callback with "failed" status
            if callback:
                callback(file, "failed", index + 1, total_files)
        finally:
            if 'clip' in locals():
                clip.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert videos from one format to another.')
    parser.add_argument('input_folder', type=str, help='Path to the input folder containing video files')
    parser.add_argument('output_folder', type=str, help='Path to the output folder for the converted videos')
    parser.add_argument('--output_format', type=str, default='.mp4', help='Output video format (default: .mp4)')
    parser.add_argument('--preferred_codec', type=str, default=None, help='Preferred codec (default: None)')

    args = parser.parse_args()

    convert_videos(args.input_folder, args.output_folder, args.output_format, args.preferred_codec)
