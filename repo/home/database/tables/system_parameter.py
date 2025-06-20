
from ..table import DBTable
from cachetools import TTLCache
import logging
import base64

_logger = logging.getLogger(__name__)

class SystemParameter(DBTable):

    TABLE_NAME = "system_parameter"


    def __init__(self):
        super().__init__(self.TABLE_NAME)
        self.users_options = {}

    def insert(self, key_v: str, value_v: str):
        return \
            f"""
            INSERT INTO {self.TABLE_NAME} (key, value)
VALUES ('{key_v}', '{value_v}') ON CONFLICT (key) DO UPDATE SET value = '{value_v}';
                        """

    def get_by_id(self, specified_id: str):
        return \
                f"""
                SELECT value FROM {self.TABLE_NAME} WHERE key = '{specified_id}';
                """

    def fetch_records(self):
        return \
                f"""
                SELECT key,value FROM {self.TABLE_NAME};
                """

    def create_table(self):
        return\
            f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
              key VARCHAR  PRIMARY KEY,
              value VARCHAR NOT NULL
            );"""