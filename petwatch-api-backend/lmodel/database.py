import dataset

class DataBase(object):
    def __init__(self, uri='sqlite:///petwatch.db'):
        self.uri = uri
        self.db = dataset.connect(self.uri)

    def search(self, query):
        try:
           return [dict(row) for row in self.db.query(query)]
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

    def delete(self, table_name, nome):
        table = self.db[table_name]
        table.delete(nome=nome)

    def query(self, query):
        self.db.query(query)
