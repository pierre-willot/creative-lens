from abc import ABC, abstractmethod
import numpy as np

class BaseImporter(ABC):
    @classmethod
    @abstractmethod
    def can_handle(cls, path: str) -> bool:
        """Returns True if this importer can parse the given file."""
        pass

    @abstractmethod
    def extract_image(self, path: str) -> np.ndarray:
        """Parses the file and returns a grayscale numpy array."""
        pass
