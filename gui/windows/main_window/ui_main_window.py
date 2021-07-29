import logging

from qt_core import *

log = logging.getLogger("inventory_qt.ui_main_window")

TOP_BAR_HEIGHT = 50
LEFT_MENU_WIDTH = 50
BOTTOM_BAR_HEIGHT = 30

class UIMainWindow(object):
    """A class to hold the main window widgets."""
    def setup_ui(self, parent: QMainWindow):
        log.debug("Naming this window if it doesn't have a name.")
        if not parent.objectName():
            parent.setObjectName("MainWindow")
        
        # Setting the initial geometry
        parent.resize(800, 450)
        parent.setMinimumSize(QSize(800, 450))
        parent.setMaximumSize(QSize(1920, 1080))

        # Main frame
        self.central_widget = QFrame()
        self.central_widget.setStyleSheet("background-color: #e6e6e6;")
        # A layout child of this central widget frame.
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Left menu frame
        self.left_menu = QFrame()
        self.left_menu.setStyleSheet("background-color: #80ffb3;")
        self.left_menu.setMaximumWidth(LEFT_MENU_WIDTH)
        self.left_menu.setMinimumWidth(LEFT_MENU_WIDTH)

        # Content frame
        self.content = QFrame()
        self.content.setStyleSheet("background-color: #e6e6e6;")

        # Content layout
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)


        # Top bar frame
        self.top_bar = QFrame()
        self.top_bar.setStyleSheet("background-color: #d7eef4; color: #005544; font: 75 25pt 'Segoe UI';")

        # Pages widget
        self.pages = QStackedWidget()
        self.pages.setStyleSheet("font-size: 12pt; color: #0b2817;")

        # Bot bar frame
        self.bot_bar = QFrame()
        self.bot_bar.setStyleSheet("background-color: #d7eef4; color: #005544; font: 75 14pt 'Segoe UI';")

        # Adding top bar, stacked widget and bot bar.
        self.content_layout.addWidget(self.top_bar)
        self.content_layout.addWidget(self.pages)
        self.content_layout.addWidget(self.bot_bar)
        
        # Adding left_menu and content frames to the main_layout
        self.main_layout.addWidget(self.left_menu)
        self.main_layout.addWidget(self.content)
        

        

        # Set the main frame as central widget
        parent.setCentralWidget(self.central_widget)


