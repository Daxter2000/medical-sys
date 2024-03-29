import mysql.connector
from mysql.connector import Error
#-------------------------------------NUEVO PACIENTE SIN REGISTRO, INCLUYE TODOS LOS CAMPOS EXCEPTO CELULAR Y TELEFONO-----------------------------------------------#
class Nuevo_formulario:
    def __init__( self, nombres, apellido1, apellido2, peso, altura, dx, estudios, medicamento):
        self.nombres = nombres
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.peso = peso
        self.altura = altura
        self.dx = dx
        self.estudios = estudios
        self.medicamento = medicamento


    def registrar_nuevo(self):
        try:
            conn = mysql.connector.connect(host = 'localhost', database = 'agenda', user = 'root', password = '')
            if conn.is_connected:

                cursor= conn.cursor()

                sql = "INSERT INTO pacientes (`Nombres`, `Apellido_paterno`, `Apellido_materno`,`Peso`, `Altura`, `Diagnostico`,`Estudios` ,`Medicamentos`  ) VALUES (%s, %s , %s , %s,  %s, %s, %s, %s);"
                cursor.execute(sql,( self.nombres, self.apellido1, self.apellido2, self.peso, self.altura, self.dx, self.estudios, self.medicamento))
                conn.commit()

        except Error as e:
            print (e)
        finally:
            cursor.close()
            conn.close()
#---------------------------------NUEVO PACIENTE PARA AGENDAR UNA CITA, NO INCLUYE DIAGNOSTICO NI NADA, SOLO NOMBRE Y TELEFONO-----------------------------------------#
class Nuevo_Paciente:
    def __init__( self, nombres, apellido1, apellido2, telefono, celular):
        self.nombres = nombres
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.telefono = telefono
        self.celular = celular


    def registrar_nuevo(self):
        try:
            conn = mysql.connector.connect(host = 'localhost', database = 'agenda', user = 'root', password = '')
            if conn.is_connected:

                cursor= conn.cursor()

                sql = "INSERT INTO pacientes (`Nombres`, `Apellido_paterno`, `Apellido_materno`,`Telefono` ,`Celular`  ) VALUES (%s, %s , %s , %s,  %s);"
                cursor.execute(sql,( self.nombres, self.apellido1, self.apellido2, self.telefono, self.celular))
                conn.commit()


        except Error as e:
            print (e)
        finally:
            cursor.close()
            conn.close()
            
