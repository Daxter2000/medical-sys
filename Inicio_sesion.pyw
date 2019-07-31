import sys 
from models import Login, Formulario, Buscar_paciente, Agregar_cita
from inicio import *
from medico import *
from asistente import *
from admin import *
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import Qt
import mysql.connector 
from mysql.connector import Error
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication,QMainWindow, QDialog, QLineEdit, QPushButton, QTableWidget, QGridLayout,
                             QTableWidgetItem, QAbstractItemView, QHeaderView, QMenu, QPlainTextEdit,
                             QActionGroup, QAction, QMessageBox)


#------------------------CLASES DEL MENU PRINCIPAL----------------------------------------------#

class Nueva_Cita(QDialog):
    def __init__(self,id,nom,ap1,ap2):
        QDialog.__init__(self)
        uic.loadUi("agregar_consulta.ui",self)
        self.id = id
        self.nombre =  nom
        self.apellido1 = ap1
        self.apellido2  = ap2


        #----------------BOTONES ---------------------------#
        self.date_ac.dateChanged.connect(self.obtener_datos_pararegistrar)
        self.time_ac.timeChanged.connect(self.obtener_datos_pararegistrar)
        self.acept_ac.clicked.connect(self.nueva)

        #---------------Rellenar los datos de los campos con los datos de la  persona seleccionada del campo buscar 
        self.nombre_ac.setText(self.nombre)
        self.ap1_ac.setText(self.apellido1)
        self.ap2_ac.setText(self.apellido2)
        self.id_ac.setText(self.id)

        # FUNCION QUE NOS ACTUALIZA LOS DATOS Y LOS GUARDA EN VARIABLES CADA  QUE SE CAMBIA UNA FECHA U HORA

    def obtener_datos_pararegistrar(self):
        self.fecha = self.date_ac.date().toString("yyyy-MM-dd")
        self.hora = self.time_ac.time().toString("HH-mm-ss")
        self.datetime = self.fecha + " " + self.hora

    def nueva(self):
        nueva_cita = Agregar_cita.Agregar(int(self.id),self.fecha, self.hora, self.datetime)
        #nueva_cita.Nueva_cita()

        if nueva_cita.Nueva_cita():
            QMessageBox.information(self,"Cita registrada", "Cita registrada con exito", QMessageBox.Ok)
            self.nombre_ac.clear()
            self.ap1_ac.clear()
            self.ap2_ac.clear()
            self.id_ac.clear()
            self.close()

            

        else:
            print("intente de nuevo")


        

