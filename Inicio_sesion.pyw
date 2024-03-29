import sys 
from models import (Login, Formulario, Buscar_paciente, Agregar_cita, Update, Historiales,Descargar_citas,
                    modificar_usuario, Descargar_usuarios, Insertar_usuario)
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import Qt
import mysql.connector 
from mysql.connector import Error
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication,QMainWindow, QDialog, QLineEdit, QPushButton, QTableWidget, QGridLayout,
                             QTableWidgetItem, QAbstractItemView, QHeaderView, QMenu, QPlainTextEdit,
                             QActionGroup, QAction, QMessageBox)


#------------------------CLASES DEL MENU PRINCIPAL----------------------------------------------#
##--------------------   MODULO CREADO PARA ASIGNAR FECHA Y HORA A LOS PACIENTES PARA CITA MEDICA 

class Nueva_Cita(QDialog):
    def __init__(self,id,nom,ap1,ap2,cel,tel):
        QDialog.__init__(self)
        uic.loadUi("agregar_consulta.ui",self)
        self.id = id
        self.nombre =  nom
        self.apellido1 = ap1
        self.apellido2  = ap2
        self.cel = cel
        self.tel = tel


        #----------------BOTONES ---------------------------#
        self.date_ac.dateChanged.connect(self.obtener_datos_pararegistrar)
        self.time_ac.timeChanged.connect(self.obtener_datos_pararegistrar)
        self.acept_ac.clicked.connect(self.nueva)
        self.cancelar_ac.clicked.connect(self.cerrar)

        #---------------Rellenar los datos de los campos con los datos de la  persona seleccionada del campo buscar 
        self.nombre_ac.setText(self.nombre)
        self.ap1_ac.setText(self.apellido1)
        self.ap2_ac.setText(self.apellido2)
        self.id_ac.setText(self.id)
        self.tel_ac.setText(self.tel)
        self.cel_ac.setText(self.cel)

        # FUNCION QUE NOS ACTUALIZA LOS DATOS Y LOS GUARDA EN VARIABLES CADA  QUE SE CAMBIA UNA FECHA U HORA

    def obtener_datos_pararegistrar(self):
        self.fecha = self.date_ac.date().toString("yyyy-MM-dd")
        self.hora = self.time_ac.time().toString("HH:mm:ss")

        #self.datetime = self.fecha + " " + self.hora
    def nueva(self):
        nueva_cita = Agregar_cita.Agregar(int(self.id),self.fecha, self.hora, self.nombre, self.apellido1, self.apellido2)
    
        if nueva_cita.Nueva_cita():
            QMessageBox.information(self,"Cita registrada", "Cita registrada con exito", QMessageBox.Ok)
            self.nombre_ac.clear()
            self.ap1_ac.clear()
            self.ap2_ac.clear()
            self.id_ac.clear()
            self.close()

        else:
            print("intente de nuevo")
    
    def cerrar(self):
        self.close()


class Nueva_Cita_con_fecha(QDialog):
        def __init__(self,id,nom,ap1,ap2,cel,tel,fecha):
            QDialog.__init__(self)
            uic.loadUi("agregar_consulta.ui",self)
            self.id = id
            self.nombre =  nom
            self.apellido1 = ap1
            self.apellido2  = ap2
            self.cel = cel
            self.tel = tel
            self.fecha = fecha
    
    
            #----------------BOTONES ---------------------------#
            self.date_ac.dateChanged.connect(self.obtener_datos_pararegistrar)
            self.time_ac.timeChanged.connect(self.obtener_datos_pararegistrar)
            self.acept_ac.clicked.connect(self.nueva)
            self.cancelar_ac.clicked.connect(self.cerrar)
    
            #---------------Rellenar los datos de los campos con los datos de la  persona seleccionada del campo buscar 
            self.nombre_ac.setText(self.nombre)
            self.ap1_ac.setText(self.apellido1)
            self.ap2_ac.setText(self.apellido2)
            self.id_ac.setText(self.id)
            self.tel_ac.setText(self.tel)
            self.cel_ac.setText(self.cel)
            self.date_ac.setDate(self.fecha)
    
            # FUNCION QUE NOS ACTUALIZA LOS DATOS Y LOS GUARDA EN VARIABLES CADA  QUE SE CAMBIA UNA FECHA U HORA
    
        def obtener_datos_pararegistrar(self):
            self.fecha = self.date_ac.date().toString("yyyy-MM-dd")
            self.hora = self.time_ac.time().toString("HH:mm:ss")
    
            #self.datetime = self.fecha + " " + self.hora
        def nueva(self):
            nueva_cita = Agregar_cita.Agregar(int(self.id),self.fecha, self.hora, self.nombre, self.apellido1, self.apellido2)
        
            if nueva_cita.Nueva_cita():
                QMessageBox.information(self,"Cita registrada", "Cita registrada con exito", QMessageBox.Ok)
                self.nombre_ac.clear()
                self.ap1_ac.clear()
                self.ap2_ac.clear()
                self.id_ac.clear()
                self.close()
    
            else:
                print("intente de nuevo")
        
        def cerrar(self):
            self.close()

