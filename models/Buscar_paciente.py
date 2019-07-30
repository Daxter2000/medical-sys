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

                sql = "select id, Nombres, Apellido_paterno, Apellido_materno FROM pacientes WHERE Nombres LIKE %s OR Apellido_paterno LIKE %s OR Apellido_materno LIKE %s or id LIKE %s"
                cursor.execute(sql,("%" + busqueda + "%","%" + busqueda + "%", "%" + busqueda + "%",  busqueda  , ))
                datos= cursor.fetchall()
                return datos 
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def programar_cita(self):
        try:
            conn = mysql.connector.connect(host='localhost',
                                        database='agenda',
                                        user='root',
                                        password='')

            if conn.is_connected(): 
                #print('Connected to MySQL database')
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM pacientes")
                datos = cursor.fetchall()    
                for row in enumerate (datos):
                    if row[0] == self.tabla.currentRow():
                        data = row[1]
                        return data

        except Error as e:
            print(e)
            #QMessageBox.warning(self,"Eror", e , QMessageBox.Discard )
    
        finally:
            cursor.close()
            conn.close()