class Abrir_Agenda (QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("Agenda.ui",self)

class Buscar_px(QDialog):
    def __init__(self):
        QDialog. __init__(self)
        uic.loadUi("buscar_px.ui",self)
 
        # Deshabilitar edición
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Deshabilitar el comportamiento de arrastrar y soltar
        self.tabla.setDragDropOverwriteMode(False)
        # Seleccionar toda la fila
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        # Seleccionar una fila a la vez
        self.tabla.setSelectionMode(QAbstractItemView.SingleSelection)
        # Especifica dónde deben aparecer los puntos suspensivos "..." cuando se muestran
        # textos que no encajan
        self.tabla.setTextElideMode(Qt.ElideRight)# Qt.ElideNone
        # Establecer el ajuste de palabras del texto 
        self.tabla.setWordWrap(False)
        # Deshabilitar clasificación
        self.tabla.setSortingEnabled(False)
        # Ocultar encabezado vertical
        self.tabla.verticalHeader().setVisible(False)
#----------------------------------------------BOTONES PARA EL AREA DE BUSCAR ------------------------------------------
        self.lineEdit_busqueda.textEdited.connect(self.busqueda)
        self.pb_agregar_nuevo_B.clicked.connect(self.progra)

    def busqueda(self):
        texto = self.lineEdit_busqueda.text()
        nueva_busqueda = Buscar_paciente.Buscar(texto.lower(), self.tabla)
        datos = nueva_busqueda.buscar_px()

        self.tabla.clearContents()

        row = 0
        for endian in datos:
            self.tabla.setRowCount(row + 1)
                                    
            self.tabla.setItem(row, 0, QTableWidgetItem(str(endian[0])))
            self.tabla.setItem(row, 1, QTableWidgetItem(endian[1]))
            self.tabla.setItem(row, 2, QTableWidgetItem(str(endian[2])))
            self.tabla.setItem(row, 3, QTableWidgetItem(str(endian[3])))

            row += 1   
    def progra(self):
        texto = self.lineEdit_busqueda.text()
        nueva_busqueda = Buscar_paciente.Buscar(texto.lower(), self.tabla)
        datos = nueva_busqueda.buscar_px()
        for row in enumerate (datos):
            if row[0] == self.tabla.currentRow():
                data = row[1]
                id = (str(data[0]))
                nombres = data[1]
                apellido1 = data[2]
                apellido2 = data[3]
                self.agregar = Nueva_Cita(id,nombres,apellido1,apellido2)
                self.agregar.show()
                
                



    
    

            
        


class Nuevo_Formulario(QMainWindow):
    def __init__(self):
        QMainWindow. __init__(self)
        uic.loadUi("formulario.ui",self)
        self.pb_actualizar.clicked.connect(self.registrar_nuevo)


    def registrar_nuevo(self):
            nombres = self.lineEdit_nombres_F.text()
            apellido_pat = self.lineEdit_ape_pat_F.text()
            apellido_mat = self.lineEdit_ape_mat_F.text()
            peso = self.lineEdit_peso.text()
            altura = self.lineEdit_altura.text()
            dx = self.plainTextEdit_Dx.toPlainText()
            estudios = self.plainTextEdit_Estudios.toPlainText()
            med = self.plainTextEdit_Med.toPlainText()
            if nombres =="":
                QMessageBox.warning(self,"Datos faltantes", "Falta ingresar un nombre", QMessageBox.Discard)
            elif apellido_pat == "":
                QMessageBox.warning(self,"Datos faltantes", "Falta ingresar un apellido paterno", QMessageBox.Discard) 
            elif apellido_mat == "":
                QMessageBox.warning(self,"Datos faltantes", "Falta ingresar un apellido materno", QMessageBox.Discard)
            elif dx =="":
                QMessageBox.warning(self,"Datos faltantes", "Falta ingresar diagnostico", QMessageBox.Discard)
            else:

                formulario = Formulario.Nuevo_formulario(nombres.lower(), apellido_pat.lower(), apellido_mat.lower(), peso.lower(), altura.lower(), dx.lower(), estudios.lower(), med.lower() )
                formulario.registrar_nuevo()
            
                QMessageBox.information(self,"Datos guardados", "Paciente registrado con exito", QMessageBox.Ok)
                nombres = self.lineEdit_nombres_F.clear()
                apellido_pat = self.lineEdit_ape_pat_F.clear()
                apellido_mat = self.lineEdit_ape_mat_F.clear()
                peso = self.lineEdit_peso.clear()
                altura = self.lineEdit_altura.clear()
                dx = self.plainTextEdit_Dx.clear()
                estudios = self.plainTextEdit_Estudios.clear()
                med = self.plainTextEdit_Med.clear()



class Historial(QMainWindow):
    def __init__(self):
        QMainWindow. __init__(self)
        uic.loadUi("Historial.ui",self)


#------------------------------------- OPERACIONES PARA EL MEDICO------------------------------------------------#

class Principal_Medico(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("medico.ui",self)
        #RELACINAR LAS CLASES CON LOS METODOS
        self.agregar = Nueva_Cita('','','','')
        self.abrirAgenda = Abrir_Agenda()
        self.buscarpx = Buscar_px()
        self.formulario = Nuevo_Formulario()
        self.historial = Historial()
    

        #AGREGAR ACCIONES A LOS BOTONES DEL MENU
        self.Btn_agregarcita_m.clicked.connect(self.agregar_cita)
        self.Btn_Agenda_m.clicked.connect(self.abrir_agenda)
        self.Btn_buscarpaciente_m.clicked.connect(self.buscarPx)
        self.Btn_nuevopaciente_m.clicked.connect(self.nuevo_formulario)
        self.btn_historialclinico_m.clicked.connect(self.historial_Clinico)


    #-----------------------DECLARAR METODOS PARA ABRIR LAS OPCIONES DEL MENU----------------#
    def agregar_cita(self):
        self.agregar.show()   
    
    def abrir_agenda(self):
        self.abrirAgenda.show()

    def buscarPx(self):
        self.buscarpx.show()

    def nuevo_formulario(self):
        self.formulario.show()

    def historial_Clinico(self):
        self.historial.show()


#---------------------------------- OPERACIONES PARA EL ASISTENTE  ----------------------------------------#

class Principal_Asistente(QMainWindow):
    def __init__(self):
        
        QMainWindow.__init__(self)
        uic.loadUi("asistente.ui",self)
        #self.pb_agenda_a = QPushButton(self)
        #self.pb_agregarcita_a = QPushButton(self)
        #self.pb_buscarPx_a = QPushButton(self)
        #self.pb_receta_a =  QPushButton(self)

        #RELACINAR LAS CLASES CON LOS METODOS
        self.agregar = Nueva_Cita('','','','')
        self.abrirAgenda = Abrir_Agenda()
        self.buscarpx = Buscar_px()
        self.formulario = Nuevo_Formulario()
        self.historial = Historial()

        #-----------------Funciones de los botones--------------------#

        self.pb_agenda_a.clicked.connect(self.abrir_agenda)
        self.pb_agregarcita_a.clicked.connect(self.agregar_cita)
        self.pb_buscarPx_a.clicked.connect(self.buscarPx)
        

    #-----------------DECLARAR METODOS PARA ABRIR LAS OPCIONES DEL MENU-----------------------#
    def agregar_cita(self):
        self.agregar.show()   
    
    def abrir_agenda(self):
        self.abrirAgenda.show()

    def buscarPx(self):
        self.buscarpx.show()

    def nuevo_formulario(self):
        self.formulario.show()

    def historial_Clinico(self):
        self.historial.show()
#-------------------------------------OPERACIONES PARA EL ADMINISTRADOR--------------------------------------#

class Principal_Admin(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("admin.ui",self)


        #RELACINAR LAS CLASES CON LOS METODOS
        self.agregar = Nueva_Cita('','','','')
        self.abrirAgenda = Abrir_Agenda()
        self.buscarpx = Buscar_px()
        self.formulario = Nuevo_Formulario()
        self.historial = Historial()

        #-----------------Funciones de los botones--------------------#

        self.pb_agregarcita_adm.clicked.connect(self.agregar_cita)
        self.pb_agenda_adm.clicked.connect(self.abrir_agenda)
        self.pb_buscarPx_adm.clicked.connect(self.buscarPx)
        self.pb_nuevoPx_adm.clicked.connect(self.nuevo_formulario)
        self.pb_historial_adm.clicked.connect(self.historial_Clinico)
        

    #DECLARAR METODOS PARA ABRIR LAS OPCIONES DEL MENU
    def agregar_cita(self):
        self.agregar.show()   
    
    def abrir_agenda(self):
        self.abrirAgenda.show()

    def buscarPx(self):
        self.buscarpx.show()

    def nuevo_formulario(self):
        self.formulario.show()

    def historial_Clinico(self):
        self.historial.show()

#---------------------------------------PANTALLA PRINCIPAL, INICIO DE SESION------------------------------------#


class Inicio_Sesion(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("inicio.ui",self)


        self.btn_aceptar_inicio.clicked.connect(self.iniciar)
        self.lineEdit_pass.setEchoMode(QLineEdit.Password)

        self.principal_medico = Principal_Medico()
        self.principal_asistente = Principal_Asistente()
        self.principal_admin = Principal_Admin()

    def iniciar(self):
        user = self.lineEdit_user.text()
        passw = self.lineEdit_pass.text()
        inicio = Login.Conectar('localhost','agenda','root','',user,passw)
        if inicio.logIn()=='Admin':
            self.principal_admin.show()
            self.close()
        elif inicio.logIn()=='Medico':
            self.principal_medico.show()
            self.close()
        elif inicio.logIn()=='Asistente':
            self.principal_asistente.show()
            self.close()
        elif inicio.logIn()=='':
            QMessageBox.warning(self,"Datos Faltantes","Se requiere el  nombre de usuario y contraseña ", QMessageBox.Discard)
        elif inicio.logIn()== 0:
            QMessageBox.warning(self,"Datos incorrectos","El nombre de usuario o contraseña son incorrectos, contacte con su administrador", QMessageBox.Discard)
    


    

app = QApplication(sys.argv)
myapp = Inicio_Sesion()
myapp.show()
sys.exit(app.exec_())
