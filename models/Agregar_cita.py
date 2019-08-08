import mysql.connector
from mysql.connector import Error
import datetime




class Agregar():
    def __init__(self,id,date,time,nom,ap1,ap2):

        self.id = id
        self.date = date
        self.time = time
        self.nom =  nom
        self.ap1 = ap1
        self.ap2 = ap2


    def Nueva_cita(self):
        try:
            conn = mysql.connector.connect(host = 'localhost', database = 'Agenda', user = 'root', password = '')

            if conn.is_connected:
                
                cursor = conn.cursor()
                identificador = self.id 
                fecha = self.date 
                hora = self.time
                nombre = self.nom
                ape_p = self.ap1
                ape_m = self.ap2
                #print("la hora es : ", hora )
                #formatted_datetime = self.now.strftime('%Y-%m-%d %H:%M:%S')
                #formatted_date = self.date.strftime('%Y-%m-%d')  
                #formatted_hour = self.hour.strftime('%H:%M:%S') 

                # Assuming you have a cursor named cursor you want to execute this query on:
                cursor.execute('insert into citas (identificador, fecha, hora, nombres, ape1, ape2 ) values(%s, %s,%s,%s,%s,%s)', (identificador, fecha, hora, nombre, ape_p, ape_m))  
                conn.commit()
                return True
            
        except Error as e:
            print (e)
            return False
        finally:
            conn.close()
            cursor.close()

