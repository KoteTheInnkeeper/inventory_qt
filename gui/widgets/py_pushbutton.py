import logging
import os

from qt_core import *
from gui.gui_constants import Color, Dimension

from utils.errors import *

log = logging.getLogger("inventory_qt.py_pushbutton")


class LeftMenuPushButton(QPushButton):
    def __init__(
        self,
        text: str="", 
        height: int=40, 
        minimum_width: int=50, 
        text_padding: int=55, 
        text_color: str=Color.BTN_TEXT, 
        icon_path: str="", 
        icon_color: str="black",
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
            font: 75 12pt 'Segoe UI';
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
            border-right: 5px solid {Color.CONTENT_BACKGROUND};
        }}
        """

        if not self.is_active:
            self.setStyleSheet(stylesheet_str)
        else:
            self.setStyleSheet(stylesheet_str + active_str)

    def paintEvent(self, event):
        """Custom paintEvent for this custom button."""
        # Painting button
        log.debug("Inside paint event")
        QPushButton.paintEvent(self, event)

        # Creating a QPainter object
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        qp.setPen(Qt.NoPen)

        # Creating a rectangle for reference for our icon
        rect = QRect(0, 0, self.minimum_width, self.minimumHeight())

        # Drawing the icon
        self.draw_icon(qp, self.icon_path, rect, self.icon_color)

        qp.end()

    def draw_icon(self, qp: QPainter, image: str, rect: QRect, color: str):
        # Formatting the path for the image
        app_path = os.path.abspath(os.getcwd())
        folder = 'gui/images/icons'
        path = os.path.join(app_path, folder)
        icon_path = os.path.normpath(os.path.join(path, image))

        # Drawing the icon
        icon = QPixmap(icon_path)
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(icon.rect(), color)
        
        # Drawing pixmap
        qp.drawPixmap(
            (rect.width() - icon.width()) / 2,
            (rect.height() - icon.height()) / 2,
            icon
        )
        painter.end()

