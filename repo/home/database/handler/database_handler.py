import threading
import logging

_logger = logging.getLogger(__name__)

class DatabaseHandler:

    def __init__(self, database):
        self.database = database
        # Create tables

        with database.obtain_cursor() as cursor:
            for table_name, table in database.tables.items():
                res = database.execute(
                    cursor, table.create_table()
                )
                _logger.info(f"Table {table.table_name} res: " + str(res))

                # Check for startup-fetch
                if table._fetch_on_startup:
                    _logger.info(f"Table {table.table_name}: has startup fetch....")
                    res = database.fetchall_named(cursor, table.fetch_records())
                    _logger.info(f"Table {table.table_name}: has fetched {len(res)} records")
                    table.records = res

            _logger.info("Database connection established!! (Pool)")

        self.thread = threading.Timer(60.0 * 5, self.run)
        self.thread.start()
        self.run()


    def run(self):
        # Check for already connected db and test connection, ping for pool :)
        _logger.debug("CRON Check for db alive...")

        try:
            conn = self.database.pool.getconn()
            assert conn is not None
            _logger.debug("Database is still alive :)")
            self.database.pool.putconn(conn)
        except Exception as e:
            _logger.error("Database is currently unavailable..")






