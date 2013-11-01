#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Modelo.proveedor import Proveedor
from Conexion.conexion import Conexion
class conexionProveedor(object):


    def __init__(self):
        self.conexion = Conexion()
        self.proveedor = Proveedor()

    def selectProveedor(self):
        query ="""SELECT prov.idproveedores, prov.descripcion, p.nombre, p.email, prov.web, d.direccion, d.numero,
                        d.piso, d.dpto, p.idpersonas, d.iddirecciones
                    FROM proveedores prov, personas p, direcciones d
                    WHERE p.direcciones_iddirecciones = d.iddirecciones and p.idpersonas = prov.personas_idpersonas"""
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query)
        listProveedor = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listProveedor

    def selectTelefonoProveedor(self, proveedor):
        query = """SELECT t.idtelefono, t.numero, t.tipo
                    FROM telefonos t, personas p, proveedores prov
                    WHERE p.idpersonas = prov.personas_idpersonas and p.idpersonas = t.personas_idpersonas
                    and prov.idproveedores = %s"""
        value = proveedor.getIdProveedor()
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query)
        listTelefono = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listTelefono

    def modificarProveedor(self, proveedor):
        query = """
                    UPDATE personas p, proveedores prov, direcciones d
                    SET p.nombre = %s , p.email= %s , prov.descripcion = %s, prov.web = %s, d.direccion= %s,
                            d.numero = %s, d.piso = %s, d.dpto = %s
                    WHERE p.idpersonas = prov.personas_idpersonas and p.direcciones_iddirecciones = d.iddirecciones
                            and prov.idproveedores = %s
                """
        values = (proveedor.getNombre(), proveedor.getEmail(), proveedor.getDescripcion(),
                    proveedor.getWeb(), proveedor.getDireccion().getDireccion(), proveedor.getDireccion().getNumero(),
                    proveedor.getDireccion().getPiso(), proveedor.getDireccion().getDpto(),proveedor.getIdProveedor())
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        self.conexion.db.commit()
        self.conexion.cerrarConexion()

    def insertarProveedor(self, proveedor):
        self.conexion.abrirConexion()

        queryDireccion = "INSERT INTO direcciones (direccion, numero, piso, dpto) VALUES (%s, %s, %s, %s)"
        valuesDireccion = (proveedor.getDireccion().getDireccion(), proveedor.getDireccion().getNumero(),
                            proveedor.getDireccion().getPiso(), proveedor.getDireccion().getDpto())
        self.conexion.cursor.execute(queryDireccion, valuesDireccion)

        queryPersona = "INSERT INTO personas (nombre, email, direcciones_iddirecciones) VALUES (%s, %s, LAST_INSERT_ID())"
        valuesPersona = (proveedor.getNombre(), proveedor.getEmail())

        self.conexion.cursor.execute(queryPersona, valuesPersona)
        query1 = "INSERT INTO proveedores (personas_idpersonas, descripcion, web) VALUES (LAST_INSERT_ID(), %s, %s)"
        values1 = (proveedor.getDescripcion(), proveedor.getWeb())
        self.conexion.cursor.execute(query1, values1)
        self.conexion.db.commit()
        self.conexion.cerrarConexion()


    def borrarProveedor(self, proveedor):
        queryTelefono = """
                            DELETE telefonos
                            FROM telefonos, personas, proveedores
                            WHERE proveedores.personas_idpersonas = personas.idpersonas and
                                personas.idpersonas = telefonos.personas_idpersonas and idproveedores= %s
                        """
        valuesTelefono = proveedor.getIdProveedor()

        queryProveedores = """
                            DELETE FROM proveedores
                            WHERE proveedores.idproveedores = %s
                           """
        valuesProveedor = proveedor.getIdProveedor()

        queryPersona = """
                            DELETE personas
                            FROM personas
                            WHERE personas.idpersonas = %s
                       """
        valuesPersona = proveedor.getIdPersona()

        queryDireccion = """
                            DELETE direcciones
                            FROM direcciones
                            WHERE direcciones.iddirecciones = %s
                         """
        valuesDireccion = proveedor.getDireccion().getIdDireccion()

        self.conexion.abrirConexion()
        self.conexion.cursor.execute(queryTelefono, valuesTelefono)
        self.conexion.db.commit()
        self.conexion.cursor.execute(queryProveedores, valuesProveedor)
        self.conexion.db.commit()
        self.conexion.cursor.execute(queryPersona, valuesPersona)
        self.conexion.db.commit()
        self.conexion.cursor.execute(queryDireccion, valuesDireccion)
        self.conexion.db.commit()

        self.conexion.cerrarConexion()