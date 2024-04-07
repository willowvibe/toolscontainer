import os
import sys
import logging
import threading
from moviepy.editor import VideoFileClip
import customtkinter as ctk
from tkinter import scrolledtext, filedialog, messagebox

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     filename=r'conversion.log',  # Log to a file named conversion.log
#     filemode='a'  # Append mode, so log file is not overwritten
# )

__version__ = "1.0.0"

video_formats = {
    '.mp4': ['libx264', 'aac'],
    '.mkv': ['libx265', 'aac'],
    '.mov': ['libx264', 'aac'],
    '.avi': ['mpeg4', 'mp3'],
    '.wmv': ['wmv2', 'wmav2']
}


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


class GUI_Setup(ctk.CTk):
    def __init__(self, format_to_codec):
        super().__init__()

        self.title("Video Converter")
        self.geometry("800x600")

        # Selection frame for input and output folder, and format
        self.selection_frame = ctk.CTkFrame(self)
        self.selection_frame.pack(pady=20, padx=10, fill="x")

        # Input folder selection
        self.input_folder_frame = ctk.CTkFrame(self.selection_frame)
        self.input_folder_frame.pack(side="left", fill="x", expand=True)
        self.input_folder_label = ctk.CTkLabel(self.input_folder_frame, text="Input Folder:")
        self.input_folder_label.pack(side="left")
        self.select_input_folder_button = ctk.CTkButton(self.input_folder_frame, text="Browse")
        self.select_input_folder_button.pack(side="left")

        # Output folder selection
        self.output_folder_frame = ctk.CTkFrame(self.selection_frame)
        self.output_folder_frame.pack(side="left", fill="x", expand=True)
        self.output_folder_label = ctk.CTkLabel(self.output_folder_frame, text="Output Folder:")
        self.output_folder_label.pack(side="left")
        self.select_output_folder_button = ctk.CTkButton(self.output_folder_frame, text="Browse")
        self.select_output_folder_button.pack(side="left")

        # Output format selection
        self.format_frame = ctk.CTkFrame(self.selection_frame)
        self.format_frame.pack(side="left", fill="x", expand=True)
        self.format_label = ctk.CTkLabel(self.format_frame, text="Output Format:")
        self.format_label.pack(side="left")
        self.format_combobox = ctk.CTkComboBox(self.format_frame, values=list(format_to_codec.keys()), width=100)
        self.format_combobox.set(".mp4")  # Set default format
        self.format_combobox.pack(side="left")

        # Conversion status and progress frame
        self.status_frame = ctk.CTkFrame(self)
        self.status_frame.pack(pady=10, fill='x', padx=10)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.status_frame)
        self.progress_bar.pack(fill="x", padx=20, pady=(5, 20))
        self.progress_percentage_label = ctk.CTkLabel(self.status_frame, text="0%")
        self.progress_percentage_label.pack(side="left", padx=(20, 0))

        self.time_taken_label = ctk.CTkLabel(self.status_frame, text="Time: 0s")
        self.time_taken_label.pack(side="right", padx=(0, 20))

        # Converted files list
        self.converted_files_label = ctk.CTkLabel(self.status_frame, text="Conversion Log:")
        self.converted_files_label.pack(pady=(5, 5), side='top')
        self.converted_files_box = scrolledtext.ScrolledText(self.status_frame, height=10, state='disabled')
        self.converted_files_box.pack(fill="both", expand=True, padx=20, pady=(5, 20))

        # Convert button
        self.convert_button = ctk.CTkButton(self, text="Start Conversion")
        self.convert_button.pack(pady=(10, 0))

        # Close button - positioned below the Convert button
        self.close_button = ctk.CTkButton(self, text="Close App", command=self.close_gui)
        self.close_button.pack(pady=(100, 10))

    def close_gui(self):
        # Perform any necessary cleanup here
        self.destroy()  # Closes the GUI window


class VideoConverterGUI(GUI_Setup):
    def __init__(self):
        super().__init__(video_formats)
        # Bind event handlers to GUI elements
        self.select_input_folder_button.configure(command=self.select_input_folder)
        self.select_output_folder_button.configure(command=self.select_output_folder)
        self.convert_button.configure(command=self.start_conversion_thread)
        self.input_folder = ""
        self.output_folder = ""

        self.converted_files_box.tag_configure('start', foreground='blue')
        self.converted_files_box.tag_configure('done', foreground='green')
        self.converted_files_box.tag_configure('failed', foreground='red')

    def select_input_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_folder = folder
            self.input_folder_label.configure(text=f"Input: {os.path.basename(folder)}")
            logging.info(f"Input folder selected: {os.path.basename(folder)}")

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder = folder
            self.output_folder_label.configure(text=f"Output: {os.path.basename(folder)}")
            logging.info(f"Output folder selected: {os.path.basename(folder)}")

    def start_conversion_thread(self):
        if not self.input_folder or not self.output_folder:
            messagebox.showerror("Error", "Please select both input and output folders.")
            logging.error("Attempted to start conversion without selecting both input and output folders.")
            return
        self.convert_button.configure(state='disabled')
        selected_format = self.format_combobox.get()
        conversion_thread = threading.Thread(target=self.start_conversion, args=(selected_format,), daemon=True)
        conversion_thread.start()

    def start_conversion(self, selected_format):
        try:
            logging.info("Conversion started.")
            convert_videos(self.input_folder, self.output_folder, output_format=selected_format,
                           callback=self.update_conversion_log)
        except Exception as e:
            logging.error(f"Conversion error: {e}")
            self.after(0, lambda: messagebox.showerror("Conversion Error", str(e)))
        finally:
            self.after(0, lambda: self.convert_button.configure(state='normal'))
            logging.info("Conversion completed.")

    def update_conversion_log(self, file, status, current_index, total_files):
        # Format the message based on status
        if status == "start":
            message = f"Starting conversion of {file}...\n"
            tag = 'start'
        elif status == "done":
            message = f"Successfully converted {file}\n"
            tag = 'done'
        elif status == "failed":
            message = f"Failed to convert {file}\n"
            tag = 'failed'
        else:
            message = f"Unknown status for {file}\n"
            tag = ''

        # Insert the message with the appropriate tag
        self.append_text(message, tag)

    def update_callback(self, file, status, current_index, total_files):
        # This method updates the GUI based on the conversion progress
        if status == "start":
            # Update for start of conversion
            pass
        elif status == "done":
            # Update for successful conversion of a file
            self.after(0, lambda: self.update_progress(current_index, total_files))
            self.after(0, lambda: self.append_text(f"Successfully converted {file}\n", "done"))
        elif status == "failed":
            # Update for failed conversion of a file
            self.after(0, lambda: self.append_text(f"Failed to convert {file}\n", "failed"))

    def update_progress(self, current, total):
        # This method updates the progress bar and percentage label
        progress = current / total * 100
        self.progress_bar.set(progress)  # Assuming this sets the progress bar value
        self.progress_percentage_label.configure(text=f"{progress:.2f}%")

    def append_text(self, text, tag=None):
        self.converted_files_box.configure(state='normal')
        if tag:
            self.converted_files_box.insert('end', text, tag)
        else:
            self.converted_files_box.insert('end', text)
        self.converted_files_box.yview_moveto(1)  # Ensure the latest entry is visible
        self.converted_files_box.configure(state='disabled')
        logging.info(text.strip())

    def close_gui(self):
        # Safely close the GUI
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            logging.info("GUI closed by user.")


def main():
    print(f"Running script version: {__version__}")


if __name__ == "__main__":
    app = VideoConverterGUI()
    app.mainloop()
