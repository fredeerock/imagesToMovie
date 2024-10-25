import os
import cv2
import subprocess
from tkinter import filedialog, messagebox, Tk, StringVar, Toplevel
from ttkbootstrap import Style
from ttkbootstrap.widgets import Button, Label, Entry, Frame, Progressbar

# Global variable to store selected images
selected_images = []

def select_images():
    global selected_images
    filetypes = (("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*"))
    filenames = filedialog.askopenfilenames(title="Select Images", filetypes=filetypes)
    if filenames:
        selected_images = filenames
        status_var.set(f"{len(selected_images)} images loaded successfully.")

def create_video():
    global selected_images
    if not selected_images:
        messagebox.showerror("Error", "No images selected")
        return

    try:
        frame_rate = float(frame_rate_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid frame rate")
        return

    output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    if not output_file:
        return

    frame = cv2.imread(selected_images[0])
    height, width, layers = frame.shape
    video = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (width, height))

    progress_bar['maximum'] = len(selected_images)
    progress_bar['value'] = 0

    for i, image in enumerate(selected_images):
        video.write(cv2.imread(image))
        progress_bar['value'] = i + 1
        app.update_idletasks()

    video.release()
    show_success_dialog(output_file)

def show_success_dialog(file_path):
    success_dialog = Toplevel(app)
    success_dialog.title("Success")

    msg = Label(success_dialog, text=f"Video created successfully: {file_path}")
    msg.pack(pady=10)

    button_frame = Frame(success_dialog)
    button_frame.pack(pady=10)

    open_dir_button = Button(button_frame, text="Open Directory", command=lambda: open_directory(file_path))
    open_dir_button.pack(side="left", padx=5)

    close_button = Button(button_frame, text="Close", command=success_dialog.destroy)
    close_button.pack(side="left", padx=5)

def open_directory(file_path):
    directory = os.path.dirname(file_path)
    if os.name == 'nt':  # Windows
        subprocess.Popen(f'explorer "{directory}"')
    elif os.name == 'posix':  # macOS and Linux
        subprocess.Popen(['open', directory])

app = Tk()
app.title("Image Sequence to Video Maker")

style = Style(theme='darkly')  # You can choose from various themes like 'flatly', 'darkly', 'cosmo', etc.
style.master = app

# Title label
title_label = Label(app, text="Image Sequence to Video Maker", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

frame = Frame(app, padding=10)
frame.pack(pady=10)

select_button = Button(frame, text="Select Images", command=select_images)
select_button.pack(side="left", padx=5)

frame_rate_label = Label(frame, text="Frame Rate:")
frame_rate_label.pack(side="left", padx=5)

frame_rate_entry = Entry(frame)
frame_rate_entry.insert(0, "30")  # Set default frame rate to 30
frame_rate_entry.pack(side="left", padx=5)

create_button = Button(frame, text="Create Video", command=create_video)
create_button.pack(side="left", padx=5)

progress_bar = Progressbar(app, orient="horizontal", length=400, mode='determinate')
progress_bar.pack(pady=10)

# Status bar
status_var = StringVar()
status_var.set("Select images to create a video.")
status_bar = Label(app, textvariable=status_var, relief="sunken", anchor="w")
status_bar.pack(side="bottom", fill="x")

app.mainloop()