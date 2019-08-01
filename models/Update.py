import mysql.connector
from mysql.connector import Error


class Actualizar_diagnostico:
    def __init__(self,id,peso, altura, dx, est, trat):
        
        self.id = id
        self.peso = peso
        self.altura = altura
        self.dx = dx
        self.est = est
        self.trat = trat

    def Actualizar(self):

        try:
            conn = mysql.connector.connect(host = 'localhost', database = 'agenda', user = 'root', password = '')
            if conn.is_connected:

                cursor= conn.cursor()

                sql = " INSERT INTO historial (`id_px`, `diagnostico`, `estudios`,`tratamiento`, `peso`,`altura`  ) VALUES (%s, %s , %s , %s, %s , %s);"
                cursor.execute(sql,( self.id, self.dx, self.est, self.trat, self.altura, self.peso))
                conn.commit()

        except Error as e:
            print(e)
        finally:
            conn.close()
            cursor.close()
