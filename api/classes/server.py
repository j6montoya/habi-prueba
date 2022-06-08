from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qsl
from classes.search import SearchProperty
import json

class ApiServer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        
        parse_path = urlparse(self.path)
        path = parse_path.path.strip('/')
        
        # Validar ruta de servicio de consulta
        if path != 'search':
            
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            self.wfile.write(bytes(json.dumps({
                'response' : False,
                'message'  : 'Página no encontrada'
            }), 'utf-8'))
            
        else:
                        
            params = dict(parse_qsl(parse_path.query))
            
            # Servicio de consulta
            search  = SearchProperty()
            results = search.fetch(params)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            self.wfile.write(bytes(json.dumps(results), 'utf-8'))
