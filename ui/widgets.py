from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal
from .styles import TITLE_BTN_STYLE

class TitleBar(QWidget):
    close_requested = pyqtSignal()
    minimize_requested = pyqtSignal()
    maximize_requested = pyqtSignal()
    pin_toggled = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)

        self.pin_btn = QPushButton("📌")
        self.pin_btn.setCheckable(True)
        self.pin_btn.setChecked(True)
        self.pin_btn.setStyleSheet(TITLE_BTN_STYLE)
        self.pin_btn.clicked.connect(self._on_pin_clicked)

        self.min_btn = QPushButton("—")
        self.min_btn.setStyleSheet(TITLE_BTN_STYLE)
        self.min_btn.clicked.connect(self.minimize_requested.emit)

        self.max_btn = QPushButton("◻")
        self.max_btn.setStyleSheet(TITLE_BTN_STYLE)
        self.max_btn.clicked.connect(self.maximize_requested.emit)

        self.close_btn = QPushButton("✕")
        self.close_btn.setStyleSheet(TITLE_BTN_STYLE)
        self.close_btn.clicked.connect(self.close_requested.emit)

        self.layout.addWidget(self.pin_btn)
        self.layout.addStretch()
        self.layout.addWidget(self.min_btn)
        self.layout.addWidget(self.max_btn)
        self.layout.addWidget(self.close_btn)

    def _on_pin_clicked(self):
        is_pinned = self.pin_btn.isChecked()
        self.pin_btn.setText("📌" if is_pinned else "📍")
        self.pin_toggled.emit(is_pinned)

    def set_maximized_state(self, is_maximized: bool):
        self.max_btn.setText("❐" if is_maximized else "◻")
