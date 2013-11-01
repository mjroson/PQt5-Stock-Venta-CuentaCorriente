#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QApplication

from Controlador.windowPrincipal import Principal
from Controlador.windowIniciar import WindowIniciar
from PyQt5.QtWidgets import QMessageBox, QDialog
from Conexion.conexionGeneral import ConexionGenerales
from Controlador.windowNotification import WindowNotification



class windowMain():

    def __init__(self):
        #self.Principal = Principal()

        self.iniciar = WindowIniciar()
        self.iniciar.winIniciar.btnIniciar.clicked.connect(self.comprobarUsuario)



    def comprobarUsuario(self):
        usuario = self.iniciar.onClickValidarUsuario()
        if usuario != None:
            self.principal = Principal(usuario=usuario)
            self.iniciar.winIniciar.close()
            self.principal.winPrincipal.lblNombreUsuario.setText(usuario.getUsuario())
            self.principal.winPrincipal.actionCerrarSesion.triggered.connect(self.cerrarSesion)
            self.principal.winPrincipal.actionSalir.triggered.connect(self.salir)

            self.notificationStock()


    def cerrarSesion(self):
        alert = QDialog()
        confirm  = QMessageBox.question(alert, "Mensaje", "¿ Desea cerrar sesion ?", QMessageBox.Yes,
             QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.iniciar.winIniciar.show()
            self.principal.winPrincipal.close()


    def salir(self):
        alert = QDialog()
        confirm = QMessageBox.question(alert, "Mensaje", "¿ Desea salir ?", QMessageBox.Yes, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.principal.winPrincipal.close()


    def notificationStock(self):
        conexionGenerales = ConexionGenerales()

        listProdSinStock = conexionGenerales.selectProductoStock()

        if len(listProdSinStock) > 0:
            self.principal.winPrincipal.btnNotification.setText(str(len(listProdSinStock)))
            self.principal.winPrincipal.btnNotification.setStyleSheet("background-color: rgb(175, 231, 196);\n"
                    "font: 75 9pt \"MS Shell Dlg 2\";\n"
                    "color: rgb(255, 197, 174);")
            self.principal.winPrincipal.btnNotification.clicked.connect(self.openNotification)
        else:
            self.principal.winPrincipal.btnNotification.setText("0")
            self.principal.winPrincipal.btnNotification.setStyleSheet("background-color: rgb(255, 0, 0);\n"
                    "font: 75 9pt \"MS Shell Dlg 2\";\n"
                    "color: rgb(255, 197, 174);")




    def openNotification(self):
        self.winNot = WindowNotification()






app = QApplication(sys.argv)
windowMain = windowMain()
sys.exit(app.exec_())