import mysql.connector
from mysql.connector import Error


class Insertar:
    def __init__(self,nom,passw,funcion): 
        self.nom = nom
        self.passw = passw
        self.funcion =  funcion


    def insertar(self):
        try:
            conn = mysql.connector.connect(host = 'localhost' , database = 'agenda', user = 'root' , password = '')

            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute('insert into usuarios (nombre, pass, funcion) values (%s, %s,%s)', (self.nom, self.passw, self.funcion))
                conn.commit()
                return True
    
        except Error as e:
            print(e)
        finally:
            conn.close()
            cursor.close()

class Actualizar:
    def __init__(self,nom,passw,funcion,id): 
        self.nom = nom
        self.passw = passw
        self.funcion =  funcion
        self.id = id


    def actualizar(self):
        try:
            conn = mysql.connector.connect(host = 'localhost' , database = 'agenda', user = 'root' , password = '')

            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute('update usuarios set nombre = %s, pass = %s, funcion = %s WHERE id = %s ', (self.nom, self.passw, self.funcion, self.id))
                conn.commit()
                return True
    
        except Error as e:
            print(e)
        finally:
            conn.close()
            cursor.close()

class Borrar:
    def __init__(self,id): 
        self.id = id

    def borrar(self):

        try:
            conn = mysql.connector.connect(host = 'localhost' , database = 'agenda', user = 'root' , password = '')

            if conn.is_connected():
                cursor = conn.cursor()
                sql = 'DELETE  FROM usuarios WHERE id = %s ; '
                cursor.execute(sql,(self.id,))
                conn.commit()
                return True

        except Error as e:
            print(e)
        finally:
            conn.close()
            cursor.close()
