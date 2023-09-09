import dataset

class DataBase(object):
    def __init__(self, uri='sqlite:///petwatch-ai-infenrece.db'):
        self.uri = uri
        self.db = dataset.connect(self.uri)

    def search(self, query):
        try:
            return [row for row in self.db.query(query)]
        except:
            return []

    def insert(self, table_name, data):
        table = self.db[table_name]
        if isinstance(data, list):
            table.insert_many(data)
        else:
            table.insert(data)

    def update(self, table_name, query, data):
        table = self.db[table_name]
        table.update(data, **query)

    def delete(self, table_name, query):
        table = self.db[table_name]
        table.delete(**query)

    def query(self, table_name, query_str):
        table = self.db[table_name]
        result = table.database.query(query_str)
        return result
