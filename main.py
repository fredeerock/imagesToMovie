import os
import cv2
import customtkinter as ctk
from tkinter import filedialog, messagebox, StringVar

# Set the appearance mode to "dark"
ctk.set_appearance_mode("dark")

# Global variable to store selected images
selected_images = []

def select_images():
    global selected_images
    filetypes = (
        ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.exr *.hdr *.tga"),
        ("All files", "*.*")
    )
    filenames = filedialog.askopenfilenames(title="Select Images", filetypes=filetypes)
    if filenames:
        selected_images = filenames
        status_var.set(f"{len(selected_images)} images loaded successfully.")
        progress_bar.set(0)  # Reset the progress bar

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

    # Get the width and height of the first image
    first_image = cv2.imread(selected_images[0])
    height, width, layers = first_image.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_file, fourcc, frame_rate, (width, height))

    progress_bar.set(0)

    for i, image_path in enumerate(selected_images):
        image = cv2.imread(image_path)
        video_writer.write(image)
        progress_bar.set((i + 1) / len(selected_images))
        app.update_idletasks()

    video_writer.release()

    # Update the status bar
    status_var.set(f"Video created successfully: {output_file}")

# GUI setup
app = ctk.CTk()
app.title("Image to Video Converter")

frame = ctk.CTkFrame(app)
frame.pack(pady=10)

# Frame rate label
frame_rate_label = ctk.CTkLabel(frame, text="Frame Rate:")
frame_rate_label.pack(side="left", padx=5)

# Frame rate entry
frame_rate_entry = ctk.CTkEntry(frame)
frame_rate_entry.insert(0, "30")  # Set default frame rate to 30
frame_rate_entry.pack(side="left", padx=5)

# Select Images button
select_button = ctk.CTkButton(frame, text="Select Images", command=select_images)
select_button.pack(side="left", padx=5)

# Create Video button
create_button = ctk.CTkButton(frame, text="Create Video", command=create_video)
create_button.pack(side="left", padx=5)

# Progress bar
progress_bar = ctk.CTkProgressBar(app, width=400)
progress_bar.set(0)  # Ensure the progress bar starts with no progress
progress_bar.pack(pady=10)

# Status bar
status_var = StringVar()
status_var.set("Select images to create a video.")
status_bar = ctk.CTkLabel(app, textvariable=status_var, anchor="w")
status_bar.pack(side="bottom", fill="x", padx=10, pady=10)  # Add more padding around the status bar

# Start the main event loop
app.mainloop()