class Abrir_Agenda (QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("Agenda.ui",self)

        self.calendarWidget.selectionChanged.connect(self.Obtener_fecha)
        self.pb_iniciar.clicked.connect(self.iniciar_cita)
        self.pb_eliminar.clicked.connect(self.eliminar_cita)
        self.pb_revision.clicked.connect(self.revision_sin_cita)
        self.pb_agregar.clicked.connect(self.programar_cita)
        self.pb_volver.clicked.connect(self.volver)

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


    def Obtener_fecha(self):
        fecha = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        nuevo = Descargar_citas.Consultar_citas(fecha)
        datos = nuevo.obtener_bd()


        self.tabla.clearContents()

        row = 0
        for endian in datos:
            self.tabla.setRowCount(row + 1)
                                        
            self.tabla.setItem(row, 0, QTableWidgetItem(str(endian[0])))
            self.tabla.setItem(row, 1, QTableWidgetItem(str(endian[2])))
            self.tabla.setItem(row, 2, QTableWidgetItem(str(endian[3])))
            self.tabla.setItem(row, 3, QTableWidgetItem(str(endian[4])))
            self.tabla.setItem(row, 4, QTableWidgetItem(str(endian[5])))
   
            row += 1  

    def iniciar_cita(self):
        fecha = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        nuevo = Descargar_citas.Consultar_citas(fecha)
        datos = nuevo.obtener_bd()
        for row in enumerate (datos):
            if row[0] == self.tabla.currentRow():
                data = row[1]
                id = str(data[0])
                nombres = data[3]
                ap1 = data[4]
                ap2 = data[5]
                self.nuevo = Nuevo_Formulario_Px_Registrado(id,nombres,ap1,ap2)
                self.nuevo.show()

    
    def eliminar_cita(self):
        fecha = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        nuevo = Descargar_citas.Consultar_citas(fecha)
        datos = nuevo.obtener_bd()
        for row in enumerate (datos):
            if row[0] == self.tabla.currentRow():
                data = row[1]
                id_cita = data[7]
                respuesta = QMessageBox.question(self,"Borrar cita", "¿ Esta seguro de borrar la cita ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if respuesta == QMessageBox.Yes:
                    nuevo = Descargar_citas.Consultar_citas(id_cita)
                    nuevo.eliminar()
                    self.Obtener_fecha()
                if respuesta == QMessageBox.No : 
                    self.Obtener_fecha()                    

    def revision_sin_cita(self):
        self.nuevo =  Buscar_Pacientes_Consulta()
        self.nuevo.show()
        self.close()

    def programar_cita(self):
        fecha = self.calendarWidget.selectedDate()
        self.nuevo = Buscar_px_con_fecha(fecha)
        self.nuevo.show()

    def volver(self):
        self.calendarWidget.showToday()
        self.close()
        


class Buscar_px_con_fecha(QDialog):
    def __init__(self,fecha):
        QDialog. __init__(self)
        uic.loadUi("buscar_px.ui",self)
        self.label_buscar.setText("Seleccione el paciente al cual desea programar")
        self.fecha = fecha

        #------------------- Agregar nuevo paciente
        self.nueva = Paciente_consulta()
        #----------------------
 
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
        self.pb_nuevopx.clicked.connect(self.nuevo)
        self.bt_cancel.clicked.connect(self.cerrar)
    
    def cerrar(self):
        self.lineEdit_busqueda.clear()
        self.busqueda()
        self.close()

    def nuevo(self):
        self.nueva.show()

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
                cel = data[4]
                tel = data[5]
                self.agregar = Nueva_Cita_con_fecha(id,nombres,apellido1,apellido2,cel,tel,self.fecha)
                self.agregar.show()
                self.close()


    #-----------------------------------  MODULO PARA BUSCAR PACIENTES  PARA AGENDAR CITA  -------------- -#

class Buscar_px(QDialog):
    def __init__(self):
        QDialog. __init__(self)
        uic.loadUi("buscar_px.ui",self)
        self.label_buscar.setText("Seleccione el paciente al cual desea programar")

        #------------------- Agregar nuevo paciente
        self.nueva = Paciente_consulta()
        #----------------------
 
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
        self.pb_nuevopx.clicked.connect(self.nuevo)
        self.bt_cancel.clicked.connect(self.cerrar)
    
    def cerrar(self):
        self.lineEdit_busqueda.clear()
        self.busqueda()
        self.close()

    def nuevo(self):
        self.nueva.show()

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
                cel = data[4]
                tel = data[5]
                self.agregar = Nueva_Cita(id,nombres,apellido1,apellido2,cel,tel)
                self.agregar.show()
                self.close()


                
    #----------------------------------------MODULO PARA INICIAR CITA Y REGISTRO DE PACIENTE QUE NO ESTA REGISTRADO

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



class Busqueda_historial(QDialog):
    def __init__(self):
        QDialog. __init__(self)
        uic.loadUi("Buscar_px.ui",self)
        #------------------- Agregar nuevo paciente   #----------------------
        self.label_buscar.setText("Seleccione el paciente para obtener Historial")
        self.pb_agregar_nuevo_B.setText("Consultar Historial")
        self.pb_nuevopx.setVisible(False)

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
        self.bt_cancel.clicked.connect(self.cerrar)

    def cerrar(self):
        self.lineEdit_busqueda.clear()
        self.busqueda()
        self.close()

    #---------------------------metodo que rellena la tabla con la busqueda
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
            #--------------------------------METODO  
    def progra(self):
        texto = self.lineEdit_busqueda.text()
        nueva_busqueda = Buscar_paciente.Buscar(texto.lower(), self.tabla)
        datos = nueva_busqueda.buscar_px()
        for row in enumerate (datos):
            if row[0] == self.tabla.currentRow():
                data = row[1]
                id = data[0]
                nom = data[1]
                ap1 = data [2]
                ap2 = data[3]
                self.nuevo = Historial(id,nom,ap1,ap2)
                self.nuevo.show()

                    
class Historial(QMainWindow):
    def __init__(self,id,nom,ap1,ap2):
        QMainWindow. __init__(self)
        uic.loadUi("Historial.ui",self)

        self.id = id
        self.nom =  nom
        self.ap1 = ap1
        self.ap2 = ap2

    #----------------------------------Agregar los valores del buscador a los campos de texto vacios
        self.nombres.setText(self.nom)
        self.apellido_p.setText(self.ap1)
        self.apellido_m.setText(self.ap2)
        self.identificador.setText(str(self.id))
        historia = Historiales.Historial(self.id)
        datos = historia.leer_historial()
        self.text_historial.setPlainText(datos)

        self.pb_consultar.clicked.connect(self.iniciar_consulta)
        self.pb_cancelar.clicked.connect(self.cerrar)


    def iniciar_consulta(self):
        self.agregar = Nuevo_Formulario_Px_Registrado(str(self.id), self.nom, self.ap1, self.ap2)
        self.agregar.show()
        self.close()

    def cerrar(self):
        self.close()


class Configuracion(QDialog):
    def __init__(self):
        QDialog. __init__(self)
        uic.loadUi("Config.ui",self)
        self.pb_modif.clicked.connect(self.config)
        self.pb_admin_users.clicked.connect(self.modificar)

    def modificar(self):
        self.modif = Modificar_usuarios()
        self.modif.show()

    def config(self):
        self.nuevo = Buscar_para_configurar()
        self.nuevo.show()


class Buscar_para_configurar(QDialog):
    def __init__(self):
        QDialog. __init__(self)
        uic.loadUi("buscar_px.ui",self)
        self.label_buscar.setText("Seleccione el paciente al cual desea configurar")

        #------------------- Agregar nuevo paciente
        self.nueva = Paciente_consulta()
        #----------------------
 
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
        self.pb_nuevopx.clicked.connect(self.nuevo)
        self.bt_cancel.clicked.connect(self.cerrar)
    
    def cerrar(self):
        self.lineEdit_busqueda.clear()
        self.busqueda()
        self.close()

    def nuevo(self):
        self.nueva.show()

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
                cel = data[4]
                tel = data[5]
                self.configurar = Modificar_nombre(id,nombres,apellido1,apellido2,tel,cel)
                self.configurar.show()
                self.close()


class Modificar_nombre(QDialog):
    def __init__(self,id, nom, ap1, ap2, tel, cel):
        QDialog.__init__(self)
        uic.loadUi("agregar_px.ui",self)
        self.id = id
        self.nombre = nom
        self.apellido_p = ap1
        self.apellido_m =  ap2
        self.telefono = tel
        self.celular = cel

        self.nombre_ap.setText(self.nombre)
        self.ap1_ap.setText(self.apellido_p)
        self.ap2_ap.setText(self.apellido_m)
        self.cel_ap.setText(self.telefono)
        self.tel_ap.setText(self.celular)

        #----------------------BOTONES-----------------------#

        #--------------------------ACCIONES---------------------------#
        self.acept_ap.clicked.connect(self.registrar)
        self.cancelar_ap.clicked.connect(self.cerrar)

    
    def cerrar(self):
            self.nombre_ap.clear()
            self.ap1_ap.clear()
            self.ap2_ap.clear()
            self.cel_ap.clear()
            self.tel_ap.clear()
            self.close()

    def registrar(self):
            self.nombre = self.nombre_ap.text()
            self.ap1 = self.ap1_ap.text()
            self.ap2 = self.ap2_ap.text()
            self.celular = self.cel_ap.text()
            self.telefono = self.tel_ap.text()
        

            if self.nombre =='':
                QMessageBox.warning(self,"Datos faltantes", "Falta ingresar un nombre", QMessageBox.Ok)
            elif self.ap1 == '':
                QMessageBox.warning(self,"Datos faltantes", "Falta ingresar un apellido paterno", QMessageBox.Ok) 
            elif self.ap2 == '':
                QMessageBox.warning(self,"Datos faltantes", "Falta ingresar un apellido materno", QMessageBox.Ok)

            else:
                                
                formulario = modificar_usuario.Modificar(self.id, self.nombre.lower(), self.ap1.lower(), self.ap2.lower(), self.telefono, self.celular )
                formulario.cambiar()
            
                QMessageBox.information(self,"Datos guardados", "Paciente registrado con exito", QMessageBox.Ok)
                self.nombre_ap.clear()
                self.ap1_ap.clear()
                self.ap2_ap.clear()
                self.cel_ap.clear()
                self.tel_ap.clear()
                self.close()

class Modificar_usuarios(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("usuarios.ui",self)

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

        self.pb_modificar.clicked.connect(self.progra)
        self.pb_nuevo.clicked.connect(self.nuevo)
        self.pb_cancelar.clicked.connect(self.cerrar)
        self.pb_borrar.clicked.connect(self.borrar)

        self.busqueda()

    def nuevo(self):
        self.nueva = agregar_usuario()
        self.nueva.show()
        self.close()
    
    def cerrar(self):
        self.close()

    def busqueda(self):
        nueva_busqueda = Descargar_usuarios.Descargar_usuarios()
        datos = nueva_busqueda.obtener_bd()
        self.tabla.clearContents()

        row = 0
        for endian in datos:
            self.tabla.setRowCount(row + 1)
                                    
            self.tabla.setItem(row, 0, QTableWidgetItem(str(endian[1])))
            self.tabla.setItem(row, 1, QTableWidgetItem(endian[2]))
            self.tabla.setItem(row, 2, QTableWidgetItem(str(endian[3])))

            row += 1   
    def progra(self):
        nueva_busqueda = Descargar_usuarios.Descargar_usuarios()
        datos = nueva_busqueda.obtener_bd()
        for row in enumerate (datos):
            if row[0] == self.tabla.currentRow():
                data = row[1]
                id = (str(data[0]))
                user = data[1]
                funcion = data[3] 
                self.configurar = actualizar_usuario(user,funcion,id)
                self.configurar.show()
                self.close()

    def borrar(self):
        nueva_busqueda = Descargar_usuarios.Descargar_usuarios()
        datos = nueva_busqueda.obtener_bd()
        for row in enumerate (datos):
            if row[0] == self.tabla.currentRow():
                data = row[1]
                id = (str(data[0]))
                respuesta = QMessageBox.question(self,"Borrar usuario", "¿ Esta seguro de borrar al usuario ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if respuesta == QMessageBox.Yes:
                    nuevo = Insertar_usuario.Borrar(id)
                    nuevo.borrar()
                    self.busqueda()
                if respuesta == QMessageBox.No : 
                    self.busqueda() 


        #------------------------------------- OPERACIONES PARA EL MEDICO------------------------------------------------#

class agregar_usuario(QDialog):
    def __init__(self):
        QDialog. __init__(self)
        uic.loadUi("agregar_usuario.ui",self)


        self.pb_aceptar.clicked.connect(self.agregar)
        self.pb_cancelar.clicked.connect(self.cancelar)

    def cancelar(self):
        self.close()


    def agregar(self):


            user = self.usuario.text()
            pass1 = self.pass1.text()
            pass2 = self.pass2.text()

            if user == '':
                QMessageBox.warning(self,"Faltan datos", "El campo usuario es obligatorio", QMessageBox.Ok)
            elif pass1 == '':
                QMessageBox.warning(self,"Faltan datos", "El campo contraseña es obligatorio", QMessageBox.Ok)
                
            elif pass2 == '':
                QMessageBox.warning(self,"Faltan datos", "Es necesario repetir la contraseña", QMessageBox.Ok)
                
            
            elif self.Admin.isChecked():
                self.funcion = 'Admin'
            
            elif self.Medico.isChecked():
                self.funcion = 'Medico'
            
            elif self.Asistente.isChecked():
                self.funcion = 'Asistente'
                
            elif pass1 != pass2:
                QMessageBox.warning(self,"Contraseña incorrecta", "Las constraseñas no coinciden", QMessageBox.Ok)
            

            if pass1 == pass2 and pass1 !='' and pass2 != '':
                nuevo = Insertar_usuario.Insertar(str(user),str(pass1),self.funcion)
                if nuevo.insertar():
                    QMessageBox.information(self,"Usuario guardado", "El usuario ha sido registrado con exito", QMessageBox.Ok)
                    self.close()


class actualizar_usuario(QDialog):
    def __init__(self,user,funcion,id):
        QDialog.__init__(self)
        uic.loadUi("agregar_usuario.ui",self)
        self.user = user
        self.funcion = funcion
        self.id = id 

        #---------------------------- Colocando los valores en los line edit ---------------------#

        self.usuario.setText(self.user)

        if self.funcion == 'Admin':
            self.Admin.setChecked(True)
        elif self.funcion == 'Medico':
            self.Medico.setChecked(True)
        elif self.funcion == "Asistente":
            self.Asistente.setChecked(True)


        self.pb_aceptar.clicked.connect(self.agregar)
        self.pb_cancelar.clicked.connect(self.cancelar)

    
    def cancelar(self):
        self.close()

    def agregar(self):


            user = self.usuario.text()
            pass1 = self.pass1.text()
            pass2 = self.pass2.text()

            if user == '':
                QMessageBox.warning(self,"Faltan datos", "El campo usuario es obligatorio", QMessageBox.Ok)
            elif pass1 =='':
                QMessageBox.warning(self,"Faltan datos", "El campo contraseña es obligatorio", QMessageBox.Ok)
                
            elif pass2 == '':
                QMessageBox.warning(self,"Faltan datos", "Es necesario repetir la contraseña", QMessageBox.Ok)
                
            
            elif self.Admin.isChecked():
                self.funcion = 'Admin'
            
            elif self.Medico.isChecked():
                self.funcion = 'Medico'
            
            elif self.Asistente.isChecked():
                self.funcion = 'Asistente'

            elif pass1 != pass2:
                QMessageBox.warning(self,"Contraseña incorrecta", "Las constraseñas no coinciden", QMessageBox.Ok)


            if pass1 == pass2 and pass1 !='' and pass2 != '':
                nuevo = Insertar_usuario.Actualizar(str(user),str(pass1),self.funcion,int(self.id))
                if nuevo.actualizar():
                    QMessageBox.information(self,"Usuario Actualizado", "El usuario ha sido actualizado con exito", QMessageBox.Ok)
                    self.close()


class Principal_Medico(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("medico.ui",self)
        #RELACINAR LAS CLASES CON LOS METODOS
        self.agregar = Buscar_Pacientes_Consulta()
        self.abrirAgenda = Abrir_Agenda()
        self.buscarpx = Buscar_px()
        self.formulario = Paciente_consulta()
        self.historial = Busqueda_historial()
        self.configuracion = Configuracion()
    

        #AGREGAR ACCIONES A LOS BOTONES DEL MENU
        self.Btn_iniciar_consulta_m.clicked.connect(self.agregar_cita)
        self.Btn_Agenda_m.clicked.connect(self.abrir_agenda)
        self.Btn_buscarpaciente_m.clicked.connect(self.buscarPx)
        self.Btn_nuevopaciente_m.clicked.connect(self.nuevo_formulario)
        self.btn_historialclinico_m.clicked.connect(self.historial_Clinico)
        self.btn_config_m.clicked.connect(self.config)


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

    def config(self):
        self.configuracion.show()


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
        self.agregar = Nueva_Cita('','','','','','')
        self.abrirAgenda = Abrir_Agenda()
        self.buscarpx = Buscar_px()
        self.formulario = Nuevo_Formulario()
        self.historial = Busqueda_historial()

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
        self.agregar = Nueva_Cita('','','','','','')
        self.abrirAgenda = Abrir_Agenda()
        self.buscarpx = Buscar_px()
        self.formulario = Nuevo_Formulario()
        self.historial = Busqueda_historial()

        #-----------------Funciones de los botones--------------------#

        self.pb_agregarcita_adm.clicked.connect(self.agregar_cita)
        self.pb_agenda_adm.clicked.connect(self.abrir_agenda)
        self.pb_buscarPx_adm.clicked.connect(self.buscarPx)
        self.pb_nuevoPx_adm.clicked.connect(self.nuevo_formulario)
        self.pb_historial_adm.clicked.connect(self.historial_Clinico)
        

    #--------------------------DECLARAR METODOS PARA ABRIR LAS OPCIONES DEL MENU
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
    #---------------------------------------SUB PROGRAMA PARA AGREGAR PACIENTES PARA CONSULTA-----------------

class Paciente_consulta(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("agregar_px.ui",self)

        #----------------------BOTONES-----------------------#

        #--------------------------ACCIONES---------------------------#
        self.acept_ap.clicked.connect(self.registrar)
        self.cancelar_ap.clicked.connect(self.cerrar)

    
    def cerrar(self):
            self.nombre_ap.clear()
            self.ap1_ap.clear()
            self.ap2_ap.clear()
            self.cel_ap.clear()
            self.tel_ap.clear()
            self.close()


    def registrar(self):
            self.nombre = self.nombre_ap.text()
            self.ap1 = self.ap1_ap.text()
            self.ap2 = self.ap2_ap.text()
            self.celular = self.cel_ap.text()
            self.telefono = self.tel_ap.text()
        

            if self.nombre =='':
                QMessageBox.warning(self,"Datos faltantes", "Falta ingresar un nombre", QMessageBox.Ok)
            elif self.ap1 == '':
                QMessageBox.warning(self,"Datos faltantes", "Falta ingresar un apellido paterno", QMessageBox.Ok) 
            elif self.ap2 == '':
                QMessageBox.warning(self,"Datos faltantes", "Falta ingresar un apellido materno", QMessageBox.Ok)

            else:
                                
                formulario = Formulario.Nuevo_Paciente(self.nombre.lower(), self.ap1.lower(), self.ap2.lower(), self.celular, self.telefono )
                formulario.registrar_nuevo()
            
                QMessageBox.information(self,"Datos guardados", "Paciente registrado con exito", QMessageBox.Ok)
                self.nombre_ap.clear()
                self.ap1_ap.clear()
                self.ap2_ap.clear()
                self.cel_ap.clear()
                self.tel_ap.clear()
                self.close()

            
    #-------------------------------------PROGRAMA PARA BUSCAR PACIENTES E INICIAR CONSULTA----------------------------#
class Buscar_Pacientes_Consulta(QDialog):
    def __init__(self):
        QDialog. __init__(self)
        uic.loadUi("buscar_px.ui",self)
        #------------------- Agregar nuevo paciente
        self.nueva = Paciente_consulta()
        #----------------------
        self.pb_agregar_nuevo_B.setText("Iniciar consulta")
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
        self.pb_nuevopx.clicked.connect(self.nuevo)
        self.bt_cancel.clicked.connect(self.cerrar)

    def cerrar(self):
        self.lineEdit_busqueda.clear()
        self.busqueda()
        self.close()

    def nuevo(self):
        self.nueva.show()

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
                self.agregar = Nuevo_Formulario_Px_Registrado(id,nombres,apellido1,apellido2)
                self.agregar.show()
                

    #-------------------------------------MODULO PARA INICIAR CONSULTA DE UN PACIENTE REGISTRADO---------------------#

class Nuevo_Formulario_Px_Registrado(QMainWindow):
    def __init__(self,id,nom,ap1,ap2):
        QMainWindow. __init__(self)
        uic.loadUi("formulario_con_datos.ui",self)
        self.id = id
        self.nombre =  nom
        self.ap1 = ap1
        self.ap2 = ap2
 
        #-------------------------- ASIGNAMOS EL VALOR QUE VIENE DEL METODO A LOS LINE EDIT PARA RELLENAR LOS DATOS
        self.lineEdit_nombres_F.setText(self.nombre)
        self.lineEdit_ape_pat_F.setText(self.ap1)
        self.lineEdit_ape_mat_F.setText(self.ap2)
        self.lineEdit_id_F.setText(self.id)


        #----------------------------------BOTONES-----------------------------
        self.pb_actualizar.clicked.connect(self.registrar_nuevo)
        self.pb_cancelar.clicked.connect(self.cerrar)


    def registrar_nuevo(self):
            id = self.id
            peso = self.lineEdit_peso.text()
            altura = self.lineEdit_altura.text()
            dx = self.plainTextEdit_Dx.toPlainText()
            estudios = self.plainTextEdit_Estudios.toPlainText()
            trat = self.plainTextEdit_Med.toPlainText()
            
            if dx == "":
                QMessageBox.warning(self,"Datos faltantes", "Falta ingresar el diagnostico", QMessageBox.Ok)
            elif trat =="":
                QMessageBox.warning(self,"Datos faltantes", "Falta ingresar el tratamiento", QMessageBox.Ok)
            else:

                formulario = Update.Actualizar_diagnostico(id,peso,altura,dx,estudios,trat)
                formulario.Actualizar()
                formulario.historial()
                
            
                QMessageBox.information(self,"Datos guardados", "Datos del paciente guardados con exito", QMessageBox.Ok)
                self.lineEdit_nombres_F.clear()
                self.lineEdit_ape_pat_F.clear()
                self.lineEdit_ape_mat_F.clear()
                self.lineEdit_id_F.clear()
                self.lineEdit_peso.clear()
                self.lineEdit_altura.clear()
                self.plainTextEdit_Dx.clear()
                self.plainTextEdit_Estudios.clear()
                self.plainTextEdit_Med.clear()
                self.close()

    def cerrar(self):
        self.close()

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
