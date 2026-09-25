
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QCheckBox, QFrame
)
from PyQt6.QtCore import QSettings
from PyQt6.QtGui import QFont
from downloader import download_media


STYLE = """
QWidget {
    background: #121212;
    color: #eeeeee;
    font-family: Segoe UI;
    font-size: 14px;
}

QLineEdit {
    background: #1e1e1e;
    border: 1px solid #444;
    border-radius: 8px;
    padding: 12px;
}

QCheckBox {
    padding: 8px;
}

QPushButton {
    background: #2563eb;
    border-radius: 10px;
    padding: 12px;
    font-weight: bold;
}

QPushButton:hover {
    background: #1d4ed8;
}

QFrame {
    border-radius: 12px;
    background: #181818;
}
"""


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.settings = QSettings(
            "UniversalMediaArchiver",
            "Preferences"
        )

        self.setWindowTitle(
            "🎬 Universal Media Archiver"
        )
        self.resize(650, 430)
        self.setStyleSheet(STYLE)

        main = QVBoxLayout()

        title = QLabel(
            "🎬 Universal Media Archiver"
        )
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setAlignment(
            __import__("PyQt6").QtCore.Qt.AlignmentFlag.AlignCenter
        )

        subtitle = QLabel(
            "YouTube • Instagram • TikTok • Media Downloader"
        )

        self.url = QLineEdit()
        self.url.setPlaceholderText(
            "Video veya gönderi linkini yapıştırın..."
        )

        card = QFrame()
        card_layout = QVBoxLayout()

        self.thumbnail = QCheckBox(
            "🖼 Thumbnail indir"
        )

        self.video = QCheckBox(
            "🎥 Video / Fotoğraf indir"
        )

        self.text = QCheckBox(
            "📄 Metadata TXT indir"
        )

        self.load_settings()

        card_layout.addWidget(self.thumbnail)
        card_layout.addWidget(self.video)
        card_layout.addWidget(self.text)
        card.setLayout(card_layout)

        self.button = QPushButton(
            "⬇ İndir"
        )

        self.status = QLabel(
            "Hazır"
        )

        self.button.clicked.connect(
            self.start
        )

        main.addWidget(title)
        main.addWidget(subtitle)
        main.addWidget(self.url)
        main.addWidget(card)
        main.addWidget(self.button)
        main.addWidget(self.status)

        self.setLayout(main)


    def load_settings(self):
        self.thumbnail.setChecked(
            self.settings.value(
                "thumbnail", True, type=bool
            )
        )
        self.video.setChecked(
            self.settings.value(
                "video", True, type=bool
            )
        )
        self.text.setChecked(
            self.settings.value(
                "text", True, type=bool
            )
        )


    def save_settings(self):
        self.settings.setValue(
            "thumbnail",
            self.thumbnail.isChecked()
        )
        self.settings.setValue(
            "video",
            self.video.isChecked()
        )
        self.settings.setValue(
            "text",
            self.text.isChecked()
        )


    def start(self):
        try:
            self.save_settings()
            self.button.setEnabled(False)
            self.status.setText(
                "⏳ İndiriliyor..."
            )

            download_media(
                self.url.text(),
                download_video=self.video.isChecked(),
                download_thumbnail=self.thumbnail.isChecked(),
                create_text=self.text.isChecked()
            )

            self.status.setText(
                "✅ Tamamlandı"
            )

        except Exception as e:
            self.status.setText(
                f"❌ {e}"
            )

        finally:
            self.button.setEnabled(True)


app = QApplication(sys.argv)

window = App()
window.show()

sys.exit(app.exec())
