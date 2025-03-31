from .table_internet_provider import InternetProvider
from .handler.database_handler import DatabaseHandler
from contextlib import contextmanager

import logging
import psycopg2.pool

_logger = logging.getLogger(__name__)

class Database:

    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.port = port

        _logger.info(f"Trying to connect to database {self.database}")
        _logger.debug(f"DB info: {self.host}:{port}/{self.database} with user {self.user} and password length {len(password)}")

        # Creating pool
        try:
            self.pool = psycopg2.pool.SimpleConnectionPool(2,
                                                           5,
                                                           host=self.host,
                                                           port=self.port,
                                                           database=self.database,
                                                           user=self.user,
                                                           password=password)
        except psycopg2.OperationalError as e:
            _logger.error(f"Failed to connect to database {self.database}")
            _logger.error("No problem we work even without database...")
            _logger.error(e)


        # Start handler
        self.handler = DatabaseHandler(self)


    def execute(self, cursor, query):
        _logger.debug(f"Executing query: {query}")
        return cursor.execute(query)

    def fetchall(self, cursor, query):
        _logger.debug(f"Executing query: {query}")
        cursor.execute(query)
        return cursor.fetchall()

    @contextmanager
    def obtain_cursor(self):
        """Context manager to automatically close a psycopg2 cursor."""
        conn = self.pool.getconn()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def _get_tables(self):
        return [
            InternetProvider()
        ]
