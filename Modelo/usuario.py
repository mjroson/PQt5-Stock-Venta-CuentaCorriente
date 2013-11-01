#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Modelo.persona import Persona
import hashlib

class Usuario(Persona):

    def __init__(self):
        Persona.__init__(self)
        self.__idUsuario = 0
        self.__apellido = ""
        self.__usuario = ""
        self.__passwd = ""
        self.__tipoUsuario = ""

    def setApellido(self, apellido):
        self.__apellido = apellido

    def getApellido(self):
        return self.__apellido

    def setUsuario(self, usuario):
        self.__usuario = usuario

    def getUsuario(self):
        return self.__usuario

    def setPasswd(self, passwd):
        #auxPasswd = hashlib.md5(passwd).hexdigest()
        self.__passwd = passwd

    def getPasswd(self):
        return self.__passwd

    def setTipoUsuario(self, tipoUsuario):
        self.__tipoUsuario = tipoUsuario


    def getTipoUsuario(self):
        return self.__tipoUsuario

    def setIdUsuario(self, idUsuario):
        self.__idUsuario = idUsuario

    def getIdUsuario(self):
        return self.__idUsuario