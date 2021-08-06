# Here I create the objects needed to interact within the program
import logging
from utils.errors import InvalidType

log = logging.getLogger("inventory_qt.objects")

class Product:
    def __init__(self, name: str, units: str, cost: float, price: float):
        try:
            log.info("Making a new <<PRODUCT>> object.")
            self.name = str(name).lower()
            self.units = int(units)
            self.cost = float(cost)
            self.price = float(price)
        except ValueError:
            log.critical("One of the given parameters wasn't the specified type.")
            raise InvalidType("An invalid type was specified for at least one of this product's parameters.")

    def __repr__(self) -> str:
        return f"<PRODUCT OBJECT identified with name '{self.name.upper()}'"

    def to_db(self) -> dict:
        return {
            'name': self.name,
            'units': self.units,
            'cost': self.cost,
            'price': self.price
        }


class StoredProduct(Product):
    def __init__(self, name: str, units: int, cost: float, price: float, id: int):
        try:
            super().__init__(name, units, cost, price)
            self.id = int(id)
        except ValueError:
            log.critical("The id wasn't an integer.")
            raise InvalidType("The id wasn't an integer.")
    
    def __repr__(self) -> str:
        return  f"<STORED PRODUCT OBJECT identified with name {self.name.upper()}"
    
    def to_db(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'units': self.units,
            'cost': self.cost,
            'price': self.price
        }
    
    