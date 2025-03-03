import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# File types dictionary
FILE_TYPE = { 
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".csv", ".pptx", ".odt", ".ods", ".odp"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv", ".webm"],
    "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "Archives": [".zip", ".rar", ".tar", ".7z", ".gz", ".bz2"],
    "Executables": [".exe", ".msi", ".bat", ".sh", ".apk", ".appimage"],
    "Programming": [".py", ".js", ".java", ".cpp", ".c", ".cs", ".rb", ".php", ".swift", ".go", ".ts"],
    "Web Files": [".html", ".css", ".js", ".php", ".asp", ".xml"],
    "Databases": [".sql", ".sqlite", ".db", ".mdb", ".accdb"],
    "Design & Graphics": [".psd", ".ai", ".xd", ".fig", ".sketch", ".indd"],
    "3D Models": [".obj", ".fbx", ".stl", ".3ds", ".blend", ".dae"],
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
    "Ebooks": [".epub", ".mobi", ".azw3", ".pdf"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
    "System Files": [".dll", ".sys", ".ini", ".log"],
    "Torrents": [".torrent"],
    "Others": []  # Default category for unknown file types
}

# Function to organize files
def file_organizer(directory):
    if not os.path.exists(directory):
        messagebox.showerror("Error", "Directory does not exist!")
        return
    
    file_list = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    for file in file_list:
        file_path = os.path.join(directory, file)
        file_extension = os.path.splitext(file)[1].lower()

        folder_name = "Others"
        for category, extensions in FILE_TYPE.items():
            if file_extension in extensions:
                folder_name = category
                break
        
        folder_path = os.path.join(directory, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        shutil.move(file_path, os.path.join(folder_path, file))

    messagebox.showinfo("Success", "Files organized successfully!")

# Function to browse directory
def browse_directory():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)

# Function to start organizing files
def start_organizing():
    directory = folder_path.get()
    if directory:
        file_organizer(directory)
    else:
        messagebox.showerror("Error", "Please select a folder!")

# Create GUI window
root = tk.Tk()
root.title("File Organizer")
root.geometry("500x250")
root.resizable(False, False)

folder_path = tk.StringVar()

# GUI Layout
tk.Label(root, text="Select Folder:", font=("Arial", 12)).pack(pady=10)
tk.Entry(root, textvariable=folder_path, width=50).pack(pady=5)
tk.Button(root, text="Browse", command=browse_directory, font=("Arial", 10)).pack(pady=5)
tk.Button(root, text="Organize Files", command=start_organizing, font=("Arial", 12), bg="green", fg="white").pack(pady=20)

# Run the GUI
root.mainloop()
