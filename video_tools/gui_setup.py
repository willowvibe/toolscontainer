import customtkinter as ctk
from tkinter import scrolledtext
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Assuming customtkinter and other necessary imports are correctly set up
ctk.set_appearance_mode("Dark")  # Set the appearance to dark mode
ctk.set_default_color_theme("dark-blue")  # Set the color theme to dark blue


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

