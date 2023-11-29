import unittest
import os
from sqlalchemy import create_engine
from lmodel.database import DataBase
import dataset


class TestDataBaseIntegration(unittest.TestCase):

    def setUp(self):
        # Configurar variáveis de ambiente de teste
        self.db = DataBase()

    def tearDown(self):
        # Limpar variáveis de ambiente de teste
        self.host = os.environ.get("PETWATCH_DB_HOST")
        self.user = os.environ.get("PETWATCH_DB_USER")
        self.password = os.environ.get("PETWATCH_DB_PASSWORD")
        self.uri = f"mysql://{self.user}:{self.password}@{self.host}/petwatch"
        self.db = dataset.connect(self.uri)

        # Verificar se o banco de dados "petwatch" existe
        engine = create_engine(self.uri)
        with engine.connect() as connection:
            connection.execute("DROP TABLE IF EXISTS test_petwatch")

    def test_database_connection(self):
        # Configurar o objeto DataBase
        db = DataBase()

        # Verificar se a conexão é bem-sucedida
        self.assertIsNotNone(db.db)

    def test_query_execution(self):
        # Configurar o objeto DataBase
        db = DataBase()

        # Inserir dados de teste
        test_data = {'column1': 'value1', 'column2': 'value2'}
        db.insert('test_petwatch', test_data)

        # Executar a função query
        result = db.search('SELECT * FROM test_petwatch')

        # Verificar se a função foi chamada corretamente
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0]['column1'], 'value1')
        self.assertEqual(result[0]['column2'], 'value2')

if __name__ == '__main__':
    unittest.main()
