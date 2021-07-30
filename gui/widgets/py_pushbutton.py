from qt_core import *
from gui.gui_constants import Color, Dimension


class LeftMenuPushButton(QPushButton):
    def __init__(
        self,
        text: str="", 
        height: int=40, 
        minimum_width: int=50, 
        text_padding: int=55, 
        text_color: str=Color.BTN_TEXT, 
        icon_path: str="", 
        icon_color: str="#c3ccdf",
        btn_color: str=Color.BTN_BG, 
        btn_hover: str=Color.BTN_HOVER,
        btn_pressed :str=Color.BTN_PRESSED,
        is_active: bool= False
    ):
        super().__init__()

        # Set default parameters
        self.setText(text)
        self.setMaximumHeight(height)
        self.setMinimumHeight(height)
        self.setCursor(Qt.PointingHandCursor)

        # Custom parameters
        self.minimum_width = minimum_width
        self.text_padding = text_padding
        self.icon_path = icon_path
        self.text_color = text_color
        self.icon_color = icon_color
        self.btn_color = btn_color
        self.btn_hover = btn_hover
        self.btn_pressed = btn_pressed
        self.is_active = is_active

        # Set stylesheet according to what we've entered.
        self.set_style()

    def set_style(self):
        stylesheet_str = f"""
        QPushButton {{
            color: {self.text_color};
            background-color: {self.btn_color};
            padding-left: {self.text_padding}px;
            text-align: left;
            border: none;
        }}

        QPushButton:hover {{
            background-color: {self.btn_hover};
        }}
        
        QPushButton:pressed {{
            background-color: {self.btn_pressed};
        }}
        """

        active_str =f"""
        QPushButton {{
            background-color: {self.btn_hover};
            border-right: 5px solid #282a36;
        }}
        """

        if not self.is_active:
            self.setStyleSheet(stylesheet_str)
        else:
            self.setStyleSheet(stylesheet_str + active_str)
