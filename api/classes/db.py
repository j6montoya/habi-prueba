import pymysql
from os import environ

class Database:
    
    _connection = None
    
    def __init__(self, 
            host=environ.get('DB_HOSTNAME', default='localhost'), 
            port=int(environ.get('DB_PORT', default=3306)),
            user=environ.get('DB_USERNAME', default=''),
            password=str(environ.get('DB_PASSWORD', default='')),
            database=environ.get('DB_NAME', default='')):
        
        self._connection = pymysql.connect(host=host, port=port, user=user, password=password, database=database, cursorclass=pymysql.cursors.DictCursor)
    
    def get_connection(self):
        return self._connection
    
db = Database()