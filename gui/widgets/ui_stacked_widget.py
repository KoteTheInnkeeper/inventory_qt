from qt_core import *
from gui.gui_constants import *
from gui.widgets.py_pushbutton import MinorLeftMenuButtons
from gui.widgets.ui_stacked_stock_widget import UIStockStackedPages

class UIStackedPages(object):
    def setupUi(self, StackedPages):
        if not StackedPages.objectName():
            StackedPages.setObjectName(u"StackedPages")
        StackedPages.resize(640, 480)
        StackedPages.setWindowTitle(u"StackedWidget")

        # Sell page
        self.sell_page = QWidget()
        self.sell_page.setObjectName(u"sell_page")
        self.sell_layout = QVBoxLayout(self.sell_page)
        self.sell_layout.setSpacing(0)
        self.sell_layout.setObjectName(u"sell_layout")
        self.sell_layout.setContentsMargins(0, 0, 0, 0)
        
        # Frames for this page
        # Frame for the input in products
        self.add_product_frame = QFrame()
        self.add_product_frame.setObjectName(u"sell_product_frame")

        # Frame for add the selling process.
        self.complete_sell_frame = QFrame()
        self.complete_sell_frame.setObjectName(u"complete_sell_frame")

        # Table where we can see the products for this transaction
        self.selling_table = QTableWidgetItem()

        
         
        

        # Adding widgets and frames to this layout

        StackedPages.addWidget(self.sell_page)

        self.stock_page = QWidget()
        self.stock_page.setObjectName(u"stock_page")
        self.stock_layout = QHBoxLayout(self.stock_page)
        self.stock_layout.setSpacing(0)
        self.stock_layout.setObjectName(u"stock_layout")
        self.stock_layout.setContentsMargins(0, 0, 0, 0)
        
        self.stock_menu = QFrame()
        self.stock_menu.setStyleSheet(f"background-color: {Color.STOCK_LEFT_MENU};")
        self.stock_menu.setMaximumWidth(Dimension.STOCK_LEFT_MENU_WIDTH)
        self.stock_menu.setMinimumWidth(Dimension.STOCK_LEFT_MENU_WIDTH)

        # Stock left menu layout
        self.stock_menu_layout = QVBoxLayout(self.stock_menu)
        self.stock_menu_layout.setContentsMargins(0, Dimension.BTN_DEF_HEIGHT - Dimension.TOP_BAR_HEIGHT, 0, 0)
        self.stock_menu_layout.setSpacing(0)
        self.stock_menu_layout.setAlignment(Qt.AlignTop)

        # Stock left menu buttons
        self.add_buy_btn = MinorLeftMenuButtons("Add buy", icon_path="stock_add_icon.svg", btn_active_border_right=Color.CONTENT_BACKGROUND, is_active=True)
        self.show_stock_btn = MinorLeftMenuButtons("Show stock", icon_path="stock_list_icon.svg", btn_active_border_right=Color.CONTENT_BACKGROUND)

        # Adding this stock left buttons to the left menu from stock
        self.stock_menu_layout.addWidget(self.add_buy_btn)
        self.stock_menu_layout.addWidget(self.show_stock_btn)

        self.stock_layout.addWidget(self.stock_menu)
        

        # Adding the stock stacked pages to this page
        self.stock_stacked_widget = QStackedWidget()
        # STYLEESHEET REQUIRED? #
        # Set the pages
        self.ui_stock_stacked_pages = UIStockStackedPages()
        self.ui_stock_stacked_pages.setupUi(self.stock_stacked_widget)
        self.stock_stacked_widget.setCurrentWidget(self.ui_stock_stacked_pages.add_buy_page)

        self.stock_layout.addWidget(self.stock_stacked_widget)



        StackedPages.addWidget(self.stock_page)
        self.about_page = QWidget()
        self.about_page.setObjectName(u"about_page")
        self.about_layout = QVBoxLayout(self.about_page)
        self.about_layout.setSpacing(0)
        self.about_layout.setObjectName(u"about_layout")
        self.about_layout.setContentsMargins(0, 0, 0, 0)
        self.about_label = QLabel(self.about_page)
        self.about_label.setObjectName(u"about_label")
        self.about_label.setText(u"About page")
        self.about_label.setAlignment(Qt.AlignCenter)

        self.about_layout.addWidget(self.about_label)

        StackedPages.addWidget(self.about_page)

        self.retranslateUi(StackedPages)

        QMetaObject.connectSlotsByName(StackedPages)
    # setupUi

    def retranslateUi(self, StackedPages):
        pass
    # retranslateUi

