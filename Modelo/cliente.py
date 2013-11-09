#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Modelo.persona import Persona
class Cliente(Persona):

    def __init__(self):
        Persona.__init__(self)
        self.__apellido = ""
        self.__idCliente = 0
        self.__estado = 0

    def setApellido(self, apellido):
        self.__apellido = apellido

    def getApellido(self):
        return self.__apellido

    def setIdCliente(self, idCliente):
        self.__idCliente = idCliente

    def getIdCliente(self):
        return self.__idCliente

    def setEstado(self, estado):
        self.__estado = estado

    def getEstado(self):
        return self.__estado