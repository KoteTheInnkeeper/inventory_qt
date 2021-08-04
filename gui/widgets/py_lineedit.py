from qt_core import *
from gui.gui_constants import *


class FormLineEdit(QLineEdit):
    def __init__(
        self,
        width: int=Dimension.LINE_EDIT_DEF_WIDTH,
        height: int=Dimension.LINE_EDIT_DEF_HEIGHT,
        bg_color: str = Color.LINE_EDIT_DEF_BG_COLOR,
        bg_hover: str = Color.LINE_EDIT_DEF_HOVER_COLOR,
        visibility: bool=True
    ):
        super().__init__()

        self.width, self.height = width, height

        self.is_visible = visibility
        self.bg_color = bg_color
        self.bg_hover = bg_hover
        self.setMinimumHeight(height)
        self.setMinimumWidth(width)

        self.setVisible(self.is_visible)
    
    def set_style(self):
        """Sets a stylesheet"""
        stylesheet_str = f"""
        QLineEdit {{
            background-color: {self.bg_color};
        }}

        QLineEdit:hover {{
            background-color: {self.bg_hover};
        }}
        """

