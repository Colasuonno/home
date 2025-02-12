import logging

_logger = logging.getLogger(__name__)

class Database:

    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

        _logger.info(f"Trying to connect to database {self.database}")
        _logger.debug(f"DB info: {self.host}:{port}/{self.database} with user {self.user} and password length {len(self.password)}")
