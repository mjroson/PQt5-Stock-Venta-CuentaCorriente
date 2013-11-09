#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Conexion.conexion import Conexion
from Modelo.rubro import Rubro

class conexionRubro(object):

    def __init__(self):
        self.conexion = Conexion()
        self.__rubro = Rubro()

    def selectRubro(self, filterText):
        query = "SELECT idrubros, descripcion FROM rubros WHERE descripcion LIKE %s"
        parametro = filterText + '%'
        value = parametro
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, value)
        listRubro = self.conexion.cursor.fetchall()

        return listRubro
        self.conexion.cerrarConexion()


    def borrarRubro(self, rubro):
        query = "DELETE FROM rubros WHERE idrubros = %s"
        values = rubro.getIdRubro()
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        self.conexion.db.commit()
        self.conexion.cerrarConexion()


    def modificarRubro(self, rubro):
        query = "UPDATE rubros SET descripcion = %s WHERE idrubros = %s"
        values = (rubro.getRubro(), rubro.getIdRubro())
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        self.conexion.db.commit()
        self.conexion.cerrarConexion()


    def insertarRubro(self, rubro):
        query = "INSERT INTO rubros (descripcion) VALUES (%s)"
        values = rubro.getRubro()
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        self.conexion.db.commit()
        self.conexion.cerrarConexion()