from qt_core import *


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
        self.stock_layout = QVBoxLayout(self.stock_page)
        self.stock_layout.setSpacing(0)
        self.stock_layout.setObjectName(u"stock_layout")
        self.stock_layout.setContentsMargins(0, 0, 0, 0)
        self.stock_label = QLabel(self.stock_page)
        self.stock_label.setObjectName(u"stock_label")
        self.stock_label.setText(u"Stock label")
        self.stock_label.setAlignment(Qt.AlignCenter)

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

