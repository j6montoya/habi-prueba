from classes.server import ApiServer
from http.server import HTTPServer
from os import environ

if __name__ == "__main__":
    
    hostname = environ.get('HOSTNAME', default='localhost')
    port     = int(environ.get('PORT', default=8888))

    apiServer = HTTPServer((hostname, port), ApiServer)
    print("Servidor de API iniciado en http://%s:%s." % (hostname, port))
    
    try:
        apiServer.serve_forever()
    except KeyboardInterrupt:
        pass
    
    apiServer.server_close()
    print("Servidor de API pausado.")