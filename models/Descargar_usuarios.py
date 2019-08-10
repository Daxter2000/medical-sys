
import mysql.connector
from mysql.connector import Error


class Descargar_usuarios:
    def __init__(self): 
        pass


    def obtener_bd(self):
        try:
            conn = mysql.connector.connect(host = 'localhost' , database = 'agenda', user = 'root' , password = '')

            if conn.is_connected():
                cursor = conn.cursor()
                sql = 'SELECT *  FROM usuarios '
                cursor.execute(sql)
                datos = cursor.fetchall()
                conn.commit()
                return datos 
    
        except Error as e:
            print(e)
        finally:
            conn.close()
            cursor.close()