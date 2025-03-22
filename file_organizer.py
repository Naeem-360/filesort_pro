import os
import shutil
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QLineEdit, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QFont, QColor, QPainter, QPen, QCursor

# File types dictionary with expanded types for all categories
FILE_TYPE = { 
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp", ".ico", ".heic", 
               ".raw", ".psd", ".jp2", ".jpe", ".jfif", ".exif", ".pnm", ".ppm", ".pgm"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".csv", ".pptx", ".odt", ".ods", ".odp", ".doc", 
                  ".rtf", ".xls", ".wps", ".md", ".tex", ".pages", ".key", ".numbers", ".wpd", ".abw"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv", ".webm", ".mpeg", ".mpg", ".m4v", 
               ".3gp", ".ogv", ".vob", ".ts", ".m2ts", ".rm", ".rmvb", ".divx", ".asf", ".mts"],
    "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma", ".aiff", ".alac", ".ape", 
              ".mpc", ".opus", ".ra", ".mid", ".midi", ".au", ".amr", ".mka", ".dts", ".ac3"],
    "Archives": [".zip", ".rar", ".tar", ".7z", ".gz", ".bz2", ".iso", ".cab", ".arj", ".z", 
                 ".lzh", ".ace", ".tgz", ".xz", ".lzma", ".cpio", ".dmg", ".uue", ".sit", ".pea"],
    "Executables": [".exe", ".msi", ".bat", ".sh", ".apk", ".appimage", ".bin", ".run", ".cmd", 
                    ".com", ".deb", ".rpm", ".jar", ".vbs", ".ps1", ".x86", ".x64", ".app", ".dll", ".scr"],
    "Programming": {
        ".py": "Python",
        ".js": "JavaScript",
        ".java": "Java",
        ".cpp": "CPP",
        ".c": "C",
        ".cs": "CSharp",
        ".rb": "Ruby",
        ".php": "PHP",
        ".swift": "Swift",
        ".go": "Go",
        ".ts": "TypeScript",
        ".html": "HTML",
        ".css": "CSS",
        ".kt": "Kotlin",
        ".rs": "Rust",
        ".scala": "Scala",
        ".pl": "Perl",
        ".lua": "Lua",
        ".r": "R",
        ".dart": "Dart",
        ".m": "Matlab",
        ".vb": "VisualBasic",
        ".asm": "Assembly",
        ".sql": "SQL",
        ".pas": "Pascal",
        ".f": "Fortran",
        ".hs": "Haskell",
        ".jl": "Julia",
        ".groovy": "Groovy",
        ".erl": "Erlang",
        ".clj": "Clojure",
        ".elm": "Elm",
        ".coffee": "CoffeeScript",
        ".ino": "Arduino",
        ".d": "D",
        ".fs": "FSharp"
    },
    "Web Files": [".asp", ".xml", ".aspx", ".jsp", ".htm", ".xhtml", ".rss", ".json", ".yaml", ".yml", 
                  ".cgi", ".shtml", ".phtml", ".wsdl", ".xsd", ".atom", ".svg", ".htaccess", ".php3", ".php4"],
    "Databases": [".sqlite", ".db", ".mdb", ".accdb", ".dbf", ".sqlitedb", ".mdf", ".ldf", ".frm", ".ibd", 
                  ".myi", ".myd", ".db3", ".s3db", ".sl3", ".db2", ".nsf", ".fp7", ".fmp12", ".odb"],
    "Design & Graphics": [".psd", ".ai", ".xd", ".fig", ".sketch", ".indd", ".eps", ".cdr", ".svgz", ".afdesign", 
                          ".afphoto", ".afpub", ".dxf", ".dwg", ".fla", ".swf", ".xar", ".pxd", ".pdd", ".pct"],
    "3D Models": [".obj", ".fbx", ".stl", ".3ds", ".blend", ".dae", ".max", ".ma", ".mb", ".lwo", 
                  ".lws", ".c4d", ".dxf", ".skp", ".3dm", ".ply", ".x", ".b3d", ".gltf", ".glb"],
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods", ".tsv", ".dif", ".sxc", ".numbers", ".qpw", ".wk1", 
                     ".wks", ".123", ".gsheet", ".xlr", ".et", ".sdc", ".uos", ".fods", ".dbf", ".slk"],
    "Ebooks": [".epub", ".mobi", ".azw3", ".pdf", ".azw", ".lit", ".prc", ".pdb", ".fb2", ".lrf", 
               ".snb", ".kfx", ".oxps", ".xps", ".cbz", ".cbr", ".iba", ".djvu", ".chm", ".tcr"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2", ".eot", ".fon", ".pfb", ".pfm", ".ttc", ".dfont", 
              ".suit", ".bmap", ".fnt", ".abf", ".pcf", ".snf", ".bdf", ".pfa", ".gsf", ".ufo"],
    "System Files": [".dll", ".sys", ".ini", ".log", ".cfg", ".conf", ".bak", ".tmp", ".temp", ".dmp", 
                     ".reg", ".inf", ".manifest", ".cat", ".drv", ".so", ".ko", ".plist", ".properties", ".lock"],
    "Torrents": [".torrent", ".magnet"],
    "Others": []  # Default category for unknown file types
}

class FileOrganizerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.old_pos = None
        self.click_start_pos = None
        self.is_shrunk = False
        self.shrunk_size = (80, 80)
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(200, 200, 500, 300)
        self.setMinimumSize(400, 250)
        self.main_widget = QWidget(self)
        self.main_widget.setStyleSheet("background-color: rgba(0, 0, 0, 100); border-radius: 10px;")
        self.main_layout = QVBoxLayout(self.main_widget)

        self.title = QLabel("File Organizer", self.main_widget)
        self.title.setFont(QFont("Arial", 20, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            color: white;
            text-shadow: 0 0 5px blue;
            background-color: rgba(0, 0, 0, 150);
            padding: 5px;
            border-radius: 5px;
        """)
        self.main_layout.addWidget(self.title)

        self.folder_layout = QHBoxLayout()
        self.folder_label = QLabel("Select Folder:", self.main_widget)
        self.folder_label.setStyleSheet("color: white; font-size: 14px;")
        self.folder_layout.addWidget(self.folder_label)

        self.folder_input = QLineEdit(self.main_widget)
        self.folder_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(0, 0, 0, 150);
                color: white;
                border: 2px solid blue;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        self.folder_layout.addWidget(self.folder_input)

        self.browse_btn = QPushButton("Browse", self.main_widget)
        self.browse_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 150);
                border: 2px solid blue;
                color: white;
                font-size: 14px;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgba(30, 144, 255, 200);
            }
        """)
        self.browse_btn.clicked.connect(self.browse_directory)
        self.folder_layout.addWidget(self.browse_btn)
        self.main_layout.addLayout(self.folder_layout)

        self.organize_btn = QPushButton("Organize Files", self.main_widget)
        self.organize_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 255, 0, 150);
                border: 2px solid green;
                color: white;
                font-size: 16px;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgba(0, 255, 0, 200);
            }
        """)
        self.organize_btn.clicked.connect(self.start_organizing)
        self.main_layout.addWidget(self.organize_btn)

        self.btn_layout = QHBoxLayout()

        self.shrink_btn = QPushButton("Shrink", self.main_widget)
        self.shrink_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 150);
                border: 2px solid blue;
                color: white;
                font-size: 14px;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgba(128, 0, 128, 200);
            }
        """)
        self.shrink_btn.clicked.connect(self.toggle_shrink)
        self.btn_layout.addWidget(self.shrink_btn)

        self.close_btn = QPushButton("Close", self.main_widget)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 0, 0, 150);
                border: 2px solid red;
                color: white;
                font-size: 14px;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 200);
            }
        """)
        self.close_btn.clicked.connect(self.close)
        self.btn_layout.addWidget(self.close_btn)

        self.main_layout.addLayout(self.btn_layout)

        self.main_widget.setLayout(self.main_layout)
        self.main_widget.resize(self.size())

        self.animation_radius = 30
        self.animation_step = 2
        QTimer(self, timeout=self.update_animation).start(50)

        self.original_geometry = self.geometry()

    def update_animation(self):
        if not self.is_shrunk:
            self.animation_radius += self.animation_step
            if self.animation_radius >= 40 or self.animation_radius <= 20:
                self.animation_step = -self.animation_step
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(30, 144, 255, 200), 2))
        if self.is_shrunk:
            painter.setBrush(QColor(0, 0, 0, 150))
            painter.drawEllipse(0, 0, self.shrunk_size[0], self.shrunk_size[1])
        else:
            painter.drawRoundedRect(0, 0, self.width(), self.height(), 10, 10)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            child = self.childAt(pos)
            is_over_button = child in (self.browse_btn, self.organize_btn, self.shrink_btn, self.close_btn)
            
            if not is_over_button:
                self.old_pos = event.globalPos()
                self.click_start_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos is not None:
            child = self.childAt(event.pos())
            is_over_button = child in (self.browse_btn, self.organize_btn, self.shrink_btn, self.close_btn)
            
            if not is_over_button:
                delta = event.globalPos() - self.old_pos
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.old_pos = event.globalPos()
        
        if self.is_shrunk:
            self.setCursor(Qt.OpenHandCursor)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_shrunk:
            if self.click_start_pos is not None:
                delta = event.globalPos() - self.click_start_pos
                if abs(delta.x()) < 5 and abs(delta.y()) < 5:
                    self.toggle_shrink()
            self.old_pos = None
            self.click_start_pos = None
        self.old_pos = None

    def toggle_shrink(self):
        if self.is_shrunk:
            self.setGeometry(self.original_geometry)
            self.main_widget.show()
            self.shrink_btn.setText("Shrink")
            self.is_shrunk = False
            self.main_widget.resize(self.size())
        else:
            self.original_geometry = self.geometry()
            self.resize(*self.shrunk_size)
            self.main_widget.hide()
            self.shrink_btn.setText("Expand")
            self.is_shrunk = True
        self.update()

    def browse_directory(self):
        if not self.is_shrunk:  
            folder_selected = QFileDialog.getExistingDirectory(self, "Select Directory")
            if folder_selected:
                self.folder_input.setText(folder_selected)

    def start_organizing(self):
        if self.is_shrunk:
            return 
        
        directory = self.folder_input.text()
        if not directory:
            QMessageBox.critical(self, "Error", "Please select a folder!")
            return
        
        if not os.path.exists(directory):
            QMessageBox.critical(self, "Error", "Directory does not exist!")
            return

        # File organization logic
        file_list = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        for file in file_list:
            file_path = os.path.join(directory, file)
            file_extension = os.path.splitext(file)[1].lower()

            folder_name = "Others"
            target_path = None

            # Handle programming files separately
            if isinstance(FILE_TYPE["Programming"], dict) and file_extension in FILE_TYPE["Programming"]:
                folder_name = "Programming"
                subfolder_name = FILE_TYPE["Programming"][file_extension]
                folder_path = os.path.join(directory, folder_name, subfolder_name)
                target_path = os.path.join(folder_path, file)
            else:
                # Handle other file types
                for category, extensions in FILE_TYPE.items():
                    if category != "Programming" and file_extension in extensions:
                        folder_name = category
                        break
                folder_path = os.path.join(directory, folder_name)
                target_path = os.path.join(folder_path, file)

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            shutil.move(file_path, target_path)

        QMessageBox.information(self, "Success", "Files organized successfully!")

def main():
    app = QApplication(sys.argv)
    window = FileOrganizerGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
