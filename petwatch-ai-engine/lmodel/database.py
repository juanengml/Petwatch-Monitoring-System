import dataset
from sqlalchemy import create_engine
import os


class DataBase(object):
    def __init__(self):
        self.host = os.environ.get("PETWATCH_DB_HOST")
        self.user = os.environ.get("PETWATCH_DB_USER")
        self.password = os.environ.get("PETWATCH_DB_PASSWORD")
        self.uri = f"mysql://{self.user}:{self.password}@{self.host}"
        self.db = dataset.connect(self.uri)

        # Verificar se o banco de dados "petwatch" existe
        engine = create_engine(self.uri)
        with engine.connect() as connection:
            result = connection.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'petwatch'")
            if not result.fetchone():
                # O banco de dados "petwatch" não existe, então criá-lo
                connection.execute("CREATE DATABASE petwatch")

        # Conectar novamente ao banco de dados "petwatch"
        self.uri += "/petwatch"
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
