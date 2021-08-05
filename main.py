import sys
import logging
logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] func:%(funcName)s - %(message)s", level=logging.DEBUG,
                    filename='log.log')
# Erasing previous log
with open('log.log', 'w'):
    pass
# Getting a logger for this file.
log = logging.getLogger("inventory_project")

from qt_core import *
from utils.errors import *

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

db = Database('data.db')


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

        # Signals for each minor button
        self.ui.ui_pages.add_buy_btn.clicked.connect(self.show_add_stock)
        self.ui.ui_pages.show_stock_btn.clicked.connect(self.show_stock_list)

        # Signal for the checkbox
        self.ui.ui_pages.ui_stock_stacked_pages.new_product_checkbox.toggled.connect(self.toggled_new_product_checkbox)

        # Signal for the add product button
        self.ui.ui_pages.ui_stock_stacked_pages.add_product_btn.clicked.connect(self.add_product_to_list)
        # Signal for the clear list button at add stock
        self.ui.ui_pages.ui_stock_stacked_pages.clear_stock_btn.clicked.connect(self.clear_buy_list)

    
        # Showing the sell page first
        self.show_sell()

        # Showing
        self.show()

    def toggled_new_product_checkbox(self, state: bool):
        """To act upon the checkbox being toggled."""
        if state:
            self.ui.ui_pages.ui_stock_stacked_pages.new_product_linedit.setVisible(True)
            self.ui.ui_pages.ui_stock_stacked_pages.set_product_combobox.setVisible(False)
        else:
            self.ui.ui_pages.ui_stock_stacked_pages.new_product_linedit.setVisible(False)
            self.ui.ui_pages.ui_stock_stacked_pages.set_product_combobox.setVisible(True)

        pass

    def clear_btns(self, frame: QFrame):
        """Sets all button's 'is_active' parameter to False."""
        log.debug("Clearing all buttons.")
        for btn in frame.findChildren(QPushButton):
            try:
                btn.set_active(False)
            except Exception:
                log.critical("An exception was raised.")
                raise
    
    def clear_fields(self, frame: QFrame):
        """Clears all the 'QLineEdits on a given frame."""
        log.debug("Clearing all fields.")
        for field in frame.findChildren(QLineEdit):
            try:
                field.clear()
            except Exception:
                log.critical("An exception was raised.")
                raise
        

    def show_menu(self):
        """An animation to show the left menu."""
        menu_width = self.ui.left_menu.width()

        width = Dimension.LEFT_MENU_WIDTH
        if menu_width == 50:
            width = Dimension.LEFT_MENU_EXPANDED_WIDTH
        
        # Start animation
        self.animation = QPropertyAnimation(self.ui.left_menu, b"minimumWidth")
        self.animation.setStartValue(menu_width)
        self.animation.setEndValue(width)
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.InOutCirc)
        self.animation.start()

    def show_sell(self):
        """Display the first page."""
        self.clear_btns(self.ui.left_menu)
        self.ui.sell_btn.set_active(True)
        self.ui.top_label_left.setText("Sell")
        self.ui.pages.setCurrentWidget(self.ui.ui_pages.sell_page)

    def show_stock(self):
        """Display stock page."""
        self.clear_btns(self.ui.left_menu)
        self.ui.stock_btn.set_active(True)
        self.ui.top_label_left.setText("Stock")
        self.ui.pages.setCurrentWidget(self.ui.ui_pages.stock_page)
    
    def show_about(self):
        """Display about page."""
        self.clear_btns(self.ui.left_menu)
        self.ui.about_btn.set_active(True)
        self.ui.top_label_left.setText("About")
        self.ui.pages.setCurrentWidget(self.ui.ui_pages.about_page)

    def show_add_stock(self):
        """"Displays the add stock page."""
        self.clear_btns(self.ui.ui_pages.stock_menu)
        self.ui.ui_pages.add_buy_btn.set_active(True)
        self.ui.ui_pages.stock_stacked_widget.setCurrentWidget(self.ui.ui_pages.ui_stock_stacked_pages.add_buy_page)
    
    def show_stock_list(self):
        """"Displays the add stock page."""
        self.clear_btns(self.ui.ui_pages.stock_menu)
        self.ui.ui_pages.show_stock_btn.set_active(True)
        self.ui.ui_pages.stock_stacked_widget.setCurrentWidget(self.ui.ui_pages.ui_stock_stacked_pages.stock_list)

    def add_product_to_list(self):
        """Adds the product to the list."""
        log.info("An addition of a product to the buy list was issued.")
        # Getting the info from the lineedits/combobox
        if self.ui.ui_pages.ui_stock_stacked_pages.new_product_checkbox.isChecked():
            name = self.ui.ui_pages.ui_stock_stacked_pages.new_product_linedit.text().strip().upper()
            id = "NEW"
        else:
            name = self.ui.ui_pages.ui_stock_stacked_pages.set_product_combobox.currentText().strip().upper()
            id = str(db.get_product_id(name.lower()))
        cost = self.ui.ui_pages.ui_stock_stacked_pages.cost_lineedit.text()
        price = self.ui.ui_pages.ui_stock_stacked_pages.price_lineedit.text()
        units = self.ui.ui_pages.ui_stock_stacked_pages.units_lineedit.text()

        # Writing it to the table       
        id = QTableWidgetItem(id)
        name = QTableWidgetItem(name)
        units = QTableWidgetItem(units)
        cost = QTableWidgetItem(cost)
        price = QTableWidgetItem(price)
        id.setTextAlignment(Qt.AlignCenter)
        name.setTextAlignment(Qt.AlignCenter)
        units.setTextAlignment(Qt.AlignCenter)
        cost.setTextAlignment(Qt.AlignCenter)
        price.setTextAlignment(Qt.AlignCenter)

        log.debug("Writing a product to the add buy table.")
        parameters = (id, name, units,cost, price)
        row = self.ui.ui_pages.ui_stock_stacked_pages.buy_list_table.rowCount()
        self.ui.ui_pages.ui_stock_stacked_pages.buy_list_table.insertRow(row)
        for i, parameter in enumerate(parameters):
            self.ui.ui_pages.ui_stock_stacked_pages.buy_list_table.setItem(row, i, parameter)
        
        self.clear_fields(self.ui.ui_pages.ui_stock_stacked_pages.set_product_frame)
    
    def clear_buy_list(self):
        """Clears the table where we show what's currently being added to the list."""
        self.ui.ui_pages.ui_stock_stacked_pages.buy_list_table.clearContents()
        self.ui.ui_pages.ui_stock_stacked_pages.buy_list_table.setRowCount(0)
    

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

