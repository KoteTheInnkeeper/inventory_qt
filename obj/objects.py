# Here I create the objects needed to interact within the program
import logging

from qt_core import *
from utils.errors import *
from typing import List, Tuple


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
            log.critical("One of the given parameters wasn't the specified type.")
            raise InvalidType("An invalid type was specified for at least one of this product's parameters.")

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
            log.critical("The id wasn't an integer.")
            raise InvalidType("The id wasn't an integer.")
    
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
        id = QTableWidgetItem(str(self.id))
        id.setTextAlignment(Qt.Aligncenter)
        name = QTableWidgetItem(str(self.name))
        name.setTextAlignment(Qt.Aligncenter)
        units = QTableWidgetItem(str(self.units))
        units.setTextAlignment(Qt.Aligncenter)
        last_buy = QTableWidgetItem(str(self.last_buy))
        last_buy.setTextAlignment(Qt.Aligncenter)
        cost = QTableWidgetItem("%.2f" %str(self.cost) if self.cost != 0 else "0")
        cost.setTextAlignment(Qt.Aligncenter)
        price = QTableWidgetItem("%.2f" %str(self.price) if self.price != 0 else "0")
        price.setTextAlignment(Qt.Aligncenter)
        return (id, name, units, cost, price)


    
    