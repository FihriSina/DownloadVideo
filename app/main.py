import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from downloader import download_media


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Universal Media Archiver")
        self.resize(600, 200)

        layout = VVBoxLayout = QVBoxLayout()
        self.url = QLineEdit()
        self.url.setPlaceholderText("Video veya gönderi linkini yapıştırın")
        self.button = QPushButton("İndir")
        self.status = QLabel("")

        self.button.clicked.connect(self.start)

        layout.addWidget(self.url)
        layout.addWidget(self.button)
        layout.addWidget(self.status)
        self.setLayout(layout)

    def start(self):
        try:
            self.status.setText("İndiriliyor...")
            download_media(self.url.text())
            self.status.setText("Tamamlandı")
        except Exception as e:
            self.status.setText(str(e))


app = QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec())
