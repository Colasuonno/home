from .table_internet_provider import InternetProvider
from .handler.database_handler import DatabaseHandler

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
                                                           port=self.port,
                                                           database=self.database,
                                                           user=self.user,
                                                           password=password)
        except psycopg2.OperationalError:
            _logger.error(f"Failed to connect to database {self.database}")
            _logger.error("No problem we work even without database...")



        # Start handler
        self.handler = DatabaseHandler(self)


    def execute(self, cursor, query):
        return cursor.execute(query)

    def fetchall(self, cursor, query):
        cursor.execute(query)
        return cursor.fetchall()

    def cursor(self):
        return self.pool.getconn().cursor()

    def _get_tables(self):
        return [
            InternetProvider()
        ]
