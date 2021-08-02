from qt_core import *
from gui.gui_constants import *
from gui.widgets.py_pushbutton import MinorLeftMenuButtons

class UIStackedPages(object):
    def setupUi(self, StackedPages):
        if not StackedPages.objectName():
            StackedPages.setObjectName(u"StackedPages")
        StackedPages.resize(640, 480)
        StackedPages.setWindowTitle(u"StackedWidget")
        self.sell_page = QWidget()
        self.sell_page.setObjectName(u"sell_page")
        self.home_layout = QVBoxLayout(self.sell_page)
        self.home_layout.setSpacing(0)
        self.home_layout.setObjectName(u"home_layout")
        self.home_layout.setContentsMargins(0, 0, 0, 0)
        self.sell_label = QLabel(self.sell_page)
        self.sell_label.setObjectName(u"sell_label")
        self.sell_label.setText(u"Sell page")
        self.sell_label.setAlignment(Qt.AlignCenter)

        self.home_layout.addWidget(self.sell_label)

        StackedPages.addWidget(self.sell_page)

        self.stock_page = QWidget()
        self.stock_page.setObjectName(u"stock_page")
        self.stock_layout = QHBoxLayout(self.stock_page)
        self.stock_layout.setSpacing(0)
        self.stock_layout.setObjectName(u"stock_layout")
        self.stock_layout.setContentsMargins(0, 0, 0, 0)
        self.stock_label = QLabel(self.stock_page)
        self.stock_label.setObjectName(u"stock_label")
        self.stock_label.setText(u"Stock label")
        self.stock_label.setAlignment(Qt.AlignCenter)

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
        self.add_buy_btn = MinorLeftMenuButtons("Add buy", icon_path="stock_add_icon.svg", btn_active_border_right=Color.CONTENT_BACKGROUND)
        self.show_stock_btn = MinorLeftMenuButtons("Show stock", icon_path="stock_list_icon.svg", btn_active_border_right=Color.CONTENT_BACKGROUND)

        # Adding this stock left buttons to the left menu from stock
        self.stock_menu_layout.addWidget(self.add_buy_btn)
        self.stock_menu_layout.addWidget(self.show_stock_btn)

        self.stock_layout.addWidget(self.stock_menu)
        self.stock_layout.addWidget(self.stock_label)

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

