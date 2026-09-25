import sys
from pathlib import Path

from PyQt6.QtCore import Qt, QPoint, QSettings, QPropertyAnimation, QEasingCurve, QEvent
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame,
    QLineEdit, QPushButton, QSizePolicy, QMessageBox
)

from downloader import download_media

LIGHT_STYLE = """
QWidget {
    background: transparent;
    color: #0f172a;
    font-family: "Segoe UI";
}

QFrame#outerPanel {
    background: transparent;
}

QFrame#mainPanel {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 36px;
}

QLabel#panelTitle {
    color: #0f172a;
    font-size: 30px;
    font-weight: 700;
    background: transparent;
}

QLabel#panelSubtitle {
    color: #64748b;
    font-size: 14px;
    background: transparent;
}

QLabel#statusLabel {
    color: #475569;
    font-size: 13px;
    background: transparent;
}

QLineEdit {
    background: #ffffff;
    border: 1px solid #cfd8e3;
    border-radius: 22px;
    padding: 14px 18px;
    color: #0f172a;
    font-size: 14px;
}

QLineEdit:focus {
    border: 1px solid #2563eb;
}

QPushButton#downloadButton {
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 20px;
    padding: 14px 26px;
    font-size: 14px;
    font-weight: 700;
}

QPushButton#downloadButton:hover {
    background: #1d4ed8;
}

QPushButton#themeButton {
    background: #f1f5f9;
    color: #0f172a;
    border: 1px solid #dbe3ee;
    border-radius: 18px;
    padding: 10px 18px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton#themeButton:hover {
    background: #e8eef7;
}

QPushButton#optionButton {
    background: #ffffff;
    color: #0f172a;
    border: 1px solid #d6deea;
    border-radius: 20px;
    padding: 12px 18px;
    font-size: 14px;
    font-weight: 600;
}

QPushButton#optionButton:hover {
    border: 1px solid #8fb1ff;
    background: #f8fbff;
}

QPushButton#optionButton:checked {
    background: #eff6ff;
    color: #0f172a;
    border: 1px solid #4f8dff;
}

QFrame#titleBar {
    background: transparent;
}

QPushButton#minButton, QPushButton#maxButton, QPushButton#closeButton {
    background: #eef2f7;
    color: #0f172a;
    border: none;
    border-radius: 17px;
    font-size: 14px;
    font-weight: 700;
}

QPushButton#minButton:hover, QPushButton#maxButton:hover {
    background: #dfe7f3;
}

QPushButton#closeButton:hover {
    background: #ef4444;
    color: white;
}
"""

DARK_STYLE = """
QWidget {
    background: transparent;
    color: #e5edf7;
    font-family: "Segoe UI";
}

QFrame#outerPanel {
    background: transparent;
}

QFrame#mainPanel {
    background: #0f172a;
    border: 1px solid #1f2a44;
    border-radius: 36px;
}

QLabel#panelTitle {
    color: #f8fafc;
    font-size: 30px;
    font-weight: 700;
    background: transparent;
}

QLabel#panelSubtitle {
    color: #94a3b8;
    font-size: 14px;
    background: transparent;
}

QLabel#statusLabel {
    color: #a5b4cc;
    font-size: 13px;
    background: transparent;
}

QLineEdit {
    background: #111c31;
    border: 1px solid #28406b;
    border-radius: 22px;
    padding: 14px 18px;
    color: #f8fafc;
    font-size: 14px;
}

QLineEdit:focus {
    border: 1px solid #4f8dff;
}

QPushButton#downloadButton {
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 20px;
    padding: 14px 26px;
    font-size: 14px;
    font-weight: 700;
}

QPushButton#downloadButton:hover {
    background: #3b82f6;
}

QPushButton#themeButton {
    background: #111c31;
    color: #f8fafc;
    border: 1px solid #2b3a59;
    border-radius: 18px;
    padding: 10px 18px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton#themeButton:hover {
    background: #18233a;
}

QPushButton#optionButton {
    background: #111827;
    color: #e5edf7;
    border: 1px solid #2c3a57;
    border-radius: 20px;
    padding: 12px 18px;
    font-size: 14px;
    font-weight: 600;
}

QPushButton#optionButton:hover {
    border: 1px solid #5b8cff;
    background: #152036;
}

QPushButton#optionButton:checked {
    background: #132342;
    color: #ffffff;
    border: 1px solid #4f8dff;
}

QFrame#titleBar {
    background: transparent;
}

QPushButton#minButton, QPushButton#maxButton, QPushButton#closeButton {
    background: #1a2740;
    color: #f8fafc;
    border: none;
    border-radius: 17px;
    font-size: 14px;
    font-weight: 700;
}

QPushButton#minButton:hover, QPushButton#maxButton:hover {
    background: #243554;
}

QPushButton#closeButton:hover {
    background: #ef4444;
    color: white;
}
"""


class TopBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.drag_pos = None
        self.setObjectName("titleBar")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        layout.addStretch()

        self.theme_btn = QPushButton()
        self.theme_btn.setObjectName("themeButton")
        self.theme_btn.setFixedHeight(38)
        self.theme_btn.setMinimumWidth(126)
        layout.addWidget(self.theme_btn)

        self.min_btn = QPushButton("–")
        self.min_btn.setObjectName("minButton")
        self.min_btn.setFixedSize(34, 34)
        self.min_btn.clicked.connect(self.parent_window.showMinimized)

        self.max_btn = QPushButton("⬜")
        self.max_btn.setObjectName("maxButton")
        self.max_btn.setFixedSize(34, 34)
        self.max_btn.clicked.connect(self.parent_window.toggle_max_restore)

        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("closeButton")
        self.close_btn.setFixedSize(34, 34)
        self.close_btn.clicked.connect(self.parent_window.close)

        layout.addWidget(self.min_btn)
        layout.addWidget(self.max_btn)
        layout.addWidget(self.close_btn)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.parent_window.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.drag_pos is not None and event.buttons() & Qt.MouseButton.LeftButton:
            if self.parent_window.isMaximized():
                self.parent_window.showNormal()
                self.drag_pos = QPoint(self.width() // 2, 16)
            self.parent_window.move(event.globalPosition().toPoint() - self.drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None
        event.accept()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.parent_window.toggle_max_restore()
            event.accept()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("UniversalMediaArchiver", "Preferences")
        self.dark_mode = self.settings.value("dark_mode", False, type=bool)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMinimumSize(760, 520)
        self.resize(920, 610)

        icon_path = Path(__file__).resolve().parent.parent / "assets" / "app_icon.svg"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self.root_layout = QVBoxLayout(self)
        self.root_layout.setSpacing(0)
        self.root_layout.setContentsMargins(10, 10, 10, 10)

        self.outer = QFrame()
        self.outer.setObjectName("outerPanel")
        outer_layout = QVBoxLayout(self.outer)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        self.main_panel = QFrame()
        self.main_panel.setObjectName("mainPanel")
        self.main_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        panel_layout = QVBoxLayout(self.main_panel)
        panel_layout.setContentsMargins(30, 24, 30, 30)
        panel_layout.setSpacing(0)

        self.top_bar = TopBar(self)
        self.top_bar.theme_btn.clicked.connect(self.toggle_theme)
        panel_layout.addWidget(self.top_bar)

        panel_layout.addSpacing(32)

        self.panel_title = QLabel("Universal Media Archiver")
        self.panel_title.setObjectName("panelTitle")
        self.panel_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(self.panel_title)

        panel_layout.addSpacing(10)

        self.panel_subtitle = QLabel("Download and archive videos, images, thumbnails and metadata")
        self.panel_subtitle.setObjectName("panelSubtitle")
        self.panel_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(self.panel_subtitle)

        panel_layout.addSpacing(28)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("🔗 Paste your media URL")
        self.url_input.setFixedHeight(50)
        panel_layout.addWidget(self.url_input)

        panel_layout.addSpacing(26)

        options_row = QHBoxLayout()
        options_row.setSpacing(12)
        options_row.addStretch()
        self.thumbnail_btn = self._make_option_button("✓  🖼  Thumbnail")
        self.video_btn = self._make_option_button("✓  🎥  Video / Images")
        self.metadata_btn = self._make_option_button("✓  📄  Metadata")
        options_row.addWidget(self.thumbnail_btn)
        options_row.addWidget(self.video_btn)
        options_row.addWidget(self.metadata_btn)
        options_row.addStretch()
        panel_layout.addLayout(options_row)

        panel_layout.addSpacing(30)

        action_row = QHBoxLayout()
        action_row.addStretch()
        self.download_btn = QPushButton("⬇  DOWNLOAD")
        self.download_btn.setObjectName("downloadButton")
        self.download_btn.setFixedSize(220, 48)
        self.download_btn.clicked.connect(self.start_download)
        action_row.addWidget(self.download_btn)
        action_row.addStretch()
        panel_layout.addLayout(action_row)

        panel_layout.addSpacing(26)

        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(self.status_label)
        panel_layout.addStretch()

        outer_layout.addWidget(self.main_panel)
        self.root_layout.addWidget(self.outer)

        self.load_preferences()
        self.update_theme_button_text()
        self.apply_theme(initial=True)
        self.animate_in()

    def _make_option_button(self, text):
        btn = QPushButton(text)
        btn.setObjectName("optionButton")
        btn.setCheckable(True)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumWidth(170)
        btn.setFixedHeight(42)
        return btn

    def load_preferences(self):
        self.thumbnail_btn.setChecked(self.settings.value("download_thumbnail", True, type=bool))
        self.video_btn.setChecked(self.settings.value("download_video", True, type=bool))
        self.metadata_btn.setChecked(self.settings.value("create_text", True, type=bool))

    def save_preferences(self):
        self.settings.setValue("download_thumbnail", self.thumbnail_btn.isChecked())
        self.settings.setValue("download_video", self.video_btn.isChecked())
        self.settings.setValue("create_text", self.metadata_btn.isChecked())
        self.settings.setValue("dark_mode", self.dark_mode)

    def update_theme_button_text(self):
        self.top_bar.theme_btn.setText("☀ Light Mode" if self.dark_mode else "🌙 Dark Mode")

    def apply_theme(self, initial=False):
        self.setStyleSheet(DARK_STYLE if self.dark_mode else LIGHT_STYLE)
        self.update_theme_button_text()
        if not initial:
            self.animate_fade()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.save_preferences()
        self.apply_theme()

    def animate_in(self):
        self.setWindowOpacity(0.0)
        self._fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self._fade_anim.setDuration(220)
        self._fade_anim.setStartValue(0.0)
        self._fade_anim.setEndValue(1.0)
        self._fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._fade_anim.start()

    def animate_fade(self):
        self._theme_anim = QPropertyAnimation(self, b"windowOpacity")
        self._theme_anim.setDuration(140)
        self._theme_anim.setStartValue(0.92)
        self._theme_anim.setEndValue(1.0)
        self._theme_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._theme_anim.start()

    def toggle_max_restore(self):
        if self.isMaximized():
            self.showNormal()
            self.top_bar.max_btn.setText("⬜")
            self.root_layout.setContentsMargins(10, 10, 10, 10)
        else:
            self.showMaximized()
            self.top_bar.max_btn.setText("❐")
            self.root_layout.setContentsMargins(0, 0, 0, 0)

    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            if self.isMaximized():
                self.top_bar.max_btn.setText("❐")
                self.root_layout.setContentsMargins(0, 0, 0, 0)
            else:
                self.top_bar.max_btn.setText("⬜")
                self.root_layout.setContentsMargins(10, 10, 10, 10)
        super().changeEvent(event)

    def start_download(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Missing URL", "Please paste a media URL first.")
            return
        if not any([self.thumbnail_btn.isChecked(), self.video_btn.isChecked(), self.metadata_btn.isChecked()]):
            QMessageBox.warning(self, "No option selected", "Please select at least one download option.")
            return

        self.save_preferences()
        self.download_btn.setEnabled(False)
        self.status_label.setText("⏳ Downloading...")
        QApplication.processEvents()
        try:
            download_media(
                url,
                download_video=self.video_btn.isChecked(),
                download_thumbnail=self.thumbnail_btn.isChecked(),
                create_text=self.metadata_btn.isChecked(),
            )
            self.status_label.setText("✅ Completed")
        except Exception as exc:
            self.status_label.setText(f"❌ {exc}")
        finally:
            self.download_btn.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Universal Media Archiver")
    window = App()
    window.show()
    sys.exit(app.exec())
