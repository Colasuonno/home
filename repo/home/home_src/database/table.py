class DBTable:

    def __init__(self, table_name):
        self.table_name = table_name

    def create_table(self):
        raise NotImplementedError()
