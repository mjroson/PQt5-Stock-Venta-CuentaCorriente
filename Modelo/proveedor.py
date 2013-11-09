#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Modelo.persona import Persona
class Proveedor(Persona):
    '''
    classdocs
    '''


    def __init__(self):
        Persona.__init__(self)
        self.__idProveedor = 0
        self.__descripcion = ""
        self.__web = ""
        self.__estado = 0

    def setIdProveedor(self, idPProveedor):
        self.__idProveedor = idPProveedor

    def getIdProveedor(self):
        return self.__idProveedor

    def setDescripcion(self, descripcion):
        self.__descripcion = descripcion

    def getDescripcion(self):
        return self.__descripcion

    def setWeb(self, web):
        self.__web = web

    def getWeb(self):
        return self.__web

    def setEstado(self, estado):
        self.__estado = estado

    def getEstado(self):
        return self.__estado
