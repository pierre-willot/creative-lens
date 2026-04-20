import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal
from io_handlers.factory import ParserFactory
from .filters import FILTERS

class ImageProcessor(QThread):
    # Emits (processed_image_array, error_message)
    processing_finished = pyqtSignal(object, str)

    def __init__(self):
        super().__init__()
        self.factory = ParserFactory()
        self.current_path = None
        self.active_filter = "notan"
        
    def process_file(self, path: str):
        """Called by the main thread to initiate processing"""
        self.current_path = path
        self.start()

    def set_filter(self, filter_name: str):
        if filter_name in FILTERS:
            self.active_filter = filter_name

    def run(self):
        if not self.current_path:
            return
            
        try:
            raw_image = self.factory.extract_with_retry(self.current_path)
            filter_func = FILTERS.get(self.active_filter)
            if not filter_func:
                raise ValueError(f"Filter '{self.active_filter}' not found in registry")
                
            processed_image = filter_func(raw_image)
            self.processing_finished.emit(processed_image, "")
            
        except Exception as e:
            self.processing_finished.emit(None, str(e))
