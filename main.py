import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from ui.window import CreativeLensApp
from core.processor import ImageProcessor
from io_handlers.watcher import FileWatcher
from config import IO

class ApplicationController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle("Fusion")
        
        self.window = CreativeLensApp()
        self.processor = ImageProcessor()
        self.watcher = None
        
        self.debounce_timer = QTimer()
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.timeout.connect(self._trigger_processing)
        self.pending_path = None

        self._connect_signals()

    def _connect_signals(self):
        self.window.file_selected.connect(self.start_watching)
        self.processor.processing_finished.connect(self.on_processing_finished)

    def start_watching(self, file_path: str):
        if self.watcher:
            self.watcher.stop()
            
        self.watcher = FileWatcher(file_path)
        self.watcher.file_changed.connect(self.on_file_changed)
        self.watcher.start()
        
        self.on_file_changed(file_path)

    def on_file_changed(self, file_path: str):
        self.pending_path = file_path
        self.debounce_timer.start(IO["debounce_time_ms"])

    def _trigger_processing(self):
        if self.pending_path:
            self.processor.process_file(self.pending_path)

    def on_processing_finished(self, image_array, error_msg):
        if error_msg:
            self.window.show_error(error_msg)
        elif image_array is not None:
            self.window.display_image(image_array)

    def run(self):
        self.window.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    controller = ApplicationController()
    controller.run()
