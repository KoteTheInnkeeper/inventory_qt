import logging
import os
import sqlite3

from typing import List
from data.database_cursor import DBCursor
from obj.objects import *
from utils.errors import *

log = logging.getLogger("inventory_qt.data")


class Database:
    def __init__(self, host: str) -> None:
        # Establishing the path
        log.debug("Getting the path according to the host's name.")
        self.host = self.db_path(host)
        log.debug(f"The host was established as '{self.host}'")

        # Check file and creates it if it doesn't exist.
        if not self.check_file():
            pass

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
            except Exception:
                log.critical("An exception was raised.")
                raise

    def setup_tables(self) -> True:
        try:
            log.debug("Making sure the tables are created.")
            with DBCursor(self.host) as cursor:
                cursor.execute("CREATE TABLE IF NOT EXISTS items(name TEXT UNIQUE, cost_price REAL, sell_price REAL)")
                cursor.execute("CREATE TABLE IF NOT EXISTS sold(items TEXT, date REAL, total REAL)")
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
                cursor.execute("INSERT INTO items VALUES (?, ?, ?)", (product_parameters['name'], product_parameters['cost'], product_parameters['price']))
        except sqlite3.IntegrityError:
            log.critical("An integrity error was raised. Maybe a matching name or id.")
            raise DatabaseIntegrityError("There's a matching name or id already stored.")
        else:
            log.info(f"{product.__repr__} was added successfully.")
    
    def update_product(self, product: StoredProduct):
        prod_param = product.to_db()
        log.debug("Updating a product.")
        try:
            with DBCursor(self.host) as cursor:
                cursor.execute("UPDATE items SET name = ?, cost_price = ?, sell_price = ? WHERE rowid = ?", (prod_param['name'], prod_param['cost'], prod_param['price'], prod_param['id']))
        except Exception:
            log.critical("An exception was raised.")
            raise
        else:
            log.info(f"{product.__repr__} was updated successfully.")
    
    def get_product_names(self) -> List[str]:
        try:
            with DBCursor(self.host) as cursor:
                cursor.execute("SELECT name FROM items")
                results = cursor.fetchall()
                if results:
                    return [product_name for (product_name, ) in results]
                else:
                    raise ProductsNotFound("There were no products to be displayed.")
        except Exception:
            log.critical("An exception was raised.")
            raise
        except ProductsNotFound:
            log.critical("No products were found. Returning an empty list.")
            return []
    
    
        
