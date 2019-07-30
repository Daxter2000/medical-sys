import mysql.connector
from mysql.connector import Error
import datetime




class Agregar():
    def __init__(self,id,date,time,datetime):

        self.id = id
        self.date = date
        self.time = time
        self.datetime =  datetime


    def Nueva_cita(self):
        try:
            conn = mysql.connector.connect(host = 'localhost', database = 'Agenda', user = 'root', password = '')

            if conn.is_connected:
                
                cursor = conn.cursor()
                identificador = self.id 
                fecha = self.date 
                hora = self.time 
                datetime = self.datetime
                #formatted_datetime = self.now.strftime('%Y-%m-%d %H:%M:%S')
                #formatted_date = self.date.strftime('%Y-%m-%d')  
                #formatted_hour = self.hour.strftime('%H:%M:%S') 

                # Assuming you have a cursor named cursor you want to execute this query on:
                cursor.execute('insert into citas (identificador, fecha, hora,  datetime) values(%s, %s,%s,%s)', (identificador, fecha, hora, datetime))  
                conn.commit()
                return True
            
        except Error as e:
            print (e)
            return False
        finally:
            conn.close()
            cursor.close()

