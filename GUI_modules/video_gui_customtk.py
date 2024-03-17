import customtkinter as ctk
import threading
import os
from video_tools.video_converter import convert_videos
from support_modules import file_handler

class VideoConverterGUI:
    def __init__(self):
        self.status_label = None
        self.status_text_var = None
        self.root = ctk.CTk()
        self.root.title("Video Converter")
        self.root.geometry("500x300")

        self.input_dir_var = ctk.StringVar()
        self.output_dir_var = ctk.StringVar()
        self.output_format_var = ctk.StringVar(value="mp4")
        self.file_handler = file_handler.FileHandler("")

        self.create_widgets()

    def create_widgets(self):
        # Input directory selection
        input_dir_label = ctk.CTkLabel(self.root, text="Input Directory:")
        input_dir_label.grid(row=0, column=0, padx=10, pady=10)
        input_dir_entry = ctk.CTkEntry(self.root, textvariable=self.input_dir_var)
        input_dir_entry.grid(row=0, column=1, padx=10, pady=10)
        browse_input_button = ctk.CTkButton(self.root, text="Browse", command=self.browse_input_dir)
        browse_input_button.grid(row=0, column=2, padx=10, pady=10)

        # Output directory selection
        output_dir_label = ctk.CTkLabel(self.root, text="Output Directory:")
        output_dir_label.grid(row=1, column=0, padx=10, pady=10)
        output_dir_entry = ctk.CTkEntry(self.root, textvariable=self.output_dir_var)
        output_dir_entry.grid(row=1, column=1, padx=10, pady=10)
        browse_output_button = ctk.CTkButton(self.root, text="Browse", command=self.browse_output_dir)
        browse_output_button.grid(row=1, column=2, padx=10, pady=10)

        # Output format selection
        output_format_label = ctk.CTkLabel(self.root, text="Output Format:")
        output_format_label.grid(row=2, column=0, padx=10, pady=10)
        output_format_menu = ctk.CTkOptionMenu(self.root, values=["mp4", "mkv", "webm", "avi"],
                                               variable=self.output_format_var)
        output_format_menu.grid(row=2, column=1, padx=10, pady=10)

        # Start conversion button
        start_conversion_button = ctk.CTkButton(self.root, text="Start Conversion", command=self.start_conversion)
        start_conversion_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        # Status text
        self.status_text_var = ctk.StringVar()
        self.status_label = ctk.CTkLabel(self.root, textvariable=self.status_text_var)
        self.status_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    def browse_input_dir(self):
        input_dir = ctk.filedialog.askdirectory(title="Select Input Directory")
        if input_dir:
            self.input_dir_var.set(input_dir)
            self.file_handler.path = input_dir
            queue = self.file_handler.find_files_with_extensions(['.avi', '.mov', '.mkv', '.mp4', '.flv', '.webm'])
            self.status_text_var.set(f"Found {len(queue)} video files in the queue to be converted.")

    def browse_output_dir(self):
        output_dir = ctk.filedialog.askdirectory(title="Select Output Directory")
        if output_dir:
            self.output_dir_var.set(output_dir)

    def threaded_start_conversion(self):
        input_dir = self.input_dir_var.get()
        output_dir = self.output_dir_var.get()
        output_format = self.output_format_var.get()

        if input_dir and output_dir:
            valid_files_found = self.file_handler.data_check(['.avi', '.mov', '.mkv', '.mp4', '.flv', '.webm'])
            if valid_files_found:
                # Create a new thread to start conversion
                thread = threading.Thread(target=convert_videos, args=(input_dir, output_dir, output_format))
                thread.start()

                # Update status text
                self.status_text_var.set("Conversion started in a separate thread.")
            else:
                self.status_text_var.set("No videos found with valid data.")
        else:
            self.status_text_var.set("Please select both input and output directories.")

    def start_conversion(self):
        # Call the threaded_start_conversion function in a separate thread to prevent GUI freeze
        thread = threading.Thread(target=self.threaded_start_conversion)
        thread.start()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gui = VideoConverterGUI()
    gui.run()
