from classes.db import db

class SearchProperty:
    """Consulta de inmuebles"""
    
    def fetch(self, params = {}):
        """Obtener datos del servicio de consulta de inmuebles

        Args:
            params (dict, optional): Parámetros del filtro de busqueda de inmuebles. Defaults to {}.

        Returns:
            dict: Respuesta de la consulta de datos
        """
        
        connection = db.get_connection()
        
        with connection.cursor() as cursor:
            
            where_sql = ''
            bind_params = []
            
            if 'status' in params:
                where_sql += ' AND s.name = %s'
                bind_params.append(params['status'])
            
            if 'year' in params:
                where_sql += ' AND p.year = %s'
                bind_params.append(params['year'])
            
            if 'city' in params:
                where_sql += ' AND p.city = %s'
                bind_params.append(params['city'])
            
            sql = """SELECT p.id, p.address, p.city, s.label AS status_label, s.name status, p.price, p.description FROM property p
                INNER JOIN (
                    SELECT sh.* FROM status_history sh 
                    INNER JOIN (SELECT MAX(id) id FROM status_history GROUP BY property_id) msh ON msh.id = sh.id
                ) AS sh ON sh.property_id = p.id
                INNER JOIN status AS s ON s.id = sh.status_id
                WHERE s.name IN ('pre_venta', 'en_venta', 'vendido') AND p.year IS NOT NULL %s
                ORDER BY sh.update_date DESC""" % where_sql
            
            cursor.execute(sql, bind_params)
            results = cursor.fetchall()
            
            return {
                'response' : len(results) > 1,
                'items'    : results
            }