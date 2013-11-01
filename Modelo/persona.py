#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Modelo.direccion import Direccion
class Persona(object):

    def __init__(self):
        self.__idPersona = 0
        self.__nombre = ""
        self.__email= ""
        self.__direccion = Direccion()

    def setIdPersona(self, idPersona):
        self.__idPersona = idPersona

    def getIdPersona(self):
        return self.__idPersona

    def setNombre(self, nombre):
        self.__nombre = nombre

    def getNombre(self):
        return self.__nombre

    def setEmail(self, email):
        self.__email = email

    def getEmail(self):
        return self.__email

    def setDireccion(self, direccion):
        self.__direccion = direccion

    def getDireccion(self):
        return self.__direccion