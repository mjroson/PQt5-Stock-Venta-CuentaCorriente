#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Modelo.proveedor import Proveedor
from Conexion.conexion import Conexion
class conexionProveedor(object):


    def __init__(self):
        self.conexion = Conexion()
        self.proveedor = Proveedor()

    def selectProveedor(self, typeParameter, parameter, parameterState):
        query ="""
                    SELECT prov.idproveedores, prov.descripcion, p.nombre, p.email, prov.web, d.direccion, d.numero,
                        d.piso, d.dpto, p.idpersonas, d.iddirecciones, prov.estado
                    FROM proveedores prov, personas p, direcciones d
                    WHERE p.direcciones_iddirecciones = d.iddirecciones and p.idpersonas = prov.personas_idpersonas and
                    """ + typeParameter + """ LIKE %s and prov.estado LIKE %s
               """
        param = parameter + '%'

        paramState = '1'
        if parameterState == 0:
            paramState = '%'

        values = (param, paramState)
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
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
                            d.numero = %s, d.piso = %s, d.dpto = %s, prov.estado = %s
                    WHERE p.idpersonas = prov.personas_idpersonas and p.direcciones_iddirecciones = d.iddirecciones
                            and prov.idproveedores = %s
                """
        values = (proveedor.getNombre(), proveedor.getEmail(), proveedor.getDescripcion(),
                    proveedor.getWeb(), proveedor.getDireccion().getDireccion(), proveedor.getDireccion().getNumero(),
                    proveedor.getDireccion().getPiso(), proveedor.getDireccion().getDpto(), proveedor.getEstado(),
                    proveedor.getIdProveedor()
        )
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
        query1 = "INSERT INTO proveedores (personas_idpersonas, descripcion, web, estado) VALUES (LAST_INSERT_ID(), %s, %s, %s)"
        values1 = (proveedor.getDescripcion(), proveedor.getWeb(), proveedor.getEstado())
        self.conexion.cursor.execute(query1, values1)
        self.conexion.db.commit()
        self.conexion.cerrarConexion()


    def borrarProveedor(self, proveedor):
        queryProveedores = """
                            UPDATE proveedores
                            SET estado = 0
                            WHERE proveedores.idproveedores = %s
                           """
        valuesProveedor = proveedor.getIdProveedor()

        self.conexion.abrirConexion()
        self.conexion.cursor.execute(queryProveedores, valuesProveedor)
        self.conexion.db.commit()
        self.conexion.cerrarConexion()