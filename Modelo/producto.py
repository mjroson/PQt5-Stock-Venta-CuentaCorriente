#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Modelo.proveedor import Proveedor
from Modelo.marca import Marca
from Modelo.rubro import Rubro
class Producto(object):
    def __init__(self):

        self.__idProducto = 0
        self.__nombre = ""
        self.__cantidad = 0
        self.__cantidadMinima = 0
        self.__descripcion = ""
        self.__genero = ""
        self.__rubro = Rubro()
        self.__proveedor = Proveedor()
        self.__marca = Marca()
        self.__estado = 0
        self.__pCompra = 0,00
        self.__pVenta = 0,00

    def setIdProducto(self, idProducto):
        self.__idProducto = idProducto

    def getIdProducto(self):
        return self.__idProducto

    def setNombre(self, nombre):
        self.__nombre = nombre

    def getNombre(self):
        return self.__nombre

    def setCantidad(self, cantidad):
        self.__cantidad = cantidad

    def getCantidad(self):
        return self.__cantidad

    def setCantidadMinima(self, cantMinima):
        self.__cantidadMinima = cantMinima

    def getCantidadMinima(self):
        return self.__cantidadMinima

    def setDescripcion(self, descripcion):
        self.__descripcion = descripcion

    def getDescripcion(self):
        return self.__descripcion

    def setGenero(self, genero):
        self.__genero = genero

    def getGenero(self):
        return self.__genero

    def setRubro(self, rubro):
        self.__rubro = rubro

    def getRubro(self):
        return self.__rubro

    def setProveedor(self, proveedor):
        self.__proveedor = proveedor

    def getProveedor(self):
        return self.__proveedor

    def setMarca(self, marca):
        self.__marca = marca

    def getMarca(self):
        return self.__marca

    def setEstado(self, estado):
        self.__estado = estado

    def getEstado(self):
        return self.__estado

    def setPrecioCompra(self, pCompra):
        self.__pCompra = pCompra

    def getPrecioCompra(self):
        return self.__pCompra

    def setPrecioVenta(self, pVenta):
        self.__pVenta = pVenta

    def getPrecioVenta(self):
        return self.__pVenta