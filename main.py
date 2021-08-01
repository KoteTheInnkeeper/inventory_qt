import sys
import logging

# Erasing previous log
with open('log.log', 'w'):
    pass


# Setting logger.
logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s", level=logging.DEBUG,
                    filename='log.log')

log = logging.getLogger("inventory_qt")

from qt_core import *
from gui.windows.main_window.ui_main_window import UIMainWindow
from gui.gui_constants import *

# Database imports
from data.data import Database

# Main window, the one we show.

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setting the title
        self.setWindowTitle("Inventory")
        self.setWindowIcon(QIcon('gui/windows/main_window/main_icon.png'))

        # Setting up the main window
        self.ui = UIMainWindow()
        self.ui.setup_ui(self)
        
        # Toggle menu button
        self.ui.toggle_btn.clicked.connect(self.show_menu)

        # Signals for each button to be clicked
        self.ui.sell_btn.clicked.connect(self.show_sell)
        self.ui.stock_btn.clicked.connect(self.show_stock)
        self.ui.about_btn.clicked.connect(self.show_about)
     
        # Showing
        self.show()
    
    def show_menu(self):
        """An animation to show the left menu."""
        # Get the current left menu's width.
        menu_width = self.ui.left_menu.width()

        width = Dimension.LEFT_MENU_WIDTH
        if menu_width == 50:
            width = 200
        
        # Start animation
        self.animation = QPropertyAnimation(self.ui.left_menu, b"minimumWidth")
        self.animation.setStartValue(menu_width)
        self.animation.setEndValue(width)
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.InOutCirc)
        self.animation.start()

    def show_sell(self):
        """Display the first page."""
        self.ui.top_label_left.setText("Sell")
        self.ui.pages.setCurrentWidget(self.ui.ui_pages.sell_page)

    def show_stock(self):
        """Display stock page."""
        self.ui.top_label_left.setText("Stock")
        self.ui.pages.setCurrentWidget(self.ui.ui_pages.stock_page)
    
    def show_about(self):
        """Display about page."""
        self.ui.top_label_left.setText("About")
        self.ui.pages.setCurrentWidget(self.ui.ui_pages.about_page)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

