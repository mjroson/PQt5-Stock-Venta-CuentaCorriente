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
from Controlador.pEstadisticas import PestaniaEstadisticas
from Controlador.windowNotification import WindowNotification
from Controlador.windowList import WindowList
from PyQt5.Qt import QDesktopServices, QUrl

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
        self.pestaniaEstadisticas = PestaniaEstadisticas(self.winPrincipal)

        self.winPrincipal.actionListCliente.triggered.connect(self.openListCliente)
        self.winPrincipal.actionListProveedor.triggered.connect(self.openListProveedor)
        self.winPrincipal.actionListStock.triggered.connect(self.openNotification)

        self.winPrincipal.actionTransacciones.triggered.connect(self.actionTransacciones)
        self.winPrincipal.actionPagos.triggered.connect(self.actionPagos)
        self.winPrincipal.actionProductos.triggered.connect(self.actionProductos)
        self.winPrincipal.actionClientes.triggered.connect(self.actionClientes)
        self.winPrincipal.actionProveedores.triggered.connect(self.actionProveedores)
        self.winPrincipal.actionUsuarios.triggered.connect(self.actionUsuarios)
        self.winPrincipal.actionEstaditicas.triggered.connect(self.actionEstadisticas)
        self.winPrincipal.actionManual.triggered.connect(self.openManual)
        self.winPrincipal.actionReportarError.triggered.connect(self.openMail)

        #self.winPrincipal.btnListProveedores_e.clicked.connect(self.openListProveedor)
        #self.winPrincipal.btnListClientes_e.clicked.connect(self.openListCliente)
        #self.winPrincipal.btnListProductos_e.clicked.connect(self.openNotification)

        if usuario.getTipoUsuario() == 'USR':
            self.winPrincipal.actionListCliente.setEnabled(False)
            self.winPrincipal.actionListProveedor.setEnabled(False)
            self.winPrincipal.actionListStock.setEnabled(False)

            self.winPrincipal.actionUsuarios.setEnabled(False)
            self.winPrincipal.actionEstaditicas.setEnabled(False)

    def openListCliente(self):
        self.winList = WindowList(type='CLIENT')

    def openListProveedor(self):
        self.winList = WindowList(type='PROV')

    def openManual(self):
        url = QUrl
        url = QUrl("../Recursos/Manual.pdf")
        QDesktopServices.openUrl(url)


    def openMail(self):
        QDesktopServices.openUrl(QUrl("mailto:duftuban@mail.com?subject=Error&body=REPORTAR ERROR :"))


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
            self.winPrincipal.btnNotification.setStyleSheet("border-top: 3px transparent;\nborder-bottom: 3px transparent;\nborder-right: 5px transparent;\nborder-left: 5px transparent;\ncolor: rgb(255, 0, 0);\nfont: 87 8pt Rockwell Extra Bold;")
            self.winPrincipal.btnNotification.clicked.connect(self.openNotification)
            if self.usuario.getTipoUsuario() == 'ADM':
                self.winPrincipal.btnNotification.setEnabled(True)
        else:
            self.winPrincipal.btnNotification.setText("0")
            self.winPrincipal.btnNotification.setStyleSheet("background-color: rgb(185, 185, 185);")


    def openNotification(self):
        self.winNot = WindowNotification()

    def changePes(self):
        #self.winPrincipal.disconnect()
        if self.winPrincipal.twMenu.currentIndex() == 0:
            #self.pestania.finish() transacciones
            self.pestaniaTransaccion.limpiarCampos()
        elif self.winPrincipal.twMenu.currentIndex() == 1:
            #self.pestania.finish() pagos
            self.pestaniaPago.limpiarCampos()
        elif self.winPrincipal.twMenu.currentIndex() == 2:
            #self.pestania.finish() producto
            self.pestaniaProducto.validarBotones('BORRAR')
        elif self.winPrincipal.twMenu.currentIndex() == 3:
            #self.pestania.finish() cliente
            self.pestaniaCliente.validarBotones('BORRAR')
        elif self.winPrincipal.twMenu.currentIndex() == 4:
            #self.pestania.finish() proveedor
            self.pestaniaProveedor.validarBotones('BORRAR')
        elif self.winPrincipal.twMenu.currentIndex() == 5:
            #self.pestania.finish() usuario
            self.pestaniaUsuario.validarBotones('BORRAR')
        elif self.winPrincipal.twMenu.currentIndex() == 6:
            #self.pestania.finish()
            print('Estaditicas')

    def actionTransacciones(self):
        self.winPrincipal.twMenu.setCurrentIndex(0)

    def actionPagos(self):
        self.winPrincipal.twMenu.setCurrentIndex(1)

    def actionProductos(self):
        self.winPrincipal.twMenu.setCurrentIndex(2)

    def actionClientes(self):
        self.winPrincipal.twMenu.setCurrentIndex(3)

    def actionProveedores(self):
        self.winPrincipal.twMenu.setCurrentIndex(4)

    def actionUsuarios(self):
        self.winPrincipal.twMenu.setCurrentIndex(5)

    def actionEstadisticas(self):
        self.winPrincipal.twMenu.setCurrentIndex(6)
