import unittest
import os
from sqlalchemy import create_engine
from lmodel.database import DataBase

class TestDataBaseIntegration(unittest.TestCase):

    def setUp(self):
        # Configurar variáveis de ambiente de teste
        self.db = DataBase()

    def test_database_connection(self):
        # Configurar o objeto DataBase
        self.assertIsNotNone(self.db)

    def test_query_execution(self):
        # Configurar o objeto DataBase
        

        # Inserir dados de teste
        test_data = {'column1': 'value1', 'column2': 'value2'}
        self.db.insert('test_petwatch', test_data)

        # Executar a função query
        result = self.db.search('SELECT * FROM test_petwatch')

        # Verificar se a função foi chamada corretamente
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['column1'], 'value1')
        self.assertEqual(result[0]['column2'], 'value2')

if __name__ == '__main__':
    unittest.main()
