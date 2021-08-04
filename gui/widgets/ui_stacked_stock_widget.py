from PySide6 import QtWidgets
import PySide6
from qt_core import *
from gui.gui_constants import *
from gui.widgets.py_pushbutton import *
from gui.widgets.py_lineedit import FormLineEdit
from gui.widgets.py_combobox import FormCombobox

TABLE_COLUMNS = ("Id", "Product name", "Date", "Cost", "Price")
TABLE_SIZE_FORMAT = (QHeaderView.ResizeToContents, QHeaderView.Stretch, QHeaderView.ResizeToContents, QHeaderView.ResizeToContents, QHeaderView.ResizeToContents)

class UIStockStackedPages(object):
    def setupUi(self, StockStackedPages: QStackedWidget):
        if not StockStackedPages.objectName():
            StockStackedPages.setObjectName(u"StockStackedPages")
        StockStackedPages.resize(800, 600)
        StockStackedPages.setWindowTitle(u"StockStackedPages")

        # Making the widgets for add buy page
        self.add_buy_page = QWidget()
        self.add_buy_page.setObjectName(u"add_buy_page")
        # Setting up a layout for add buy page
        self.add_buy_layout = QVBoxLayout(self.add_buy_page)
        self.add_buy_layout.setContentsMargins(10, 10, 10, 10)
        self.add_buy_layout.setSpacing(10)
        self.add_buy_layout.setAlignment(Qt.AlignVCenter)
        # Making the elements that are going to fit within this layout
        # A frame to hold the 'products' widgets
        self.set_product_frame = QFrame()
        self.set_product_frame.setMinimumHeight(20)
        self.set_product_frame.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        # A layout for this frame
        self.set_product_layout = QHBoxLayout(self.set_product_frame)
        self.set_product_layout.setSpacing(10)
        self.set_product_layout.setContentsMargins(0, 0, 0, 0)
        self.set_product_layout.setAlignment(Qt.AlignLeft)
        # Elements for this frame
        # Label
        self.set_product_label = QLabel("Product name")
        self.set_product_label.setStyleSheet("font: 100 13pt 'Segoe UI';")
        # Combobox for products that are already in database
        self.set_product_combobox = FormCombobox()
        self.set_product_combobox.addItems(["nooo", "dat"])
        self.set_product_combobox.setMinimumSize(QSize(Dimension.COMBOBOX_MIN_WIDTH, Dimension.COMBOBOX_MIN_HEIGHT))
        # A line edit in case the product is a new one
        self.new_product_linedit = FormLineEdit(visibility=True)
        # A checkbox to tell if the product is a new one
        self.new_product_checkbox = QCheckBox()
        self.new_product_checkbox.setChecked(True)
        self.new_product_checkbox.setText("New product")
        # Let's add these three elements to the layout
        self.set_product_layout.addWidget(self.set_product_label)
        self.set_product_layout.addWidget(self.set_product_combobox)
        self.set_product_layout.addWidget(self.new_product_linedit)
        self.set_product_layout.addWidget(self.new_product_checkbox)

        # A table for us to show what's currently being added as a buy
        self.buy_list_table = QTableWidget()
        self.buy_list_table.setMinimumWidth(724)
        self.buy_list_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.buy_list_table.setStyleSheet("background-color: white;")
        # Setting the columns
        column_font = QFont()
        column_font.setFamily('Segoe UI')
        column_font.setPointSize(12)
        column_font.setBold(True)
        column_font.setWeight(QFont.Weight.Bold)
        if self.buy_list_table.columnCount() < len(TABLE_COLUMNS):
            self.buy_list_table.setColumnCount(len(TABLE_COLUMNS))
        for i, column in enumerate(TABLE_COLUMNS, 0):
            item = QTableWidgetItem()
            item.setText(column)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFont(column_font)
            self.buy_list_table.setHorizontalHeaderItem(i, item)
        self.buy_list_table.horizontalHeader().setDefaultSectionSize(150)
        self.buy_list_table.horizontalHeader().setMinimumSectionSize(150)
        # Formatting the size for each header
        for i, size in enumerate(TABLE_SIZE_FORMAT, 0):
            self.buy_list_table.horizontalHeader().setSectionResizeMode(i, size)
        # Showing horizontal header and hiding vertical
        self.buy_list_table.horizontalHeader().setVisible(True)
        self.buy_list_table.verticalHeader().setVisible(False)
    
        # A frame to hold the "add" and "clear list" buttons
        self.stock_btn_frame = QFrame()
        # Setting a layout
        self.stock_btn_layout = QHBoxLayout(self.stock_btn_frame)
        self.stock_btn_layout.setContentsMargins(0, 0, 0, 0)
        self.stock_btn_layout.setSpacing(0)
        self.stock_btn_layout.setAlignment(Qt.AlignCenter)
        # Buttons for this layout
        self.add_stock_btn = FormButton("Add to stock")
        self.clear_stock_btn = FormButton("Clear list")
        # A spacer to space them
        self.btn_spacer = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # Adding these to the layout
        self.stock_btn_layout.addWidget(self.clear_stock_btn)
        self.stock_btn_layout.addItem(self.btn_spacer)
        self.stock_btn_layout.addWidget(self.add_stock_btn)

        # Adding all of this to the add_page layout
        self.add_buy_layout.addWidget(self.set_product_frame)
        self.add_buy_layout.addWidget(self.buy_list_table)
        self.add_buy_layout.addWidget(self.stock_btn_frame)

        StockStackedPages.addWidget(self.add_buy_page)


        QMetaObject.connectSlotsByName(StockStackedPages)
