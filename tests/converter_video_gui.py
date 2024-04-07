from moviepy.editor import VideoFileClip
import os
import customtkinter as ctk
from tkinter import filedialog, scrolledtext
import threading
import os
import time
from moviepy.editor import VideoFileClip


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


ctk.set_appearance_mode("Dark")  # Light/Dark mode
ctk.set_default_color_theme("dark-blue")  # Color theme


class VideoConverterGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Video Converter")
        self.geometry("800x600")

        self.selection_frame = ctk.CTkFrame(self)
        self.selection_frame.pack(pady=20, padx=10, fill="x")

        # Input folder selection
        self.input_folder_frame = ctk.CTkFrame(self.selection_frame)
        self.input_folder_frame.pack(side="left", fill="x", expand=True)
        self.input_folder_label = ctk.CTkLabel(self.input_folder_frame, text="Input Folder:")
        self.input_folder_label.pack(side="left")
        self.select_input_folder_button = ctk.CTkButton(self.input_folder_frame, text="Browse",
                                                        command=self.select_input_folder)
        self.select_input_folder_button.pack(side="left")

        # Output folder selection
        self.output_folder_frame = ctk.CTkFrame(self.selection_frame)
        self.output_folder_frame.pack(side="left", fill="x", expand=True)
        self.output_folder_label = ctk.CTkLabel(self.output_folder_frame, text="Output Folder:")
        self.output_folder_label.pack(side="left")
        self.select_output_folder_button = ctk.CTkButton(self.output_folder_frame, text="Browse",
                                                         command=self.select_output_folder)
        self.select_output_folder_button.pack(side="left")

        # Output format selection
        self.format_frame = ctk.CTkFrame(self.selection_frame)
        self.format_frame.pack(side="left", fill="x", expand=True)
        self.format_label = ctk.CTkLabel(self.format_frame, text="Output Format:")
        self.format_label.pack(side="left")

        self.format_to_codec = {
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
        # Update this line to use the keys from format_to_codec for the dropdown values
        self.format_combobox = ctk.CTkComboBox(self.format_frame, values=list(self.format_to_codec.keys()), width=100)
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
        # For Color Text in scroll Box
        self.converted_files_box.tag_configure("red_clr", foreground="red")
        self.converted_files_box.tag_configure("green_clr", foreground="green")
        self.converted_files_box.tag_configure("blue_clr", foreground="blue")
        self.converted_files_box.tag_configure("black_clr", foreground="black")

        # Convert button
        self.convert_button = ctk.CTkButton(self, text="Start Conversion", command=self.start_conversion_thread)
        self.convert_button.pack(pady=(10, 5), side='bottom')

        self.input_folder = ""
        self.output_folder = ""

    def select_input_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_folder = folder
            self.input_folder_label.configure(text=f"Input: {os.path.basename(folder)}")

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder = folder
            self.output_folder_label.configure(text=f"Output: {os.path.basename(folder)}")

    def update_progress(self, file, status, current_index=0, total_files=1, time_taken=None):
        def update():
            message = ""  # Initialize message with an empty string to avoid UnboundLocalError
            tag = "black_clr"
            if status == "start":
                self.converted_files_box.configure(state='normal')
                self.converted_files_box.insert('end', f"Starting Conversion:", "red_clr")
                self.converted_files_box.insert('end', f"{file},")
                self.converted_files_box.insert('end', f"To Format:", "green_clr")
                self.converted_files_box.insert('end', f"{self.format_combobox.get()}\n")
                self.converted_files_box.yview_moveto(1)
                self.converted_files_box.configure(state='disabled')
            elif status in ["done", "failed"]:
                message = "Conversion done:" if status == "done" else "Conversion failed:"
                self.converted_files_box.configure(state='normal')
                self.converted_files_box.insert('end', f"{message}", "blue_clr")
                self.converted_files_box.insert('end', f"{file}\n")
                self.converted_files_box.yview_moveto(1)
                self.converted_files_box.configure(state='disabled')
                self.progress_bar.set(current_index / total_files)

            self.converted_files_box.configure(state='normal')
            self.converted_files_box.insert('end', message,
                                            "red_clr" if status == "start" else "green_clr" if status == "done" else "blue_clr")
            self.converted_files_box.yview_moveto(1)
            self.converted_files_box.configure(state='disabled')

            # Update progress bar and label
            progress = current_index / total_files
            self.progress_bar.set(progress)
            self.progress_percentage_label.configure(text=f"{progress * 100:.2f}%")

            # Update time taken label if status is 'done'
            if status == "done" and time_taken is not None:
                self.time_taken_label.configure(text=f"Time: {round(time_taken, 2)}s")

        self.after(0, update)

    def start_conversion_thread(self):
        if not self.input_folder or not self.output_folder:
            self.update_conversion_log("Please select both input and output folders.\n")
            return
        self.convert_button.configure(state='disabled')
        selected_format = self.format_combobox.get()
        conversion_thread = threading.Thread(target=lambda: self.start_conversion(selected_format), daemon=True)
        conversion_thread.start()

    def update_conversion_log(self, message):
        self.converted_files_box.configure(state='normal')
        self.converted_files_box.insert('end', message)
        self.converted_files_box.yview_moveto(1)
        self.converted_files_box.configure(state='disabled')

    def start_conversion(self, selected_format):
        # Ensure 'self.input_folder' is actually a directory and not a file
        if not os.path.isdir(self.input_folder):
            print(f"The input path {self.input_folder} is not a directory.")
            return

        # Disable the convert button to prevent multiple conversions running at the same time
        self.convert_button.configure(state='disabled')

        # Define a thread target function for the conversion process
        def conversion_process():
            # List of supported formats derived from the keys of format_to_codec mapping
            supported_formats = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.ogv', '.gif']
            files = [f for f in os.listdir(self.input_folder) if os.path.splitext(f)[1].lower() in supported_formats]
            total_files = len(files)
            if total_files == 0:
                self.after(0, lambda: self.update_conversion_log("No supported files found for conversion.\n"))
                self.after(0, lambda: self.convert_button.configure(state='normal'))
                return

            current_index = 0

            # The callback function for updating the GUI with the conversion progress.
            def update_callback(file, status, current_index, total_files):
                self.after(0, lambda: self.update_progress(file, status, current_index, total_files))

            try:
                # Assuming convert_videos is designed to process all files in the input directory
                # and correctly calls update_callback with four arguments
                convert_videos(self.input_folder, self.output_folder, selected_format, update_callback)
            except Exception as e:
                print(f"Error during conversion: {e}")
                self.after(0, lambda: self.update_conversion_log(f"Error during conversion: {e}\n"))

            self.after(0, lambda: self.convert_button.configure(state='normal'))

        # Start the conversion process in a new thread to keep the GUI responsive
        conversion_thread = threading.Thread(target=conversion_process, daemon=True)
        conversion_thread.start()


if __name__ == "__main__":
    app = VideoConverterGUI()
    app.mainloop()
