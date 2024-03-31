from moviepy.editor import VideoFileClip
import os


def convert_videos(input_folder, output_folder, output_format=".mp4", callback=None):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    format_to_codec = {
        ".mp4": "libx264",
        ".avi": "mpeg4",
        ".mov": "libx264",
        ".mkv": "libx264",
        ".flv": "flv",
        ".wmv": "wmv2",
        ".webm": "libvpx-vp9",
        ".ogv": "libtheora",
        ".gif": "gif",
    }

    supported_formats = list(format_to_codec.keys())
    files = [f for f in os.listdir(input_folder) if any(f.endswith(ext) for ext in supported_formats)]

    for index, file in enumerate(files):
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, os.path.splitext(file)[0] + output_format)
        codec = format_to_codec.get(output_format, "libx264")

        # Notify start of conversion
        if callback:
            callback(file, "start", index + 1, len(files))

        try:
            clip = VideoFileClip(input_path)
            clip.write_videofile(output_path, codec=codec, verbose=False, logger=None)

            # Notify completion of conversion
            if callback:
                callback(file, "done", index + 1, len(files))
        except Exception as e:
            print(f"Failed to convert '{file}'. Error: {e}")
            if callback:
                callback(file, "failed", index + 1, len(files))
        finally:
            if 'clip' in locals() or 'clip' in globals():
                clip.close()


if __name__ == "__main__":
    # Example usage
    input_folder = "path/to/input_folder"
    output_folder = "path/to/output_folder"
    convert_videos(input_folder, output_folder)
