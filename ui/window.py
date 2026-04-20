from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QFileDialog
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
import numpy as np

from config import WINDOW
from .styles import MAIN_WINDOW_STYLE, ACTION_BTN_STYLE, PREVIEW_LABEL_STYLE
from .widgets import TitleBar

class CreativeLensApp(QMainWindow):
    file_selected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.drag_start_pos = None
        self.init_ui()

    def init_ui(self):
        # Window Flags & Basic Setup
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setMinimumSize(WINDOW["min_width"], WINDOW["min_height"])
        self.setMouseTracking(True)
        self.setStyleSheet(MAIN_WINDOW_STYLE)

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setMouseTracking(True)
        
        # Main Vertical Layout
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # ELIMINATE MARGINS AND SPACING:
        # This ensures the TitleBar touches the top/sides perfectly.
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0) 

        # 1. Title Bar (Fixed at Top)
        self.title_bar = TitleBar(self)
        self.title_bar.setFixedHeight(35) # Ensure consistent height
        self.title_bar.close_requested.connect(self.close)
        self.title_bar.minimize_requested.connect(self.showMinimized)
        self.title_bar.maximize_requested.connect(self.toggle_maximize)
        self.title_bar.pin_toggled.connect(self.toggle_pin)
        
        self.main_layout.addWidget(self.title_bar)

        # 2. Content Container (To add padding back to the inner UI)
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(10, 5, 10, 10)
        self.content_layout.setSpacing(10)

        # Preview Area
        self.preview_label = QLabel("Drop File or Select")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet(PREVIEW_LABEL_STYLE)
        self.content_layout.addWidget(self.preview_label)

        # Open Button
        self.open_btn = QPushButton("Open File")
        self.open_btn.setStyleSheet(ACTION_BTN_STYLE)
        self.open_btn.clicked.connect(self.open_file)
        self.content_layout.addWidget(self.open_btn)

        # Finalize Layout Stretches
        self.main_layout.addWidget(self.content_container)
        self.main_layout.setStretch(0, 0) # Title Bar stays small
        self.main_layout.setStretch(1, 1) # Content fills the rest

    def get_edge(self, pos):
        rect = self.rect()
        edge = Qt.Edge(0)
        bw = WINDOW["border_width"]
        if pos.x() <= bw: edge |= Qt.Edge.LeftEdge
        if pos.x() >= rect.width() - bw: edge |= Qt.Edge.RightEdge
        if pos.y() <= bw: edge |= Qt.Edge.TopEdge
        if pos.y() >= rect.height() - bw: edge |= Qt.Edge.BottomEdge
        return edge

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            edge = self.get_edge(event.pos())
            if edge != Qt.Edge(0):
                self.windowHandle().startSystemResize(edge)
            else:
                # Only allow dragging from the TitleBar area
                if self.title_bar.underMouse():
                    self.drag_start_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        # Cursor Update Logic
        edge = self.get_edge(event.pos())
        if edge == (Qt.Edge.LeftEdge | Qt.Edge.TopEdge) or edge == (Qt.Edge.RightEdge | Qt.Edge.BottomEdge):
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif edge == (Qt.Edge.RightEdge | Qt.Edge.TopEdge) or edge == (Qt.Edge.LeftEdge | Qt.Edge.BottomEdge):
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        elif edge & (Qt.Edge.LeftEdge | Qt.Edge.RightEdge):
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        elif edge & (Qt.Edge.TopEdge | Qt.Edge.BottomEdge):
            self.setCursor(Qt.CursorShape.SizeVerCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

        # Dragging Logic
        if self.drag_start_pos is not None and not self.isMaximized():
            delta = event.globalPosition().toPoint() - self.drag_start_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.drag_start_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.drag_start_pos = None

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
        self.title_bar.set_maximized_state(self.isMaximized())

    def toggle_pin(self, is_pinned: bool):
        # Update flags while preserving current visibility
        is_visible = self.isVisible()
        flags = Qt.WindowType.FramelessWindowHint
        if is_pinned:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        
        self.setWindowFlags(flags)
        if is_visible:
            self.show()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Art Files (*.psd *.clip)")
        if file_path:
            self.file_selected.emit(file_path)

    def display_image(self, cv_img: np.ndarray):
        if cv_img is None:
            return
            
        h, w = cv_img.shape
        q_img = QImage(cv_img.data, w, h, w, QImage.Format.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_img)
        
        # Smoothly scale to fit the label
        scaled = pixmap.scaled(
            self.preview_label.size(), 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        )
        self.preview_label.setPixmap(scaled)

    def show_error(self, message: str):
        self.preview_label.setText(f"Error:\n{message}")