import os
import tempfile
import sqlite3
from io import BytesIO
from PIL import Image
import numpy as np
from .base_importer import BaseImporter
from config import IO

class ClipImporter(BaseImporter):
    @classmethod
    def can_handle(cls, path: str) -> bool:
        return path.lower().endswith('.clip')

    def extract_image(self, path: str) -> np.ndarray:
        with open(path, 'rb') as f:
            data = f.read()
            
        offset = data.find(b'SQLite format 3')
        if offset == -1:
            raise ValueError("No SQLite database found in .clip file")
            
        tmp_path = ""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite") as tmp:
            tmp.write(data[offset:])
            tmp_path = tmp.name
            
        try:
            with sqlite3.connect(tmp_path) as conn:
                row = conn.execute(IO["clip_sqlite_query"]).fetchone()
                
            if not row:
                raise ValueError("CanvasPreview ImageData not found in .clip file")
                
            pil_img = Image.open(BytesIO(row[0]))
            cv_img = np.array(pil_img.convert('L'))
            return cv_img
        finally:
            if os.path.exists(tmp_path):
                # Using try/except around unlink to ensure cross-platform safety
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass
