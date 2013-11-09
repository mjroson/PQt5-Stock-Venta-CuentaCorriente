#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import uic
from Controlador.pCliente import PestaniaCliente
from Controlador.pProveedor import PestaniaProveedor
from Controlador.pUsuario import PestaniaUsuario
from Controlador.pProducto import PestaniaProducto
from Controlador.pTransacciones import PestaniaTransacciones
from Controlador.pPagos import PestaniaPagos
from Conexion.conexionGeneral import ConexionGenerales
from Controlador.windowNotification import WindowNotification

class Principal():

    def __init__(self, usuario):

        #Definiendo variables
        self.usuario = usuario
        self.winPrincipal = uic.loadUi('../Vista/mainwindow.ui')
        self.winPrincipal.show()

        self.setInterfaceUsuario()
        #self.winPrincipal.maximumSize = self.winPrincipal.size()
        self.winPrincipal.setFixedSize(self.winPrincipal.size())
        self.notificationStock()
        self.winPrincipal.twMenu.currentChanged.connect(self.changePes)

        self.pestaniaTransaccion = PestaniaTransacciones(self.winPrincipal)
        self.pestaniaPago = PestaniaPagos(self.winPrincipal)
        self.pestaniaCliente = PestaniaCliente(self.winPrincipal)
        self.pestaniaUsuario = PestaniaUsuario(self.winPrincipal)
        self.pestaniaProveedor = PestaniaProveedor(self.winPrincipal)
        self.pestaniaProducto = PestaniaProducto(self.winPrincipal)


    def setInterfaceUsuario(self):

        if self.usuario.getTipoUsuario() == 'ADM':
            self.winPrincipal.twMenu.setTabEnabled(5, True)
            self.winPrincipal.twMenu.setTabEnabled(6, True)
        else:
            self.winPrincipal.twMenu.setTabEnabled(5, False)
            self.winPrincipal.twMenu.setTabEnabled(6, False)


    def notificationStock(self):
        conexionGenerales = ConexionGenerales()

        listProdSinStock = conexionGenerales.selectProductoStock()
        self.winPrincipal.btnNotification.setEnabled(False)
        if len(listProdSinStock) > 0:
            self.winPrincipal.btnNotification.setText(str(len(listProdSinStock)))
            self.winPrincipal.btnNotification.setStyleSheet("background-color: rgb(255, 229, 230);")
            self.winPrincipal.btnNotification.clicked.connect(self.openNotification)
            if self.usuario.getTipoUsuario() == 'ADM':
                self.winPrincipal.btnNotification.setEnabled(True)
        else:
            self.winPrincipal.btnNotification.setText("0")
            self.winPrincipal.btnNotification.setStyleSheet("background-color: rgb(255, 255, 255);")


    def openNotification(self):
        self.winNot = WindowNotification()

    def changePes(self):
        #self.winPrincipal.disconnect()
        if self.winPrincipal.twMenu.currentIndex() == 0:
            #self.pestania.finish() transacciones
            self.pestaniaProducto.limpiarCampos()
        elif self.winPrincipal.twMenu.currentIndex() == 1:
            #self.pestania.finish() pagos
            self.pestaniaPago.limpiarCampos()
        elif self.winPrincipal.twMenu.currentIndex() == 2:
            #self.pestania.finish() producto
            self.pestaniaProducto.limpiarCampos()
        elif self.winPrincipal.twMenu.currentIndex() == 3:
            #self.pestania.finish() cliente
            self.pestaniaCliente.limpiarCampos()
        elif self.winPrincipal.twMenu.currentIndex() == 4:
            #self.pestania.finish() proveedor
            self.pestaniaProveedor.limpiarCampos()
        elif self.winPrincipal.twMenu.currentIndex() == 5:
            #self.pestania.finish() usuario
            self.pestaniaUsuario.limpiarCampos()
        elif self.winPrincipal.twMenu.currentIndex() == 6:
            #self.pestania.finish()
            print('Estaditicas')
