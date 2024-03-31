import customtkinter as ctk
from tkinter import filedialog, scrolledtext
import threading
import os

# Ensure you have a module named 'converter_video.py' with a function 'convert_videos' correctly defined.
from converter_video import convert_videos

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

        # Converted files list
        self.converted_files_label = ctk.CTkLabel(self.status_frame, text="Conversion Log:")
        self.converted_files_label.pack(pady=(5, 5), side='top')
        self.converted_files_box = scrolledtext.ScrolledText(self.status_frame, height=10, state='disabled')
        self.converted_files_box.pack(fill="both", expand=True, padx=20, pady=(5, 20))
        # For Color Text in scroll Box
        self.converted_files_box.tag_configure("red_clr", foreground="red")
        self.converted_files_box.tag_configure("green_clr", foreground="green")
        self.converted_files_box.tag_configure("blue_clr", foreground="blue")

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

    def update_progress(self, file, status, current_index=0, total_files=1):
        # Ensure updates are thread-safe and done in the main thread
        def gui_update():
            message_prefix = ""
            tag = ""

            if status == "start":
                message_prefix = f"Starting conversion: {file} to format: {self.format_combobox.get()}\n"
                tag = "red_clr"
            elif status == "done":
                message_prefix = f"Conversion done: {file}\n"
                tag = "green_clr"
            elif status == "failed":
                message_prefix = f"Conversion failed: {file}\n"
                tag = "red_clr"

            # Update the log in the scrolled text box
            self.converted_files_box.configure(state='normal')
            self.converted_files_box.insert('end', message_prefix, tag)
            self.converted_files_box.yview_moveto(1)  # Auto-scroll to the bottom
            self.converted_files_box.configure(state='disabled')

            # Update the progress bar
            progress = current_index / total_files
            self.progress_bar.set(progress)

        self.after(0, gui_update)

    def start_conversion_thread(self):
        if not self.input_folder or not self.output_folder:
            # Directly updating the conversion log if folders are not selected
            self.converted_files_box.configure(state='normal')
            self.converted_files_box.insert('end', "Please select both input and output folders.\n")
            self.converted_files_box.configure(state='disabled')
            return

        # Disabling the convert button to prevent multiple concurrent conversion processes
        self.convert_button.configure(state='disabled')

        # Extracting the selected format from the combobox
        selected_format = self.format_combobox.get()

        # Creating a new thread for the conversion process
        conversion_thread = threading.Thread(target=lambda: self.start_conversion(selected_format), daemon=True)
        conversion_thread.start()

    def start_conversion(self, selected_format):
        # Ensure 'self.input_folder' is actually a directory and not a file
        if not os.path.isdir(self.input_folder):
            print(f"The input path {self.input_folder} is not a directory.")
            return

        # Disable the convert button to prevent multiple conversions running at the same time
        self.convert_button.configure(state='disabled')

        # Define a thread target function for the conversion process
        def conversion_process():

            total_files = len(
                [f for f in os.listdir(self.input_folder) if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))])
            current_index = 0

            # The callback function for updating the GUI with the conversion progress.
            def update_callback(file, status, current_index, total_files):
                self.after(0, lambda: self.update_progress(file, status, current_index, total_files))

            for file in os.listdir(self.input_folder):
                if not file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                    continue
                current_index += 1
                self.update_progress(file, "start", current_index, total_files)

                try:
                    # Dynamic codec selection is handled within convert_videos
                    convert_videos(self.input_folder, self.output_folder, selected_format, update_callback)

                    # No need to update progress here as it's handled via callback
                except Exception as e:
                    print(f"Error converting {file}: {e}")
                    self.after(0, lambda: self.update_progress(file, "failed", current_index, total_files))

            self.after(0, lambda: self.convert_button.configure(state='normal'))
            self.after(0, lambda: self.converted_files_box.configure(state='normal'))
            self.after(0, lambda: self.converted_files_box.insert('end', "All conversions completed.\n"))
            self.after(0, lambda: self.converted_files_box.configure(state='disabled'))
            self.after(0, lambda: self.progress_bar.set(1.0))  # Set progress bar to 100% at the end

        # Start the conversion process in a separate thread
        conversion_thread = threading.Thread(target=conversion_process)
        conversion_thread.start()

    def update_conversion_log(self, message):
        self.converted_files_box.configure(state='normal')
        self.converted_files_box.insert('end', message)
        self.converted_files_box.yview_moveto(1)
        self.converted_files_box.configure(state='disabled')


if __name__ == "__main__":
    app = VideoConverterGUI()
    app.mainloop()
