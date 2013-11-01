__author__ = 'Vicio'
from Modelo.persona import Persona

class Telefono(object):

    def __init__(self):
        self.__idTelefono = 0
        self.__tipo = ""
        self.__telefono = 0
        self.__idPersona = 0

    def setIdTelefono(self, idTelefono):
        self.__idTelefono = idTelefono

    def getIdTelefono(self):
        return self.__idTelefono

    def setTipo(self, tipo):
        self.__tipo = tipo

    def getTipo(self):
        return self.__tipo

    def setTelefono(self, telefono):
        self.__telefono =telefono

    def getTelefono(self):
        return self.__telefono

    def setIdPersona(self, idPersona):
        self.__idPersona = idPersona

    def getIdPersona(self):
        return self.__idPersona