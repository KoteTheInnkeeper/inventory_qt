from qt_core import *
from gui.gui_constants import *


class FormLineEdit(QLineEdit):
    def __init__(
        self,
        width: int=Dimension.LINE_EDIT_DEF_WIDTH,
        height: int=Dimension.LINE_EDIT_DEF_HEIGHT,
        visibility: bool=True
    ):
        super().__init__()

        self.width, self.height = width, height
        self.is_visible = visibility

        self.setVisible(self.is_visible)

