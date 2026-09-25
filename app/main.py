import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtGui import QFont
from downloader import download_media

STYLE = """
QWidget { background:#0f172a; color:#e5e7eb; font-family:Segoe UI; }
QFrame { background:#111827; border:1px solid #24324a; border-radius:16px; }
QLineEdit { background:#0b1220; border:1px solid #2563eb; border-radius:12px; padding:12px; color:white; }
QCheckBox { spacing:8px; }
QPushButton { background:#2563eb; border:none; border-radius:12px; padding:14px; font-weight:bold; color:white; }
QPushButton:hover { background:#1d4ed8; }
QLabel#title { font-size:26px; font-weight:bold; }
QLabel#sub { color:#94a3b8; font-size:13px; }
"""

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("UniversalMediaArchiver", "Preferences")
        self.setWindowTitle("🎬 Universal Media Archiver")
        self.resize(900, 620)
        self.setStyleSheet(STYLE)

        root = QVBoxLayout(self)
        root.setContentsMargins(30,30,30,30)
        root.setSpacing(18)

        title = QLabel("🎬 Universal Media Archiver")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sub = QLabel("Download and preserve videos, images, thumbnails and metadata")
        sub.setObjectName("sub")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.url = QLineEdit()
        self.url.setPlaceholderText("🔗 Paste your media URL...")

        options = QFrame()
        opt = QHBoxLayout(options)

        self.thumbnail = QCheckBox("🖼 Thumbnail")
        self.video = QCheckBox("🎥 Video / Images")
        self.text = QCheckBox("📄 Metadata")
        self.load_settings()

        opt.addWidget(self.thumbnail)
        opt.addWidget(self.video)
        opt.addWidget(self.text)

        self.button = QPushButton("⬇ DOWNLOAD")
        self.status = QLabel("Ready")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        history = QFrame()
        h = QVBoxLayout(history)
        h.addWidget(QLabel("🕘 History"))
        h.addWidget(QLabel("Downloaded files will appear here in future versions."))

        self.button.clicked.connect(self.start)

        root.addWidget(title)
        root.addWidget(sub)
        root.addWidget(self.url)
        root.addWidget(options)
        root.addWidget(self.button)
        root.addWidget(self.status)
        root.addWidget(history)

    def load_settings(self):
        self.thumbnail.setChecked(self.settings.value("thumbnail", True, type=bool))
        self.video.setChecked(self.settings.value("video", True, type=bool))
        self.text.setChecked(self.settings.value("text", True, type=bool))

    def save_settings(self):
        self.settings.setValue("thumbnail", self.thumbnail.isChecked())
        self.settings.setValue("video", self.video.isChecked())
        self.settings.setValue("text", self.text.isChecked())

    def start(self):
        try:
            self.save_settings()
            self.button.setEnabled(False)
            self.status.setText("⏳ Downloading...")
            download_media(
                self.url.text(),
                download_video=self.video.isChecked(),
                download_thumbnail=self.thumbnail.isChecked(),
                create_text=self.text.isChecked()
            )
            self.status.setText("✅ Completed")
        except Exception as e:
            self.status.setText(f"❌ {e}")
        finally:
            self.button.setEnabled(True)

app = QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec())
