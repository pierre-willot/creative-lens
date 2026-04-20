import os
import numpy as np
from psd_tools import PSDImage
from .base_importer import BaseImporter

class PSDImporter(BaseImporter):
    @classmethod
    def can_handle(cls, path: str) -> bool:
        return path.lower().endswith('.psd')

    def extract_image(self, path: str) -> np.ndarray:
        psd = PSDImage.open(path)
        pil_img = psd.composite()
        # Convert to Grayscale
        cv_img = np.array(pil_img.convert('L'))
        return cv_img
