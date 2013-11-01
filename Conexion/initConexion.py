#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Conexion.conexion import Conexion
from Conexion.conexionProducto import conexionProducto
from Conexion.conexionProveedor import conexionProveedor
from Conexion.conexionCliente import conexionCliente
from Conexion.conexionUsuario import conexionUsuario
from Conexion.conexionMarca import conexionMarca
from Conexion.conexionRubro import conexionRubro
class ControllerConnection(object):

    def __init__(self):
        self.connection = Conexion()
        self.connectionCliente = conexionCliente(self.connection)

    def getConnectionRubro(self):
        self.__connectionRubro = conexionRubro(self.connection)
        return self.__connenctionRubro

    def getConnectionMarca(self):
        self.__connectioMarca = conexionMarca(self.__connection)
        return  self.__connectioMarca

    def getConnectionUsuario(self):
        self.__connectionUsuario = conexionUsuario(self.__connection)
        return self.__connectionUsuario

    def getConnectionCliente(self):
        return self.connectionCliente

    def getConnectionProveedor(self):
        self.__connectionProveedor = conexionProveedor(self.__connection)
        return self.__connectionProveedor

    def getConnectionProducto(self):
        self.__connectionProducto = conexionProducto(self.__connection)
        return self.__connectionProducto

