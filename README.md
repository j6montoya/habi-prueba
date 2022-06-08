# habi-prueba

# Tecnologías a usar
- Python 3.9.2 (Virtual Enviroment)
- MySQL
- JSON

# Servicio de consultas

- Se realiza la implementación de servidor HTTP para el consumo del API con la arquitectura REST.
- Se utiliza pymysql para la conexión y consultas a la base de datos.
- El endpoint de consulta de datos es /search al cual se pueden enviar los siguientes parámetros GET en la URL para filtrar la consulta de datos
  - status: (pre_venta, en_venta, vendido) Estado del inmueble
  - city: Ciudad del inmueble
  - year: Año de construcción del inmueble
- Se realizaron pruebas unitarias con unittest para validar la conexión a la base de datos.

- ### Instalación
  Se recomienda instalar un entorno virtual en el directorio de api (opcional)
  ```
    python -m venv .
  ```
  Instalar las dependencias requeridas
  ```
    pip install requirements.txt
  ```
- ### Ejecución
  Variables de entorno de ejecución
  | Variable | Descripción
  |----------|-----------|
  |DB_HOSTNAME|Host de la base de datos por defecto localhost|
  |DB_PORT|Puerto de la base de datos por defecto 3306|
  |DB_USERNAME|Usuario de la base de datos|
  |DB_PASSWORD|Contraseña de la base de datos|
  |DB_NAME|Nombre de la base de datos|
  |HOSTNAME|Hostname del servidor por defecto localhost|
  |PORT|Puerto del servidor por defecto 8888|

  ```
    python app.py
  ```
  Con variables de entorno
  ```
    DB_HOSTNAME= DB_PORT= DB_USERNAME= DB_PASSWORD= DB_NAME= HOSTNAME= PORT= python app.py
  ```
 - ### Consumo del servicio de consultas
   Usaremos curl como ejemplo para el consumo del servicio de consultas.

   Obtener todos los registros según el requerimiento
   ```
   curl http://localhost:8888/search
   ```
   Salida esperada:
   ```
   {
    "response": true,
    "items": [
        {
            "id": 20,
            "address": "Entrada 2 via cerritos",
            "city": "pereira",
            "status_label": "Inmueble publicado en preventa",
            "status": "pre_venta",
            "price": 270000000,
            "description": "Casa campestre con lago"
        }
    }...
   ```
   Obtener los registros segun el requerimiento filtrando por (estado, ciudad o año de construcción)
   ```
   curl http://localhost:8888/search?status=pre_venta&city=pereira&year=2021
   ```
   Salida esperada:
   ```
   {
    "response": true,
    "items": [
        {
            "id": 20,
            "address": "Entrada 2 via cerritos",
            "city": "pereira",
            "status_label": "Inmueble publicado en preventa",
            "status": "pre_venta",
            "price": 270000000,
            "description": "Casa campestre con lago"
        }
    }...
   ```
- ### Ejecución de las pruebas
  Para ejecutar las pruebas ingresar al directorio api/test
  
  Configurar las credenciales de la base de datos, usando las variables de entorno o modificarlas en test_db.py
  | Variable | Descripción
  |----------|-----------|
  |DB_HOSTNAME|Host de la base de datos por defecto localhost|
  |DB_PORT|Puerto de la base de datos por defecto 3306|
  |DB_USERNAME|Usuario de la base de datos|
  |DB_PASSWORD|Contraseña de la base de datos|
  |DB_NAME|Nombre de la base de datos|
  Ejecutar las pruebas
  ```
   python -m unittest test_db.py
  ```
  Con variables de entorno
  ```
    DB_HOSTNAME= DB_PORT= DB_USERNAME= DB_PASSWORD= DB_NAME= HOSTNAME= PORT= python -m unittest test_db.py
  ```
- ### Propuesta de mejora en la estructura de la base de datos de servicio de consultas
  Crear otra tabla (current_status) donde se guarde el estado actual de la propiedad, esto mejoraría la consulta de los inmuebles ya que evita que se deba crear una subconsulta para obtener primero el ultimo valor en la tabla de historíco de estados. En el repositorio se encuentra el modelo propuesto (search_property.png).

  Consulta con el modelo actual
  ```
  SELECT p.id, p.address, p.city, s.label AS status_label, s.name status, p.price, p.description FROM property p
  INNER JOIN (
    SELECT sh.* FROM status_history sh 
    INNER JOIN (SELECT MAX(id) id FROM status_history GROUP BY property_id) msh ON msh.id = sh.id
  ) AS sh ON sh.property_id = p.id
  INNER JOIN status AS s ON s.id = sh.status_id
  WHERE s.name IN ('pre_venta', 'en_venta', 'vendido') AND p.year IS NOT NULL
  ORDER BY sh.update_date DESC
  ```

  Consulta con el modelo propuesto
  ```
  SELECT p.id, p.address, p.city, s.label AS status_label, s.name status, p.price, p.description FROM property p
  INNER JOIN current_status cs ON cs.property_id = p.id
  INNER JOIN status AS s ON s.id = cs.status_id
  WHERE s.name IN ('pre_venta', 'en_venta', 'vendido') AND p.year IS NOT NULL
  ORDER BY cs.update_date DESC
  ```

# Servicio de me gusta

Se realiza un modelo para la implementación de un servicio de me gusta para usuarios registrados, el diagrama del modelo se encuentra en el repositorio (like_property.png).

Se implementaron dos tablas:

current_like: En esta tabla se guarda el estado actual de los "me gusta" del usuario en los inmuebles, este valor es único por inmueble y usuario.

like_history: En esta tabla se guarda el historico de los "me gusta" de los usuarios en los inmuebles, esta valor no es unico ya el usuario puede quitar el "me gusta" y volver a darle "me gusta" a diferencia de la tabla current_like, es un historico de las acciones del usuario en el servicio de "me gusta".

Las tablas se crean con el motor InnoDB ya que son tablas que se usaran de manera transaccional.

```
CREATE TABLE IF NOT EXISTS `current_like` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `property_id` int(11) DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `current_like_id_idx` (`id`),
  KEY `current_like_user_id_idx` (`user_id`),
  KEY `current_like_property_id_idx` (`property_id`),
  CONSTRAINT `FK_current_like_auth_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_current_like_property` FOREIGN KEY (`property_id`) REFERENCES `property` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

CREATE TABLE IF NOT EXISTS `like_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `property_id` int(11) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `like_history_id_idx` (`id`) USING BTREE,
  KEY `like_history_user_id_idx` (`user_id`) USING BTREE,
  KEY `like_history_property_id_idx` (`property_id`) USING BTREE,
  CONSTRAINT `like_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `like_history_ibfk_2` FOREIGN KEY (`property_id`) REFERENCES `property` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;
```