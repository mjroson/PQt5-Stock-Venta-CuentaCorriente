#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Conexion.conexion import Conexion
from Modelo.cliente import Cliente

class conexionCliente(object):

    def __init__(self):
       self.conexion = Conexion()
       self.cliente = Cliente()

    def selectCliente(self, typeParameter, parameter, parameterState):
        query = """
                    SELECT cli.idClientes, cli.apellido, p.nombre, p.email, d.direccion, d.numero, d.piso, d.dpto,
                         d.iddirecciones, p.idpersonas, cli.estado
                    FROM clientes cli, personas p, direcciones d
                    WHERE p.idpersonas = cli.personas_idpersonas and d.iddirecciones = p.direcciones_iddirecciones and
                    """ +typeParameter + """ LIKE %s and cli.estado LIKE %s
                """
        paramState = '1'
        if parameterState == 0:
            paramState = '%'

        param = parameter+ '%'
        values = (param, paramState)
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
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
                    SET p.nombre = %s , p.email= %s , c.apellido = %s, d.direccion= %s, d.numero = %s, d.piso = %s, d.dpto = %s, c.estado = %s
                    WHERE p.idpersonas = c.personas_idpersonas and p.direcciones_iddirecciones = d.iddirecciones
                            and c.idClientes = %s"""
        values = (cliente.getNombre(), cliente.getEmail(), cliente.getApellido(), cliente.getDireccion().getDireccion(),
                  cliente.getDireccion().getNumero(), cliente.getDireccion().getPiso(),
                  cliente.getDireccion().getDpto(), cliente.getEstado(), cliente.getIdCliente())
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

        queryCliente = "INSERT INTO clientes (personas_idpersonas, apellido, estado) VALUES (LAST_INSERT_ID(), %s, %s)"
        valuesCliente = (cliente.getApellido(), cliente.getEstado())
        self.conexion.cursor.execute(queryCliente, valuesCliente)

        self.conexion.db.commit()
        self.conexion.cerrarConexion()

    def borrarCliente(self, cliente):
        queryCliente = """
                            UPDATE clientes
                            SET estado = 0
                            WHERE idClientes = %s
                       """
        valuesCliente = cliente.getIdCliente()

        self.conexion.abrirConexion()
        self.conexion.cursor.execute(queryCliente, valuesCliente)
        self.conexion.db.commit()
        self.conexion.cerrarConexion()