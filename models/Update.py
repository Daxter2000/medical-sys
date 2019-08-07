import mysql.connector
from mysql.connector import Error
import os
import datetime

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

    def historial(self):


        id_str = str(self.id)
        id = id_str + '.txt'
        diag = str(self.dx )
        trat = str(self.trat )
        estu= str(self.est )
        alt= str(self.altura )
        peso= str(self.peso )
        hoy = datetime.datetime.today()
        fecha = str(hoy.date())
        hora = hoy.time()
        h = str(hora.hour)
        m = str(hora.minute)


        here = os.path.dirname(os.path.realpath(__file__))
        subdir = "Historiales"
        filename = id
        filepath = os.path.join(here, subdir, filename)

        with  open( filepath,'a') as f:
            f.write('Fecha : \n' + fecha + '\n\n') 
            f.write('Hora : \n' + h + ' : '+ m +   '\n\n') 
            f.write('Altura : \n' + alt + ' metros \n\n') 
            f.write('Peso : \n' + peso + ' kilogramos \n\n')
            f.write('Diagnostico : \n' + diag + '\n\n')
            f.write('Tratamiento : \n' + trat + '\n\n')
            f.write('Estudios a realizar : \n' + estu + '\n\n')
