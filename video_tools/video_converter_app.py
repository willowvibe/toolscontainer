import os
import threading
from tkinter import filedialog, messagebox
from video_tools import gui_setup, converter_video
from utils import constants
import logging
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
video_formats = constants.video_formats
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=r'logs\video_converter_app.log',
                    filemode='a')
GUI_Setup = gui_setup.GUI_Setup


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
            converter_video.convert_videos(self.input_folder, self.output_folder, output_format=selected_format,
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


if __name__ == "__main__":
    app = VideoConverterGUI()
    app.mainloop()
