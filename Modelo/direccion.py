#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Direccion():
    def __init__(self):
        self.__idDireccion = 0
        self.__direccion = ""
        self.__numero = 0
        self.__piso = 0
        self.__dpto = ""

    def setIdDireccion(self, idDireccion):
        self.__idDireccion = idDireccion

    def getIdDireccion(self):
        return self.__idDireccion

    def setDireccion(self, direccion):
        self.__direccion = direccion

    def getDireccion(self):
        return self.__direccion

    def setNumero(self, numero):
        self.__numero = numero

    def getNumero(self):
        if self.__numero != 0:
            return self.__numero
        else:
            return None

    def setPiso(self, piso):
        self.__piso = piso

    def getPiso(self):
        if self.__piso != 0:
            return self.__piso
        else:
            return None

    def setDpto(self, dpto):
        self.__dpto = dpto

    def getDpto(self):
        if self.__dpto != "":
            return self.__dpto
        else:
            return None