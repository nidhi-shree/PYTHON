import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from pytube import YouTube

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Video Downloader")
        self.setGeometry(400, 400, 400, 200)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Label
        self.label = QLabel("Enter YouTube URL:")
        layout.addWidget(self.label)

        # URL Input Field
        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)

        # Download Button
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download_video)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

    def download_video(self):
        url = self.url_input.text()
        if not url:
            QMessageBox.warning(self, "Input Error", "Please enter a YouTube URL")
            return

        try:
            yt = YouTube(url)
            # Apply filter for more stability
            stream = yt.streams.filter(progressive=True, file_extension="mp4").first()
            
            if stream:
                stream.download()  # Download the selected stream
                QMessageBox.information(self, "Success", "Video downloaded successfully!")
            else:
                QMessageBox.critical(self, "Error", "No suitable stream found.")
        except Exception as e:
            print(f"An error occurred: {e}")  # Print error for debugging
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec_())


