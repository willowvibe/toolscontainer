import tkinter as tk
from tkinter import filedialog


def browse_input_dir():
    """
    Opens a file dialog to select the input directory.
    """
    global input_dir_var
    input_dir = filedialog.askdirectory(title="Select Input Directory")
    if input_dir:
        input_dir_var.set(input_dir)


def browse_output_dir():
    """
    Opens a file dialog to select the output directory.
    """
    global output_dir_var
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    if output_dir:
        output_dir_var.set(output_dir)


def start_conversion():
    """
    Initiates video conversion based on user-provided directories and format.
    """
    input_dir = input_dir_var.get()
    output_dir = output_dir_var.get()
    output_format = output_format_var.get()
    if input_dir and output_dir:
        # Call your video conversion function here
        # convert_videos(input_dir, output_dir, output_format)
        status_text.set("Conversion completed.")
    else:
        status_text.set("Please select both input and output directories.")


# Main program
window = tk.Tk()
window.title("Video Converter")

# Set window size
window.geometry("500x300")

# Input directory selection
input_dir_var = tk.StringVar()
input_dir_label = tk.Label(window, text="Input Directory:")
input_dir_label.grid(row=0, column=0, padx=10, pady=10)
input_dir_entry = tk.Entry(window, textvariable=input_dir_var)
input_dir_entry.grid(row=0, column=1, padx=10, pady=10)
browse_input_button = tk.Button(window, text="Browse", command=browse_input_dir)
browse_input_button.grid(row=0, column=2, padx=10, pady=10)

# Output directory selection
output_dir_var = tk.StringVar()
output_dir_label = tk.Label(window, text="Output Directory:")
output_dir_label.grid(row=1, column=0, padx=10, pady=10)
output_dir_entry = tk.Entry(window, textvariable=output_dir_var)
output_dir_entry.grid(row=1, column=1, padx=10, pady=10)
browse_output_button = tk.Button(window, text="Browse", command=browse_output_dir)
browse_output_button.grid(row=1, column=2, padx=10, pady=10)

# Output format selection
output_format_var = tk.StringVar()
output_format_label = tk.Label(window, text="Output Format:")
output_format_label.grid(row=2, column=0, padx=10, pady=10)
output_format_menu = tk.OptionMenu(window, output_format_var, "mp4", "mkv", "webm", "avi")
output_format_menu.grid(row=2, column=1, padx=10, pady=10)

# Start conversion button
start_conversion_button = tk.Button(window, text="Start Conversion", command=start_conversion)
start_conversion_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Status text
status_text = tk.StringVar()
status_label = tk.Label(window, textvariable=status_text)
status_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Event loop
window.mainloop()
