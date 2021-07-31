import logging

from gui.gui_constants import Color, Dimension
from qt_core import *
from gui.widgets.py_pushbutton import LeftMenuPushButton

log = logging.getLogger("inventory_qt.ui_main_window")


class UIMainWindow(object):
    """A class to hold the main window widgets."""
    def setup_ui(self, parent: QMainWindow):
        log.debug("Naming this window if it doesn't have a name.")
        if not parent.objectName():
            parent.setObjectName("MainWindow")
        
        # Setting the initial geometry
        parent.resize(1024, 576)
        parent.setMinimumSize(QSize(800, 450))
        parent.setMaximumSize(QSize(1920, 1080))

        # Main frame
        self.central_widget = QFrame()
        self.central_widget.setStyleSheet(f"background-color: {Color.CONTENT_BACKGROUND};")
        # A layout child of this central widget frame.
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Left menu frame
        self.left_menu = QFrame()
        self.left_menu.setStyleSheet(f"background-color: {Color.LEFT_MENU};")
        self.left_menu.setMaximumWidth(Dimension.LEFT_MENU_WIDTH)
        self.left_menu.setMinimumWidth(Dimension.LEFT_MENU_WIDTH)
        
        # Left menu layout
        self.left_menu_layout = QVBoxLayout(self.left_menu)
        self.left_menu_layout.setContentsMargins(0, 0, 0, 10)
        self.left_menu_layout.setSpacing(0)

        # Toggle, sell and stock buttons
        self.toggle_btn = LeftMenuPushButton("    Hide menu", icon_path="gui/windows/main_window/toggle_icon_black.png")
        self.home_btn = LeftMenuPushButton("    Home", icon_path="gui/windows/main_window/home_icon_black.png", is_active=True)
        self.stock_btn = LeftMenuPushButton("    Stock", icon_path="gui/windows/main_window/box_icon_black.png")

        # A spacer for the left menu
        self.left_menu_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # A version label
        self.version_label = QLabel("v1.0.0")
        self.version_label.setAlignment(Qt.AlignCenter)
        self.version_label.setStyleSheet(f"color: {Color.BOT_BAR_TEXT}; font: 9pt 'Segoe UI';")

        # Adding elements to the left_menu_layout
        self.left_menu_layout.addWidget(self.toggle_btn)
        self.left_menu_layout.addWidget(self.home_btn)
        self.left_menu_layout.addWidget(self.stock_btn)
        self.left_menu_layout.addItem(self.left_menu_spacer)
        self.left_menu_layout.addWidget(self.version_label)

        # Content frame
        self.content = QFrame()
        self.content.setStyleSheet(f"background-color: {Color.CONTENT_BACKGROUND};")

        # Content layout
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        # Top bar frame
        self.top_bar = QFrame()
        self.top_bar.setMinimumHeight(Dimension.TOP_BAR_HEIGHT)
        self.top_bar.setMaximumHeight(Dimension.TOP_BAR_HEIGHT)
        self.top_bar.setStyleSheet(f"background-color: {Color.TOP_BAR}; color: #162d50;")
        
        # A top bar layout to organize the labels
        self.top_layout = QHBoxLayout(self.top_bar)
        self.top_layout.setContentsMargins(10, 0, 10, 0)
        self.top_layout.setSpacing(0)
        self.top_layout.setAlignment(Qt.AlignVCenter)
        
        # Labels for this top bar
        self.top_label_left = QLabel("Home")
        self.top_label_left.setStyleSheet("font: 75 18pt 'Segoe UI';")
        self.top_label_right = QLabel("| Inventory Project")
        self.top_label_right.setStyleSheet("font: 9pt 'Segoe UI'; text-align: right;")

        # Spacer to put between them
        self.top_spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Adding the spacer and labesl to this top bar
        self.top_layout.addWidget(self.top_label_left)
        self.top_layout.addItem(self.top_spacer)
        self.top_layout.addWidget(self.top_label_right)
        
        # Pages widget
        self.pages = QStackedWidget()
        self.pages.setStyleSheet("font-size: 12pt; color: #0b2817;")

        # Bot bar frame
        self.bot_bar = QFrame()
        self.bot_bar.setMinimumHeight(Dimension.BOTTOM_BAR_HEIGHT)
        self.bot_bar.setMaximumHeight(Dimension.BOTTOM_BAR_HEIGHT)
        self.bot_bar.setStyleSheet(f"background-color: {Color.BOT_BAR}; color: {Color.BOT_BAR_TEXT}; font: 75 14pt 'Segoe UI';")

        # Bot bar layout
        self.bot_layout = QHBoxLayout(self.bot_bar)
        self.bot_layout.setContentsMargins(10, 0, 10, 0)
        self.bot_layout.setSpacing(0)

        # Bot left label
        self.bot_label_left = QLabel("Inventory project by KoteTheInnkeeper")
        self.bot_label_left.setStyleSheet("font: 75 10pt 'Segoe UI';")
        
        # Bot spacer
        self.bot_spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Bot right label
        self.bot_label_right = QLabel("© 2021")
        self.bot_label_right.setStyleSheet("font: 12pt 'Segoe UI';")

        # Adding these last three elements to the bot_layout
        self.bot_layout.addWidget(self.bot_label_left)
        self.bot_layout.addItem(self.bot_spacer)
        self.bot_layout.addWidget(self.bot_label_right)


        # Adding top bar, stacked widget and bot bar.
        self.content_layout.addWidget(self.top_bar)
        self.content_layout.addWidget(self.pages)
        self.content_layout.addWidget(self.bot_bar)
        
        # Adding left_menu and content frames to the main_layout
        self.main_layout.addWidget(self.left_menu)
        self.main_layout.addWidget(self.content)
        

        

        # Set the main frame as central widget
        parent.setCentralWidget(self.central_widget)


