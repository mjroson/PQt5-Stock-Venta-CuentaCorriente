#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import uic
from Controlador.pCliente import PestaniaCliente
from Controlador.pProveedor import PestaniaProveedor
from Controlador.pUsuario import PestaniaUsuario
from Controlador.pProducto import PestaniaProducto
from Controlador.pTransacciones import PestaniaTransacciones
from Controlador.pPagos import PestaniaPagos

class Principal():

    def __init__(self, usuario):

        #Definiendo variables
        self.usuario = usuario
        self.winPrincipal = uic.loadUi('../Vista/mainwindow.ui')
        self.winPrincipal.show()

        self.setInterfaceUsuario()


    def setInterfaceUsuario(self):
        self.pesCliente = PestaniaCliente(self.winPrincipal)
        self.pesProveedor = PestaniaProveedor(self.winPrincipal)
        self.pesProducto = PestaniaProducto(self.winPrincipal)
        self.pesTransaccion = PestaniaTransacciones(self.winPrincipal)
        self.pesPagos = PestaniaPagos(self.winPrincipal)
        if self.usuario.getTipoUsuario() == 'ADM':
            self.winPrincipal.twMenu.setTabEnabled(5, True)
            self.winPrincipal.twMenu.setTabEnabled(6, True)
            self.pesUsuario = PestaniaUsuario(self.winPrincipal)

        else:
            self.winPrincipal.twMenu.setTabEnabled(5, False)
            self.winPrincipal.twMenu.setTabEnabled(6, False)


       