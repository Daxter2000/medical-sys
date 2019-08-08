
import mysql.connector
from mysql.connector import Error


class Consultar_citas:
    def __init__(self,dato):   
        self.dato = dato



    def obtener_bd(self):
        try:
            conn = mysql.connector.connect(host = 'localhost' , database = 'agenda', user = 'root' , password = '')

            if conn.is_connected():
                cursor = conn.cursor()
                sql = 'SELECT *  FROM citas WHERE fecha = %s ORDER BY hora ; '
                cursor.execute(sql,(self.dato,))
                datos = cursor.fetchall()
                conn.commit()
                return datos 
    
        except Error as e:
            print(e)
        finally:
            conn.close()
            cursor.close()


    def eliminar(self):
        try:
            conn = mysql.connector.connect(host = 'localhost' , database = 'agenda', user = 'root' , password = '')

            if conn.is_connected():
                cursor = conn.cursor()
                sql = 'DELETE  FROM citas WHERE id_cita = %s ; '
                cursor.execute(sql,(self.dato,))
                conn.commit()
        except Error as e:
            print(e)
        finally:
            conn.close()
            cursor.close()


