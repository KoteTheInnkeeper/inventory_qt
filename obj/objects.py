# Here I create the objects needed to interact within the program
import logging

from qt_core import *
from utils.errors import *
from typing import List, Tuple
from datetime import datetime


log = logging.getLogger("inventory_qt.objects")

class Product:
    def __init__(self, name: str, units: str, last_buy: float, cost: float, price: float):
        try:
            log.info("Making a new <<PRODUCT>> object.")
            self.name = str(name).lower()
            self.units = int(units)
            self.last_buy = int(last_buy)
            self.cost = float(cost)
            self.price = float(price)
        except ValueError:
            log.critical("Invalid types were entered to the initialization of this StoredProduct object.")
            raise InvalidType("Invalid types were entered to the initialization of this StoredProduct object.")

    def __repr__(self) -> str:
        return f"<PRODUCT OBJECT identified with name '{self.name.upper()}': C {self.cost}, P {self.price}; U {self.units}>"

    def to_db(self) -> dict:
        return {
            'name': self.name,
            'units': self.units,
            'last_buy': self.last_buy,
            'cost': self.cost,
            'price': self.price
        }

class StoredProduct(Product):
    def __init__(self, id: int, name: str, units: int, last_buy: float, cost: float, price: float):
        try:
            super().__init__(name, units, last_buy,cost, price)
            self.id = int(id)
        except ValueError:
            log.critical("Invalid types were entered to the initialization of this StoredProduct object.")
            raise InvalidType("Invalid types were entered to the initialization of this StoredProduct object.")
    
    def __repr__(self) -> str:
        return  f"<STORED PRODUCT OBJECT identified with name {self.name.upper()} and id {self.id}: C {self.cost}; P {self.cost}; U {self.units}"
    
    def to_db(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'units': self.units,
            'last_buy': self.last_buy,
            'cost': self.cost,
            'price': self.price
        }
    
    def to_table(self) -> Tuple[QTableWidgetItem]:
        # Getting the 'last buy' as a formated date.
        formated_date = datetime.fromtimestamp(self.last_buy).strftime("%d/%m/%Y - %H:%M")
        id = QTableWidgetItem(str(self.id))
        id.setTextAlignment(Qt.AlignCenter)
        id.setFlags(Qt.ItemIsEnabled)
        name = QTableWidgetItem(str(self.name.upper()))
        name.setTextAlignment(Qt.AlignCenter)
        units = QTableWidgetItem(str(self.units))
        units.setTextAlignment(Qt.AlignCenter)
        last_buy = QTableWidgetItem(formated_date)
        last_buy.setTextAlignment(Qt.AlignCenter)
        last_buy.setFlags(Qt.ItemIsEnabled)
        cost = QTableWidgetItem("%.2f" %self.cost if self.cost != 0 else "0")
        cost.setTextAlignment(Qt.AlignCenter)
        price = QTableWidgetItem("%.2f" %self.price if self.price != 0 else "0")
        price.setTextAlignment(Qt.AlignCenter)
        return (id, name, last_buy, cost, price, units)


    
    