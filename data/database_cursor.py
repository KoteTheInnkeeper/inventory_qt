import logging
import sqlite3

log = logging.getLogger("inventory_qt.database_cursor")

class DBCursor:
    """
    Context manager for sqlite queries. Returns a cursor object.
    """
    def __init__(self, host: str):
        self.host = host
        self.connection = None

    def __enter__(self):
        log.debug("Making a connection.")
        self.connection = sqlite3.connect(self.host)
        log.debug("Returning a cursor.")
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb or exc_val or exc_type:
            log.debug("An exception was reased within this context manager. Closing connection.")
            self.connection.close()
        else:
            log.debug("This context has concluded without exceptions raised. Commiting and closing.")
            self.connection.commit()
            self.connection.close()
