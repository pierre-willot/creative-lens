import time
import numpy as np
from .importers.psd import PSDImporter
from .importers.clip import ClipImporter
from config import IO

class ParserFactory:
    def __init__(self):
        self.importers = [PSDImporter(), ClipImporter()]

    def get_importer(self, path: str):
        for importer in self.importers:
            if importer.can_handle(path):
                return importer
        return None

    def extract_with_retry(self, path: str) -> np.ndarray:
        importer = self.get_importer(path)
        if not importer:
            raise ValueError(f"No valid importer found for {path}")
            
        last_exception = None
        for _ in range(IO["max_retries"]):
            try:
                return importer.extract_image(path)
            except Exception as e:
                last_exception = e
                time.sleep(IO["retry_delay_sec"])
                
        raise RuntimeError(f"Failed to extract image after {IO['max_retries']} retries: {last_exception}")
