import mysql.connector
from mysql.connector import Error


class Buscar:
    def __init__(self, busqueda,tabla):
        self.busqueda = busqueda
        self.tabla = tabla

    def buscar_px(self):

        try:
            conn =  mysql.connector.connect(host= 'localhost', database = 'agenda', user= 'root', password= '')
            if conn.is_connected:
                busqueda = self.busqueda
                
                cursor = conn.cursor()

                sql = "select id, Nombres, Apellido_paterno, Apellido_materno, Telefono, Celular, Ultima_visita FROM pacientes WHERE Nombres LIKE %s OR Apellido_paterno LIKE %s OR Apellido_materno LIKE %s or id LIKE %s"
                cursor.execute(sql,("%" + busqueda + "%","%" + busqueda + "%", "%" + busqueda + "%",  busqueda  , ))
                datos= cursor.fetchall()
                return datos 
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()


class Historial:
        def __init__(self, id):
            self.id = id
        
        def buscar_px(self):
            id = self.id 
            try:
                conn =  mysql.connector.connect(host= 'localhost', database = 'agenda', user= 'root', password= '')
                if conn.is_connected:                  
                    cursor = conn.cursor()
                    sql = 'SELECT  * FROM historial WHERE id_px = %s ;'
                    cursor.execute(sql,(id,))
                    datos= cursor.fetchall()
                    conn.commit()
                    return datos 
            except Error as e:
                print(e)
            finally:
                cursor.close()
                conn.close()
