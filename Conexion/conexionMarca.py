#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Conexion.conexion import Conexion
from Modelo.marca import Marca

class conexionMarca(object):


    def __init__(self):
        self.conexion = Conexion()
        self.__marca = Marca()
        
        
    def selectMarca(self, textFilter):
        query = "SELECT idmarcas, descripcion FROM marcas WHERE descripcion LIKE %s"
        parametro = textFilter + '%'
        value = parametro
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, parametro)
        listMarca = self.conexion.cursor.fetchall()

        return listMarca
        self.conexion.cerrarConexion()

    
    def borrarMarca(self, marca):
        query = "DELETE FROM marcas WHERE idmarcas= %s "
        values = marca.getIdMarca()
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        self.conexion.db.commit()
        self.conexion.cerrarConexion()

    def modificarMarca(self, marca):
        query = "UPDATE marcas SET descripcion= %s WHERE idmarcas= %s"
        values = (marca.getMarca(),marca.getIdMarca())
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        self.conexion.db.commit()
        self.conexion.cerrarConexion()
        
    def insertMarca(self, marca):
        query = "INSERT INTO marcas (descripcion) VALUES (%s)"
        values = marca.getMarca()
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        self.conexion.db.commit()
        self.conexion.cerrar_conexion()