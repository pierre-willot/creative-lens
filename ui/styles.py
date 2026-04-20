from config import COLORS, WINDOW

MAIN_WINDOW_STYLE = f"""
    QMainWindow {{ 
        background-color: {COLORS['bg_main']}; 
        border: 1px solid {COLORS['border_normal']}; 
    }}
    QLabel {{ 
        color: {COLORS['text_light']}; 
        font-family: 'Segoe UI', sans-serif; 
    }}
"""

TITLE_BTN_STYLE = f"""
    QPushButton {{ 
        background-color: transparent; 
        border: none; 
        color: {COLORS['text_light']};
        font-family: 'Segoe UI Symbol'; 
        font-size: 14px; 
        padding: 5px 12px;
    }}
    QPushButton:hover {{ 
        background-color: {COLORS['btn_bg_hover']}; 
        color: {COLORS['text_white']}; 
    }}
"""

ACTION_BTN_STYLE = f"""
    QPushButton {{ 
        background-color: {COLORS['btn_action_bg']}; 
        color: {COLORS['text_white']}; 
        border-radius: 3px; 
        padding: 10px; 
        border: 1px solid {COLORS['border_normal']}; 
        font-weight: bold;
    }}
    QPushButton:hover {{ 
        background-color: {COLORS['btn_action_hover']}; 
    }}
"""

PREVIEW_LABEL_STYLE = f"""
    QLabel {{
        background-color: {COLORS['bg_preview']}; 
        border-radius: {WINDOW['corner_radius']}px; 
        border: 1px solid {COLORS['border_preview']};
    }}
"""
