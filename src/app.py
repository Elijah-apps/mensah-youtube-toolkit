from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit,
    QComboBox, QPushButton, QFileDialog, QLabel, QMessageBox,
    QMenuBar, QDialog, QDialogButtonBox, QFormLayout
)
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt
import os
import re
import requests
from pytube import YouTube

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setFixedSize(300, 150)
        layout = QFormLayout()

        # Title
        title = QLabel("<h3>About Mensah YouTube Toolkit</h3>")
        layout.addRow(title)

        # Description
        description = QLabel(
            "Mensah YouTube Toolkit is a tool for downloading YouTube videos, transcripts, audio, and thumbnails.\n"
            "It is designed for convenience and efficiency.\n\n"
            "Developed by Elijah Ekpen Mensah."
        )
        layout.addRow(description)

        # Close button
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addRow(buttons)

        self.setLayout(layout)


class DeveloperDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Meet the Developer")
        self.setFixedSize(300, 150)
        layout = QFormLayout()

        # Title
        title = QLabel("<h3>Meet the Developer</h3>")
        layout.addRow(title)

        # Description
        description = QLabel(
            "Elijah Ekpen Mensah is a developer passionate about creating innovative tools and applications.\n"
            "For more information, visit our website or contact us."
        )
        layout.addRow(description)

        # Close button
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addRow(buttons)

        self.setLayout(layout)


class YouTubeToolKit(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mensah YouTube Toolkit")
        self.setGeometry(100, 100, 600, 300)  # Adjusted height for compact view
        self.setStyleSheet("background-color: #f9f9f9;")
        self.setWindowIcon(QIcon("icon.png"))

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)  # Adjusted spacing

        # Custom font
        font = QFont("Arial", 10)
        self.setFont(font)

        # URL input
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter YouTube URL")
        self.url_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                background-color: #fff;
            }
        """)
        main_layout.addWidget(self.url_input)

        # ComboBox for actions
        self.action_combobox = QComboBox(self)
        self.action_combobox.addItems(["Fetch Video", "Fetch Transcript", "Fetch Audio", "Fetch Thumbnail"])
        self.action_combobox.setStyleSheet("""
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                background-color: #fff;
            }
        """)
        main_layout.addWidget(self.action_combobox)

        # Browse button and directory display
        browse_layout = QVBoxLayout()
        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_directory)
        self.browse_button.setStyleSheet("""
            QPushButton {
                background-color: #ff0000;
                color: #fff;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
        """)
        browse_layout.addWidget(self.browse_button)

        self.directory_label = QLabel("No directory selected", self)
        self.directory_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #333;
            }
        """)
        browse_layout.addWidget(self.directory_label)

        main_layout.addLayout(browse_layout)

        # Download button
        self.download_button = QPushButton("Download", self)
        self.download_button.clicked.connect(self.download_content)
        self.download_button.setStyleSheet("""
            QPushButton {
                background-color: #ff0000;
                color: #fff;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
        """)
        main_layout.addWidget(self.download_button)

        # Menu bar
        menubar = self.menuBar()
        menubar.setStyleSheet("background-color: #ff0000; color: #fff;")
        menu = menubar.addMenu("Menu")
        menu.addAction("Meet Developer").triggered.connect(self.show_meet_developer)
        menu.addAction("About").triggered.connect(self.show_about)

        # Directory path variable
        self.directory_path = ""

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.directory_path = directory
            self.directory_label.setText(f"Selected Directory: {self.directory_path}")

    def download_content(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Input Error", "Please enter a YouTube URL.")
            return

        if not self.directory_path:
            QMessageBox.warning(self, "Directory Error", "Please select a directory.")
            return

        action = self.action_combobox.currentText()
        try:
            yt = YouTube(url)
            # Cleaning video title for a safe filename
            video_title = re.sub(r'[\\/*?:"<>|]', "", yt.title)
            video_title = video_title.encode("ascii", "ignore").decode()

            if action == "Fetch Video":
                stream = yt.streams.get_highest_resolution()
                stream.download(output_path=self.directory_path, filename=f"{video_title}.mp4")
                QMessageBox.information(self, "Download Complete", "Video downloaded successfully.")
            elif action == "Fetch Transcript":
                # Note: Transcript fetching code has been removed as it's not used in the updated example.
                QMessageBox.warning(self, "Feature Not Available", "Transcript fetching is not supported in this version.")
            elif action == "Fetch Audio":
                audio_stream = yt.streams.filter(only_audio=True).first()
                audio_stream.download(output_path=self.directory_path, filename=f"{video_title}.mp3")
                QMessageBox.information(self, "Download Complete", "Audio downloaded successfully.")
            elif action == "Fetch Thumbnail":
                thumbnail_url = yt.thumbnail_url
                thumbnail_response = requests.get(thumbnail_url, stream=True)
                if thumbnail_response.status_code == 200:
                    thumbnail_path = os.path.join(self.directory_path, f"{video_title}.jpg")
                    with open(thumbnail_path, 'wb') as f:
                        f.write(thumbnail_response.content)
                    QMessageBox.information(self, "Download Complete", "Thumbnail downloaded successfully.")
                else:
                    QMessageBox.warning(self, "Download Error", "Failed to download thumbnail.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def show_meet_developer(self):
        dialog = DeveloperDialog(self)
        dialog.exec()

    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication([])
    window = YouTubeToolKit()
    window.show()
    app.exec()
