from .table import DBTable

class InternetProvider(DBTable):

    TABLE_NAME = "internet_provider"

    def __init__(self):
        super().__init__(self.TABLE_NAME)

    def create_table(self):
        return \
            f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
              id SERIAL PRIMARY KEY,
              name VARCHAR,
              brand VARCHAR,
              UNIQUE (name, brand)  
            );"""