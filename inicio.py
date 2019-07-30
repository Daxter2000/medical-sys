# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inicio.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Iniciar_Sesion(object):
    def setupUi(self, Iniciar_Sesion):
        Iniciar_Sesion.setObjectName("Iniciar_Sesion")
        Iniciar_Sesion.resize(400, 300)
        Iniciar_Sesion.setStyleSheet("")
        self.lineEdit_user = QtWidgets.QLineEdit(Iniciar_Sesion)
        self.lineEdit_user.setGeometry(QtCore.QRect(160, 110, 171, 21))
        self.lineEdit_user.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_user.setObjectName("lineEdit_user")
        self.lineEdit_pass = QtWidgets.QLineEdit(Iniciar_Sesion)
        self.lineEdit_pass.setGeometry(QtCore.QRect(160, 160, 171, 21))
        self.lineEdit_pass.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_pass.setObjectName("lineEdit_pass")
        self.Label_usuario = QtWidgets.QLabel(Iniciar_Sesion)
        self.Label_usuario.setGeometry(QtCore.QRect(90, 110, 51, 16))
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Label_usuario.setFont(font)
        self.Label_usuario.setStyleSheet("")
        self.Label_usuario.setObjectName("Label_usuario")
        self.label_pass = QtWidgets.QLabel(Iniciar_Sesion)
        self.label_pass.setGeometry(QtCore.QRect(70, 160, 71, 20))
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_pass.setFont(font)
        self.label_pass.setStyleSheet("")
        self.label_pass.setObjectName("label_pass")
        self.btn_aceptar_inicio = QtWidgets.QPushButton(Iniciar_Sesion)
        self.btn_aceptar_inicio.setGeometry(QtCore.QRect(180, 240, 75, 23))
        self.btn_aceptar_inicio.setStyleSheet("")
        self.btn_aceptar_inicio.setObjectName("btn_aceptar_inicio")
        self.btn_salir_inicio = QtWidgets.QPushButton(Iniciar_Sesion)
        self.btn_salir_inicio.setGeometry(QtCore.QRect(290, 240, 75, 23))
        self.btn_salir_inicio.setStyleSheet("")
        self.btn_salir_inicio.setObjectName("btn_salir_inicio")
        self.label = QtWidgets.QLabel(Iniciar_Sesion)
        self.label.setGeometry(QtCore.QRect(70, 20, 281, 61))
        font = QtGui.QFont()
        font.setFamily("Sitka Text")
        font.setPointSize(26)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(Iniciar_Sesion)
        QtCore.QMetaObject.connectSlotsByName(Iniciar_Sesion)

    def retranslateUi(self, Iniciar_Sesion):
        _translate = QtCore.QCoreApplication.translate
        Iniciar_Sesion.setWindowTitle(_translate("Iniciar_Sesion", "Dialog"))
        self.Label_usuario.setText(_translate("Iniciar_Sesion", "Usuario"))
        self.label_pass.setText(_translate("Iniciar_Sesion", "Contraseña"))
        self.btn_aceptar_inicio.setText(_translate("Iniciar_Sesion", "Aceptar"))
        self.btn_salir_inicio.setText(_translate("Iniciar_Sesion", "Salir"))
        self.label.setText(_translate("Iniciar_Sesion", "INICIAR SESION"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Iniciar_Sesion = QtWidgets.QDialog()
    ui = Ui_Iniciar_Sesion()
    ui.setupUi(Iniciar_Sesion)
    Iniciar_Sesion.show()
    sys.exit(app.exec_())
