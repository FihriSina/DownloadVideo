import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QCheckBox
)
from PyQt6.QtCore import QSettings
from downloader import download_media


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.settings = QSettings("UniversalMediaArchiver", "Preferences")

        self.setWindowTitle("Universal Media Archiver")
        self.resize(600, 300)

        layout = QVBoxLayout()

        self.url = QLineEdit()
        self.url.setPlaceholderText("Video veya gönderi linkini yapıştırın")

        self.thumbnail = QCheckBox("Thumbnail indir")
        self.video = QCheckBox("Video / Fotoğraf indir")
        self.text = QCheckBox("Metadata TXT indir")

        self.load_settings()

        self.button = QPushButton("⬇ İndir")
        self.status = QLabel("")

        self.button.clicked.connect(self.start)

        layout.addWidget(self.url)
        layout.addWidget(self.thumbnail)
        layout.addWidget(self.video)
        layout.addWidget(self.text)
        layout.addWidget(self.button)
        layout.addWidget(self.status)

        self.setLayout(layout)

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
            self.status.setText("İndiriliyor...")

            download_media(
                self.url.text(),
                download_video=self.video.isChecked(),
                download_thumbnail=self.thumbnail.isChecked(),
                create_text=self.text.isChecked()
            )

            self.status.setText("Tamamlandı")

        except Exception as e:
            self.status.setText(str(e))


app = QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec())
