# 📁 File Organizer with GUI

A powerful and easy-to-use **File Organizer** with a **Graphical User Interface (GUI)** built using Python and Tkinter. Automatically sorts files into categorized folders based on their types.

## 🚀 Features
- ✅ **GUI Interface** – No need to use the terminal.
- ✅ **Automatic Sorting** – Organizes files into predefined categories.
- ✅ **Customizable File Types** – Easily modify the file type dictionary.
- ✅ **One-Click Operation** – Select a folder and organize with a single click.

## 📂 Organized Folder Structure
After running the organizer, files will be grouped like this:
```
📂 Selected Folder
   ├── 📂 Images
   │   ├── photo.jpg
   │   ├── wallpaper.png
   ├── 📂 Documents
   │   ├── report.pdf
   │   ├── notes.txt
   ├── 📂 Programming
   │   ├── script.py
   │   ├── project.js
   ├── 📂 Videos
   │   ├── movie.mp4
   ├── 📂 Others
```

## 🛠 Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/Naeem-360/File-Organizer.git
   cd File-Organizer
   ```
2. **Install Dependencies**
   Ensure you have **Python 3.7+** installed. Then, install Tkinter (pre-installed in most cases):
   ```bash
   pip install tk
   ```
3. **Run the Script**
   ```bash
   python file_organizer.py
   ```

## 🎮 Usage
1. Run the script.
2. Click **"Browse"** and select a folder.
3. Click **"Organize Files"** to start sorting.
4. Files are moved into categorized folders automatically.

## ⚡ Customization
You can modify the `FILE_TYPE` dictionary in `file_organizer.py` to add or change file categories.

```python
FILE_TYPE = { 
    "Images": [".jpg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Programming": [".py", ".js", ".java"],
    # Add more categories as needed
}
```

## 🤝 Contributing
Pull requests are welcome! Follow these steps:

1. **Fork** the repo.
2. Create a **new branch** (`feature-branch`).
3. Commit your **changes** and push.
4. Submit a **Pull Request**.

## 📜 License
This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

🌟 **If you find this useful, please ⭐ the repo!**
