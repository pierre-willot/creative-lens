import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).parent.absolute()
ASSETS_DIR = BASE_DIR / "assets"

# Colors
COLORS = {
    "bg_main": "#2b2b2b",
    "bg_preview": "#1a1a1a",
    "border_normal": "#444",
    "border_preview": "#333",
    "text_light": "#aaa",
    "text_white": "white",
    "btn_bg_hover": "#444",
    "btn_action_bg": "#444",
    "btn_action_hover": "#555",
}

# Window configuration
WINDOW = {
    "min_width": 300,
    "min_height": 400,
    "border_width": 5,
    "corner_radius": 10,
}

# IO Processing Config
IO = {
    "debounce_time_ms": 500,
    "max_retries": 5,
    "retry_delay_sec": 0.2,
    "clip_sqlite_query": "SELECT ImageData FROM CanvasPreview LIMIT 1",
}
