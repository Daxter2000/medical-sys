import mysql.connector
from mysql.connector import Error


class Modificar():
    def __init__(self,id,nom,ap1,ap2,tel,cel):
        self.id = id
        self.nom = nom
        self.ap1 = ap1
        self.ap2 =  ap2
        self.tel = tel
        self.cel = cel


    def cambiar(self):
        try:
            conn = mysql.connector.connect(host = 'localhost', database = 'Agenda', user = 'root', password = '')

            if conn.is_connected:
                
                cursor = conn.cursor()
                id = self.id 
                nom = self.nom
                ap1 = self.ap1
                ap2 = self.ap2
                tel = self.tel
                cel = self.cel
                cursor.execute('UPDATE  pacientes  SET Nombres = %s, Apellido_paterno = %s , Apellido_materno = %s, Telefono = %s, Celular  = %s WHERE id = %s ;', (nom, ap1, ap2, tel, cel, id))
                conn.commit()
                
            
        except Error as e:
            print (e)
            return False
        finally:
            conn.close()
            cursor.close()
