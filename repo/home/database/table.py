class DBTable:
    _fetch_on_startup = False

    def __init__(self, table_name):
        self.table_name = table_name
        self.records = []

    def insert(self, **kwargs):
        raise NotImplementedError()

    def get_by_id(self, specified_id):
        raise NotImplementedError()

    def fetch_records(self):
        raise NotImplementedError()

    def create_table(self):
        raise NotImplementedError()
