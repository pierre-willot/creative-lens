import cv2
import numpy as np

def apply_notan(image: np.ndarray) -> np.ndarray:
    """
    Applies the Notan filter: Median Blur -> Otsu Threshold
    Expects a grayscale numpy array.
    """
    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    blurred = cv2.medianBlur(image, 11)
    _, notan = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return notan

# Filter Registry
FILTERS = {
    "notan": apply_notan
}
