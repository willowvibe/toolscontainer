from moviepy.editor import VideoFileClip
import os


def convert_videos(input_folder, output_folder, output_format=".mp4", callback=None):
    """
    Convert all video files in the input_folder to the specified output_format
    and save them to the output_folder. A callback function can be provided
    to receive progress updates.
    """
    # Ensure output folder exists
    global clip
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Supported video formats
    format_to_codec = {
        ".mp4": "libx264",  # H.264 codec; widely supported, good for web videos
        ".avi": "mpeg4",  # MPEG-4 codec; older format, widely compatible
        ".mov": "libx264",  # H.264 codec; used in QuickTime
        ".mkv": "libx264",  # H.264 codec; for Matroska container, supports modern features
        ".flv": "flv",  # FLV codec; used in Flash Video
        ".wmv": "wmv2",  # Windows Media Video codec; for Windows Media Video
        ".webm": "libvpx-vp9",  # VP9 codec; for WebM container, good for web with smaller file sizes
        ".ogv": "libtheora",  # Theora codec; for Ogg container
        ".gif": "gif",  # GIF codec; for creating animated GIFs
    }

    supported_formats = list(format_to_codec.keys())
    files = [f for f in os.listdir(input_folder) if any(f.endswith(ext) for ext in supported_formats)]

    for index, file in enumerate(files):
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, os.path.splitext(file)[0] + output_format)
        codec = format_to_codec.get(output_format, "libx264")  # Default to "libx264" if not found
        try:
            clip = VideoFileClip(input_path)
            clip.write_videofile(output_path, codec=codec, verbose=False, logger=None)
            if callback:
                callback(file, "done", index + 1, len(files))
        except Exception as e:
            print(f"Failed to convert '{file}'. Error: {e}")
            if callback:
                callback(file, "failed", index + 1, len(files))
        finally:
            if 'clip' in locals():
                clip.close()


if __name__ == "__main__":
    # Example usage
    input_folder = "path/to/input_folder"
    output_folder = "path/to/output_folder"
    convert_videos(input_folder, output_folder)
