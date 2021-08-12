import logging
import os
import time
from types import DynamicClassAttribute
logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] func:%(funcName)s - %(message)s", level=logging.DEBUG,
                    filename='log.log')


from typing import Dict, List, Union
from data.database_cursor import *
from obj.objects import *
from utils.errors import *

log = logging.getLogger("inventory_qt.data")
product_std_fields = ('id', 'name', 'units', '')

class Database:
    def __init__(self, host: str) -> None:
        # Establishing the path
        log.debug("Getting the path according to the host's name.")
        self.host = self.db_path(host)
        log.debug(f"The host was established as '{self.host}'")

        # Check file and creates it if it doesn't exist.
        if not self.check_file():
            with open(self.host, 'w'):
                log.info("Database file created")
        self.setup_tables()

    def check_file(self) -> bool:
        """Checks if the database exists and returns True or False."""
        log.info("Checking if the database file exists.")
        try:
            with open(self.host, 'r'):
                log.info("Database file exists. Checking it's integrity")
        except FileNotFoundError:
            log.error("The database file doesn't exists.")
            return False
        else:
            try:
                self.setup_tables()
                return True
            except Exception:
                log.critical("An exception was raised.")
                raise

    def setup_tables(self) -> None:
        try:
            log.debug("Making sure the tables are created.")
            with DBCursor(self.host) as cursor:
                cursor.execute("CREATE TABLE IF NOT EXISTS items(name TEXT UNIQUE, units INTEGER, last_buy REAL, cost_price REAL, sell_price REAL)")
                cursor.execute("CREATE TABLE IF NOT EXISTS sold(item TEXT, units INTEGER, date REAL, total REAL)")
        except Exception:
            log.critical("An exception was raised.")
            raise
        else:
            log.info("Tables are set up.")

    def db_path(self, host: str) -> str:
        """Returns the absolute path for the database file provided."""
        app_path = os.path.abspath(os.getcwd())
        folder = 'data'
        path = os.path.join(app_path, folder)
        return os.path.normpath(os.path.join(path, host))

    def add_product(self, product: Product):
        """Adds a new product."""
        log.debug("Adding a new product")
        product_parameters = product.to_db()
        try:
            with DBCursor(self.host) as cursor:
                cursor.execute("INSERT INTO items VALUES (?, ?, ?, ?, ?)", (product_parameters['name'].lower(), product_parameters['units'], product_parameters['last_buy'], product_parameters['cost'], product_parameters['price']))
        except sqlite3.IntegrityError:
            log.critical("An integrity error was raised. Maybe a matching name or id.")
            raise DatabaseIntegrityError("There's a matching name or id already stored.")
        else:
            log.info(f"{product.__repr__} was added successfully.")

    def update_product_with_rows(self, product: List[str]):
        """Updates the product when there's only text."""
        try:
            id, cost, price, stock = product
            if not (cost and price and stock):
                raise BlankFieldError("A field was blank.")
            cost = float(cost)
            price = float(price)
            stock = int(stock)
            id = int(id)
            log.debug(f"Updating product with {id} as id.")
            with DBCursor(self.host) as cursor:
                cursor.execute("UPDATE items SET cost_price = ?, sell_price = ?, units = ? WHERE rowid = ?", (cost, price, stock, id))
        except ValueError:
            log.critical("At least one of the entered values isn't valid.")
            raise InvalidType("At least one of the entered values isn't the right type.")
        except Exception:
            log.critical("An exception was raised.")
            raise    
        else:
            log.debug("The product was successfully")

    def update_product(self, product: StoredProduct):
        prod_param = product.to_db()
        log.debug("Updating a product.")
        try:
            if not (prod_param['id'] and prod_param['name'] and prod_param['units'] and prod_param['last_buy'] and prod_param['cost'] and prod_param['price']):
                raise BlankFieldError("Blank field were encountered.")
            with DBCursor(self.host) as cursor:
                cursor.execute("UPDATE items SET name = ?, units = units + ?, last_buy = ?, cost_price = ?, sell_price = ? WHERE rowid = ?", (prod_param['name'], prod_param['units'], prod_param['last_buy'], prod_param['cost'], prod_param['price'], prod_param['id']))
        except Exception:
            log.critical("An exception was raised.")
            raise
        else:
            log.info(f"{product.__repr__} was updated successfully.")
    
    def get_product_names(self) -> List[str]:
        log.debug("Getting a list with all product's names.")
        try:
            with DBCursor(self.host) as cursor:
                cursor.execute("SELECT name FROM items")
                results = cursor.fetchall()
                if results:
                    return [product_name.upper() for (product_name, ) in results]
                else:
                    raise ProductsNotFound("There were no products to be displayed.")
        except ProductsNotFound:
            log.critical("No products were found. Returning an empty list.")
            return []
        except Exception:
            log.critical("An exception was raised.")
            raise
        
    def get_product_id(self, name: str) -> str:
        log.info("Getting a product's id by its name.")
        try:
            with DBCursor(self.host) as cursor:
                cursor.execute("SELECT rowid FROM items WHERE name = ?", (name.lower(),))
                result = cursor.fetchone()
                if result:
                    log.debug("Product found. Returning the id.")
                    return str(result[0])
                else:
                    log.error("There's no match for this name. Returning NEW")
                    return "NEW"
        except Exception:
            log.critical("An exception was raised.")
            raise
    
    def check_product_existance(self, name: str) -> bool:
        log.info("Guessing if the product exist already in database.")
        with DBCursor(self.host) as cursor:
            cursor.execute("SELECT rowid FROM items WHERE name = ?", (name.lower(), ))
            result = cursor.fetchone()
            if result:
                return True
            else:
                return False
    
    def get_stock(self, name: str="all") -> List[QTableWidgetItem]:
        """Gets the stock for the product provided in name. If no name was specified, it does it for all of them."""
        try:
            if name != "all":
                log.debug(f"Getting the stock for {name.upper()}.")
                with DBCursor(self.host) as cursor:
                    cursor.execute("SELECT rowid, name, units, last_buy, cost_price, sell_price FROM items WHERE name = ?", (name.lower(), ))
                    result = cursor.fetchone()
                    if result:
                        log.debug("There was a product named like soo, returning a StoredProduct for it.")
                        return StoredProduct(*result).to_table()
                    else:
                        raise ProductNotFound("There was no product named like so.")
            else:
                log.debug("Getting the stock for all products.")
                with DBCursor(self.host) as cursor:
                    cursor.execute("SELECT rowid, name, units, last_buy, cost_price, sell_price FROM items")
                    results = cursor.fetchall()
                    if not results:
                        log.error("There were no products to show at all.")
                        raise ProductsNotFound("There are no products to show.")
                    product_list = []
                    for product in results:
                        product_list.append(StoredProduct(*product).to_table())
        except Exception:
            log.critical("An exception was raised.")
            raise
        else:
            log.debug("A StoredProduct list was consumated.")
            return product_list

    def get_product_for_cart(self, name: str) -> Dict:
        """Gets the product's parameters """
        try:
            with DBCursor(self.host) as cursor:
                cursor.execute("SELECT units, sell_price FROM items WHERE rowid = ?", (int(self.get_product_id(name.lower())), ))
                result = cursor.fetchone()
                if not result:
                    log.critical("Product not found in database.")
                    raise ProductNotFound("The product wasn't found.")
                return {
                    'id': int(self.get_product_id(name.lower())),
                    'name': name,
                    'units': int(result[0]),
                    'price': float(result[1])
                }                
        except ValueError:
            log.critical("The id wasn't found within the database or one of the retrieved fields wasn't a number when it had to.")
            raise ProductNotFound("The product wasn't found.")
        except Exception:
            log.critical("An exception was raised.")
            raise



    
        
    
    
        
