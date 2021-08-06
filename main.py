from obj.objects import Product, StoredProduct
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
from typing import List

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
        # Signal for add to stock
        self.ui.ui_pages.ui_stock_stacked_pages.add_stock_btn.clicked.connect(self.add_products_to_stock)

    
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
            if not db.check_product_existance(name):
                id = "NEW"
            else:
                id = str(db.get_product_id(name.lower()))
        else:
            name = self.ui.ui_pages.ui_stock_stacked_pages.set_product_combobox.currentText().strip().upper()
            id = str(db.get_product_id(name.lower()))
        cost = self.ui.ui_pages.ui_stock_stacked_pages.cost_lineedit.text()
        price = self.ui.ui_pages.ui_stock_stacked_pages.price_lineedit.text()
        units = self.ui.ui_pages.ui_stock_stacked_pages.units_lineedit.text()

        if not (name and id and cost and price and units):
            QMessageBox.critical(self, "Error", "Make sure you're filling all the fields.")
            return None

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
        log.debug("A clearing of the buy list table was issued.")
        UICode.clear_table(self.ui.ui_pages.ui_stock_stacked_pages.buy_list_table)
    
    def add_products_to_stock(self):
        """Get's the buy items from the table."""
        log.info("Getting the products list from the add buy table.")
        try:
            products_list = UICode.get_table_rows_text(self.ui.ui_pages.ui_stock_stacked_pages.buy_list_table)
            for product in products_list:
                if product[0] == "NEW":
                    product.pop(0)
                    log.debug("Adding a new product")
                    product_obj = Product(*product)
                    db.add_product(product_obj)                
                else:
                    product_obj = StoredProduct(*product)
                    db.update_product(product_obj)
        except DatabaseIntegrityError:
            log.error("There's a product with the same name and this one was marked as a new one.")
            QMessageBox.critical(self, "Error", f"There's already a product named {product_obj.name.upper()}. Please, search it in the list instead.")
        except NoProductsSpecified:
            log.error("There were no products to add in the table.")
            QMessageBox.critical(self, "Error", "There were no products to add. Please, enter at least one.")
        except Exception:
            log.critical("An exception was raised.")
            QMessageBox.critical(self, "Error", "There was an error trying to add all the products. Check log file.")
            raise
        else:
            QMessageBox.about(self, "Stock buy added", "The bought products were added to stock successfully.")
        finally:
            log.debug("Clearing the table")
            self.clear_buy_list()
 

class UICode:
    @classmethod
    def get_table_rows_text(cls, table: QTableWidget) -> List:
        """Gets the cells texts for each row in a QTableWidget. Only works if the cells don't have any widgets.
        :param table: QTableWidget with ONLY STRINGS. Won't work if a cell has a widget."""
        log.debug(f"Getting items from a table called {table.objectName()}.")
        rows = table.rowCount()
        if not rows:
            raise NoProductsSpecified("There are no products in the list to be added.")
        columns = table.columnCount()
        row_list = []
        for row in range(0, rows):
            this_row = []
            for column in range(0, columns):
                item = table.item(row, column).text()
                this_row.append(item)
            row_list.append(this_row)
        return row_list

    @classmethod
    def clear_table(self, table: QTableWidget) -> None:
        """Clears the table without erasing the headers."""
        log.debug(f"Clearing the {table.objectName()} table.")
        table.clearContents()
        table.setRowCount(0)


        
        
    

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

