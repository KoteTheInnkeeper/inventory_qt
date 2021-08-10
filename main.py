from data.database_cursor import DBCursor
import logging
import time
import sys
# Erasing previous log
with open('log.log', 'w'):
    pass


logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] func:%(funcName)s - %(message)s", level=logging.DEBUG,
                    filename='log.log')

from gui.widgets.py_lineedit import FormLineEdit


# Getting a logger for this file.
log = logging.getLogger("inventory_project")

from gui.widgets.py_combobox import FormCombobox
from obj.objects import Product, StoredProduct
from gui.widgets.ui_stacked_stock_widget import SHOW_TABLE_COLUMS



from qt_core import *
from utils.errors import *
from typing import List, Union


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

        # Populating product comboboxes properly
        UICode.update_comboboxes(self.ui.ui_pages.sell_page, db.get_product_names())
        UICode.update_comboboxes(self.ui.ui_pages.ui_stock_stacked_pages.add_buy_page, db.get_product_names())
        UICode.update_comboboxes(self.ui.ui_pages.ui_stock_stacked_pages.stock_list_page, db.get_product_names())
        # Disabling the one for the stock list by default, since the "show all" checkbox will be checked also by default
        self.ui.ui_pages.ui_stock_stacked_pages.select_product_combobox.setEnabled(False)
        self.ui.ui_pages.ui_stock_stacked_pages.select_product_combobox.set_style()

        # Choosing what to show first at add_product
        UICode.lineedit_or_combobox(
            self.ui.ui_pages.ui_stock_stacked_pages.new_product_linedit,
            self.ui.ui_pages.ui_stock_stacked_pages.set_product_combobox,
            self.ui.ui_pages.ui_stock_stacked_pages.new_product_checkbox
        )
        
        # Toggle menu button
        self.ui.toggle_btn.clicked.connect(self.show_menu)

        # Signals for each button to be clicked
        self.ui.sell_btn.clicked.connect(self.show_sell)
        self.ui.stock_btn.clicked.connect(self.show_stock)
        self.ui.about_btn.clicked.connect(self.show_about)

        # Signals for each minor button
        self.ui.ui_pages.add_buy_btn.clicked.connect(self.show_add_stock)
        self.ui.ui_pages.show_stock_btn.clicked.connect(self.show_stock_list_page)

        # Signal for adding a product to the selling list.
        self.ui.ui_pages.add_item_btn.clicked.connect(self.add_to_cart)

        # Signal for the checkbox to add a new product
        self.ui.ui_pages.ui_stock_stacked_pages.new_product_checkbox.toggled.connect(self.toggled_new_product_checkbox)

        # Signal for the add product button
        self.ui.ui_pages.ui_stock_stacked_pages.add_product_btn.clicked.connect(self.add_product_to_list)
        # Signal for the clear list button at add stock
        self.ui.ui_pages.ui_stock_stacked_pages.clear_stock_btn.clicked.connect(self.clear_buy_list)
        # Signal for add to stock
        self.ui.ui_pages.ui_stock_stacked_pages.add_stock_btn.clicked.connect(self.add_products_to_stock)

        # Signal for the checkbox to show all products
        self.ui.ui_pages.ui_stock_stacked_pages.show_all_products_checkbox.toggled.connect(self.toggled_show_all_products_checkbox)

        # Signal for when the current text has changed in the show stock combobox
        self.ui.ui_pages.ui_stock_stacked_pages.select_product_combobox.currentTextChanged.connect(self.product_name_has_changed)

        # Signal for the stock being updated
        self.ui.ui_pages.ui_stock_stacked_pages.save_changes_btn.clicked.connect(self.update_stock)

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
        UICode.update_comboboxes(self.ui.ui_pages.sell_page, db.get_product_names())
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
    
    def show_stock_list_page(self):
        """"Displays the add stock page."""
        try:
            self.ui.ui_pages.ui_stock_stacked_pages.select_product_combobox.setEnabled(not self.ui.ui_pages.ui_stock_stacked_pages.show_all_products_checkbox.isChecked())
            self.ui.ui_pages.ui_stock_stacked_pages.select_product_combobox.set_style()
            log.debug("Rendering the table for all products.")
            UICode.fill_stock_table(self.ui.ui_pages.ui_stock_stacked_pages.select_product_combobox, self.ui.ui_pages.ui_stock_stacked_pages.show_all_products_checkbox, self.ui.ui_pages.ui_stock_stacked_pages.show_stock_list_page_table, db)
            self.ui.ui_pages.stock_stacked_widget.setCurrentWidget(self.ui.ui_pages.ui_stock_stacked_pages.stock_list_page)
        except ProductsNotFound:
            QMessageBox.critical(self, "No stored products", "At the moment, there are no products stored. You can add them in the 'add buy' section.")
        except Exception:
            log.critical("An exception was raised.")
            QMessageBox(self, "Database error", "There was an error in database. Contact the administrator.") 
        else:
            self.clear_btns(self.ui.ui_pages.stock_menu)
            self.ui.ui_pages.show_stock_btn.set_active(True)

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
        id.setFlags(Qt.ItemIsEnabled)
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

    def update_stock(self) -> None:
        """Updates the stock accordingly."""
        log.info("An update for the stock was issued.")
        try:
            table_text = UICode.get_table_rows_text(self.ui.ui_pages.ui_stock_stacked_pages.show_stock_list_page_table)
            for product in table_text:
                product.pop(1)
                product.pop(1)
                db.update_product_with_rows(product)
        except BlankFieldError:
            log.critical("A field was left blank.")
            QMessageBox.critical(self, "Unable to update", "One of the fields was left blank. This way it is imposible for the database to be edited!")
        except InvalidType:
            log.critical("An invalid type of data was entered in a field in the table.")
            QMessageBox.critical(self, "Invalid input", "You entered an invalid type of data in a field. Remember you can only enter quantities!")
        except Exception:
            log.critical("An exception was raised.")
            raise
        else:
            QMessageBox.information(self, "Updated!", "The stocks were updated successfully.")
        finally:
            UICode.fill_stock_table(
                self.ui.ui_pages.ui_stock_stacked_pages.select_product_combobox,
                self.ui.ui_pages.ui_stock_stacked_pages.show_all_products_checkbox.isChecked(),
                self.ui.ui_pages.ui_stock_stacked_pages.show_stock_list_page_table,
                db
            )

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
                    product_obj = Product(product[0], product[1], time.time(), product[2], product[3])
                    db.add_product(product_obj)                
                else:
                    product_obj = StoredProduct(product[0], product[1], product[2], time.time(), product[3], product[4])
                    db.update_product(product_obj)
        except BlankFieldError:
            log.critical("A field was left blank.")
            QMessageBox.critical(self, "Unable to update", "One of the fields was left blank. This way it is imposible for the database to be edited!")
        except InvalidType:
            QMessageBox.critical(self, "Invalid input", "You entered an invalid type of data in a field. Remember you can only enter quantities!")
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
            log.debug("Updating comboboxes")
            UICode.update_comboboxes(self.ui.ui_pages.ui_stock_stacked_pages.add_buy_page, db.get_product_names())
            UICode.update_comboboxes(self.ui.ui_pages.ui_stock_stacked_pages.stock_list_page, db.get_product_names())
            log.debug("Clearing the table")
            self.clear_buy_list()            

    def toggled_show_all_products_checkbox(self, state: bool):
        """If it's checked, then it shows all products. Otherwise, it just shows the one selected."""
        log.debug("The 'show all products' checkbox was toggled.")
        self.ui.ui_pages.ui_stock_stacked_pages.select_product_combobox.setEnabled(not state)
        self.ui.ui_pages.ui_stock_stacked_pages.select_product_combobox.set_style()
        try:
            UICode.fill_stock_table(
                self.ui.ui_pages.ui_stock_stacked_pages.select_product_combobox,
                state,
                self.ui.ui_pages.ui_stock_stacked_pages.show_stock_list_page_table,
                db
            )
        except ProductNotFound:
            log.critical("There was no product found with this name.")
            QMessageBox.critical(self, "Product not found", f"We couldn't find infor for {self.ui.ui_pages.ui_stock_stacked_pages.select_product_combobox.currentText()}.")
        except Exception:
            log.critical("An exception was raised.")
            raise
    
    def product_name_has_changed(self):
        """Passes down the new selected name."""
        log.info("The text within the product combobox has changed.")
        try:
            UICode.fill_stock_table(
                self.ui.ui_pages.ui_stock_stacked_pages.select_product_combobox,
                self.ui.ui_pages.ui_stock_stacked_pages.show_all_products_checkbox.isChecked(),
                self.ui.ui_pages.ui_stock_stacked_pages.show_stock_list_page_table,
                db
            )
        except ProductNotFound:
            log.critical("There are no products called like so.")
            pass
    
    def add_to_cart(self) -> None:
        """Adds an item to the cart."""
        try:
            name = self.ui.ui_pages.add_product_combobox.currentText().lower()
            units = int(self.ui.ui_pages.sell_units_lineedit.text())
            product_params = db.get_product(name)
        except ValueError:
            log.critical("Something different than a quantity was inputed at the units field.")
            QMessageBox.critical(self, "Invalid units", "Invalid input in the 'units' field. Remember you can only input integers.")
        except ProductNotFound:
            QMessageBox.critical(self, "Product not found", "The product wasn't found.")
        except Exception:
            log.critical("An exception was raised.")
            raise
        else:
            try:
                pass
            except Exception:
                log.critical("An exception was raised.")
                raise

            


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
    
    @classmethod
    def update_comboboxes(self, frame: Union[QFrame, QWidget], list: List):
        """Updates all comboboxes in the given frame."""
        log.debug("Clearing combobox.")
        # Products ones
        if list:
            for combobox in frame.findChildren(QComboBox):
                combobox.clear()
                combobox.addItems(list)
            combobox.setEnabled(True)
            combobox.set_style()

    @classmethod
    def lineedit_or_combobox(cls, line_edit: FormLineEdit, combobox: FormCombobox, checkbox: QCheckBox):
        """If the combobox has items at all, it shows it and disables the lineedit. It uncheks the checkbox."""
        log.debug("Choosing between the combobox or lineedit for the product name.")
        if combobox.isEnabled():
            checkbox.setChecked(False)
            combobox.setVisible(True)
            line_edit.setVisible(False)
    
    @classmethod
    def fill_stock_table(cls, combobox: FormCombobox, state: bool, table: QTableWidget, db: Database) -> None:
        """If the checkbox is checked, renders the table for all products."""
        try:
            # Clearing the table
            table.clearContents()
            table.setRowCount(0)
            if state:
                log.debug("Rendering for all products")
                product_list = db.get_stock()
                # Making sure there's enough rows in the table
                for row, product in enumerate(product_list):
                    this_row = []
                    if not (table.rowCount() == len(product_list)):
                        table.insertRow(row)
                    for element in product:
                        this_row.append(element)
                    for column, product_item in enumerate(this_row):
                        table.setItem(row, column, product_item)                                            
            else:
                log.debug("Rendering for one product")
                product_name = combobox.currentText().lower()
                prod_items = db.get_stock(product_name)
                table.insertRow(0)
                for column, item in enumerate(prod_items):
                    table.setItem(0, column, item)
        except Exception:
            log.critical("An exception was raised.")
            raise


        
        


        
    

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

