import os

class Historial:
    def __init__(self,id):
        self.id = id


    def leer_historial(self):
        id_str = str(self.id)
        id = id_str +  '.txt'

        here = os.path.dirname(os.path.realpath(__file__))
        subdir = "Historiales"
        filename = id
        filepath = os.path.join(here, subdir, filename)
        
        if os.path.isfile(filepath):

            with  open( filepath,'r') as f:
                data = f.read()
                return data

        else: return "No hay historial de este paciente"




