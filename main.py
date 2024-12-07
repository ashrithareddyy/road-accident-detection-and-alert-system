from camera import startapplication
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  # Import Image and ImageTk for loading images
import threading

def start_video_application():
    """Open a file dialog and start the accident detection with the selected video."""
    
    root = tk.Tk()
    root.title("Accident Detection System")

    # Set window size and position
    width, height = 800, 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.resizable(0, 0)

    # Load the background image
    bg_image = Image.open("homee.jpg")  # Specify the path to your background image
    bg_image = bg_image.resize((width, height), Image.LANCZOS)  # Resize the image to fit the window
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create a label for the background image
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill the entire window

    def browse_video():
        """Open a file dialog to select a video file."""
        video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mkv")])
        if video_path:
            print(f"Selected video: {video_path}")  # Debugging statement
            # Start video processing in a new thread
            threading.Thread(target=startapplication, args=(video_path,), daemon=True).start()

    def on_exit():
        """Handle the exit button and prompt for confirmation."""
        result = messagebox.askquestion("Accident Detection System", 'Are you sure you want to exit?', icon="warning")
        if result == 'yes':
            root.destroy()  # Close the Tkinter window

    # Create and pack buttons
    browse_button = tk.Button(root, text="Browse Video", command=browse_video, font=("Helvetica", 14), bg="#4CAF50", fg="white", padx=10, pady=5)
    browse_button.place(relx=0.5, rely=0.4, anchor='center')  # Center the button

    exit_button = tk.Button(root, text="Exit", command=on_exit, font=("Helvetica", 14), bg="#f44336", fg="white", padx=10, pady=5)
    exit_button.place(relx=0.5, rely=0.5, anchor='center')  # Center the button

    # Override the close button to call on_exit
    root.protocol("WM_DELETE_WINDOW", on_exit)

    root.mainloop()  # Start the Tkinter event loop

if __name__ == '__main__':
    start_video_application()








