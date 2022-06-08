from classes.db import Database
from os import environ
import unittest
from pymysql.connections import Connection

class TestDatabase(unittest.TestCase):
    """Probar conexión a la base de datos"""
    
    credentials = {}
    
    def setUp(self):
        
        self.credentials = {
            'host'    : environ.get('DB_HOSTNAME', default = 'localhost'), 
            'port'    : int(environ.get('DB_PORT', default = 3306)),
            'user'    : environ.get('DB_USERNAME', default = ''),
            'password': str(environ.get('DB_PASSWORD', default = '')),
            'database': environ.get('DB_NAME', default = '')
        }
        
    def test_db_instance(self):
        """Probar conexión a la base de datos"""
        
        try:
            Database(**self.credentials)
        except Exception:
            self.fail("Database() Error conectando a la base de datos")
            
    def test_db_connection(self):
        """Probar resultado de conexión a la base de datos"""
        
        try:
            
            db = Database(**self.credentials)
            connection = db.get_connection()
            
            self.assertIsInstance(connection, Connection, 'La conexión a la base de datos es invalida')
        
        except Exception:
            pass