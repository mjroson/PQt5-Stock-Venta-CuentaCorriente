#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Conexion.conexion import Conexion
from Modelo.cliente import Cliente

class conexionCliente(object):

    def __init__(self):
       self.conexion = Conexion()
       self.cliente = Cliente()

    def selectCliente(self):
        query = """SELECT cli.idClientes, cli.apellido, p.nombre, p.email, d.direccion, d.numero, d.piso, d.dpto,
                         d.iddirecciones, p.idpersonas
                    FROM clientes cli, personas p, direcciones d
                    WHERE p.idpersonas = cli.personas_idpersonas and d.iddirecciones = p.direcciones_iddirecciones"""
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query)
        listCliente = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listCliente

    def selectTelefonoCliente(self, cliente):
        query = """SELECT t.idtelefono, t.numero, t.tipo
                    FROM telefonos t, personas p, clientes c
                    WHERE p.idpersonas = c.personas_idpersonas and p.idpersonas = t.personas_idpersonas
                    and c.idClientes = %s"""
        values = cliente.getIdCliente()
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query)
        listTelefono = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listTelefono

    def modificarCliente(self, cliente):

        query = """UPDATE personas p, clientes c, direcciones d
                    SET p.nombre = %s , p.email= %s , c.apellido = %s, d.direccion= %s, d.numero = %s, d.piso = %s, d.dpto = %s
                    WHERE p.idpersonas = c.personas_idpersonas and p.direcciones_iddirecciones = d.iddirecciones
                            and c.idClientes = %s"""
        values = (cliente.getNombre(), cliente.getEmail(), cliente.getApellido(), cliente.getDireccion().getDireccion(),
                  cliente.getDireccion().getNumero(), cliente.getDireccion().getPiso(),
                  cliente.getDireccion().getDpto(), cliente.getIdCliente())
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        self.conexion.db.commit()
        self.conexion.cerrarConexion()

    def insertarCliente(self, cliente):
        self.conexion.abrirConexion()

        queryDireccion = "INSERT INTO direcciones (direccion, numero, piso, dpto) VALUES (%s, %s, %s, %s)"

        valuesDireccion = (cliente.getDireccion().getDireccion(), cliente.getDireccion().getNumero(),
                            cliente.getDireccion().getPiso(), cliente.getDireccion().getDpto())
        self.conexion.cursor.execute(queryDireccion, valuesDireccion)

        queryPersona = "INSERT INTO personas (nombre, email, direcciones_iddirecciones) VALUES (%s, %s, LAST_INSERT_ID())"
        valuesPersona = (cliente.getNombre(), cliente.getEmail())
        self.conexion.cursor.execute(queryPersona, valuesPersona)

        queryCliente = "INSERT INTO clientes (personas_idpersonas, apellido) VALUES (LAST_INSERT_ID(), %s)"
        valuesCliente = cliente.getApellido()
        self.conexion.cursor.execute(queryCliente, valuesCliente)

        self.conexion.db.commit()
        self.conexion.cerrarConexion()

    def borrarCliente(self, cliente):
        queryTelefono = """
                            DELETE telefonos
                            FROM telefonos
                            WHERE telefonos.personas_idpersonas = %s
                        """
        valuesTelefono = cliente.getIdPersona()

        queryCliente = """
                            DELETE clientes
                            FROM clientes
                            WHERE idClientes = %s
                       """
        valuesCliente = cliente.getIdCliente()

        queryPersona = """
                            DELETE personas
                            FROM personas
                            WHERE personas.idpersonas = %s
                       """
        valuesPersona = cliente.getIdPersona()

        queryDireccion = """
                            DELETE direcciones
                            FROM direcciones
                            WHERE direcciones.iddirecciones = %s
                         """
        valuesDireccion = cliente.getDireccion().getIdDireccion()

        self.conexion.abrirConexion()
        self.conexion.cursor.execute(queryTelefono, valuesTelefono)
        self.conexion.db.commit()
        self.conexion.cursor.execute(queryCliente, valuesCliente)
        self.conexion.db.commit()
        self.conexion.cursor.execute(queryPersona, valuesPersona)
        self.conexion.db.commit()
        self.conexion.cursor.execute(queryDireccion, valuesDireccion)
        self.conexion.db.commit()

        self.conexion.cerrarConexion()