#!/usr/bin/env python
# -*- coding: utf-8 -*-



from PyQt5 import uic
from Conexion.conexionUsuario import conexionUsuario
from Modelo.usuario import Usuario
from PyQt5.QtWidgets import QMessageBox, QDialog


class WindowIniciar():

    def __init__(self):

        self.winIniciar = uic.loadUi('../Vista/iniciar.ui')
        self.conexionUsuario = conexionUsuario()
        #self.winIniciar.btnIniciar.clicked.connect(self.onClickValidarUsuario)
        self.winIniciar.btnSalir.clicked.connect(self.onClickSalir)
        self.usuario = Usuario()
        self.winIniciar.txtUsuario.setFocus(True)
        self.winIniciar.show()


    def onClickValidarUsuario(self):

        self.usuario = Usuario()
        self.usuario.setUsuario(self.winIniciar.txtUsuario.text())
        self.usuario.setPasswd(self.winIniciar.txtPass.text())
        value = ''
        if self.usuario.getUsuario() != '' and self.usuario.getPasswd() != '':
            value  = self.conexionUsuario.validarUsuario(usuario=self.usuario)
            if len(value) != 0:
                self.usuario.setUsuario(value[0][0])
                self.usuario.setTipoUsuario(value[0][1])
                self.winIniciar.txtPass.setText('')
                self.winIniciar.txtUsuario.setText('')
                return self.usuario
            else:
                self.winIniciar.lblError.setText('LA CONTRASEÑA O USUARIO NO COINCIDEN')
                self.winIniciar.txtPass.setText('')
                alert = QDialog()
                QMessageBox.information(alert,"ERROR", 'LA CONTRASEÑA O USUARIO NO COINCIDEN')
        else:
            print('Falta completar algun campo')
            alert = QDialog()
            QMessageBox.information(alert,"ERROR", 'Falta completar algun campo')



    def onClickSalir(self):
        alert = QDialog()
        confirm  = QMessageBox.question(alert, "Mensaje", "¿ Desea salir ?", QMessageBox.Yes,
             QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.winIniciar.close()


