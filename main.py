import sys
import logging

# Setting logger.
logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s", level=logging.WARNING,
                    filename='log.log')

log = logging.getLogger("inventory_qt")

from qt_core import *
from gui.windows.main_window.ui_main_window import UIMainWindow
from gui.gui_constants import *

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

        

        # Showing
        self.show()
    
    def show_menu(self):
        """An animation to show the left menu."""
        # Get the current left menu's width.
        menu_width = self.ui.left_menu.width()

        width = Dimension.LEFT_MENU_WIDTH
        if menu_width == 50:
            width = 240
        
        # Start animation
        self.animation = QPropertyAnimation(self.ui.left_menu, b"minimumWidth")
        self.animation.setStartValue(menu_width)
        self.animation.setEndValue(width)
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.InOutCirc)
        self.animation.start()

    def show_sell(self):
        """Display the first page."""
        self.ui.sell_btn.is_active = True
        self.ui.pages.currentWidget(self.ui.ui_pages.sell_page)
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
