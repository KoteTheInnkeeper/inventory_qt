from data.database_cursor import DBCursor
import sqlite3
import logging
import os

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

