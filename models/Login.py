import mysql.connector 
from mysql.connector import Error

class Conectar:
    def __init__(self, host, database, user, password, usuario, passw):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.usuario = usuario
        self.passw = passw

    def logIn(self):
        try:
            conn = mysql.connector.connect(host =self.host ,
                                    database = self.database, user = self.user, password = self.password)

            if conn.is_connected():
                cursor = conn.cursor()
                usuario = self.usuario
                contraseña = self.passw
                
                if usuario == "":
                    return usuario
                elif contraseña == "":
                    return contraseña
                else:
                    cursor.execute("SELECT * FROM usuarios WHERE nombre = %s AND  pass = %s", (usuario,contraseña))
                    datos = cursor.fetchall()
                    conn.commit()
                    numero = cursor.rowcount
                    if numero == 0 :
                        return numero
                    else: 
                        for dato in datos:
                            nombre = dato[1]
                            puesto = dato[3]
                            if puesto == "Admin":
                                return puesto
                            elif puesto == "Asistente":
                                return puesto
                            elif puesto == "Medico":
                                return puesto 




        except Error as e:
            print (e)
            
        finally:
            conn.close()
            cursor.close()
            


