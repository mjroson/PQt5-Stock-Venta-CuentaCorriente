#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Conexion.conexion import Conexion
from Modelo.usuario import Usuario
class conexionUsuario(object):

    def __init__(self):
        self.conexion = Conexion()
        self.usuario = Usuario()

    def selectUsuario(self, typeParameter, parameter):
        query = """
                    SELECT u.idusuarios, p.nombre, u.apellido, u.usuario, u.tipo, u.contraseña, p.email, d.direccion,
                            d.numero, d.piso, d.dpto, d.iddirecciones, p.idpersonas
                    FROM usuarios u , personas p, direcciones d
                    WHERE p.idpersonas = u.personas_idpersonas and p.direcciones_iddirecciones = d.iddirecciones and
                    """ + typeParameter + """ LIKE %s
                """
        param = parameter + '%'
        values = param
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listUsuario = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listUsuario

    def selectTelefonoUsuario(self, usuario):
        query = """
                    SELECT t.idtelefono, t.numero, t.tipo
                    FROM telefonos t, personas p, usuarios u",
                    WHERE p.idpersonas = u.personas_idpersonas and p.idpersonas = t.personas_idpersonas
                    and usuarios.idusuarios = %s
                """
        values = usuario.getIdUsuario()
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listTelefono = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listTelefono

    def modificarUsuario(self, usuario):
        query = """
                    UPDATE personas p, usuarios u, direcciones d
                    SET p.nombre = %s , p.email= %s, u.apellido = %s, u.usuario = %s,
                        u.tipo = %s, u.contraseña = %s, d.direccion = %s, d.numero = %s, d.piso = %s, d.dpto = %s
                    WHERE p.idpersonas = u.personas_idpersonas and p.direcciones_iddirecciones = d.iddirecciones
                        and u.idusuarios = %s
                """
        values = (usuario.getNombre(), usuario.getEmail(), usuario.getApellido(), usuario.getUsuario(),
                  usuario.getTipoUsuario(), usuario.getPasswd(), usuario.getDireccion().getDireccion(),
                  usuario.getDireccion().getNumero(), usuario.getDireccion().getPiso(),
                  usuario.getDireccion().getDpto(), usuario.getIdUsuario())
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        self.conexion.db.commit()
        self.conexion.cerrarConexion()

    def insertarUsuario(self, usuario):
        self.conexion.abrirConexion()

        queryDireccion = "INSERT INTO direcciones (direccion, numero, piso, dpto) VALUES (%s, %s, %s, %s)"
        valuesDireccion = (usuario.getDireccion().getDireccion(), usuario.getDireccion().getNumero(),
                            usuario.getDireccion().getPiso(), usuario.getDireccion().getDpto())
        self.conexion.cursor.execute(queryDireccion, valuesDireccion)

        queryPersona = "INSERT INTO personas (nombre, email, direcciones_iddirecciones) VALUES (%s, %s, LAST_INSERT_ID())"
        valuesPersona = (usuario.getNombre(), usuario.getEmail())
        self.conexion.cursor.execute(queryPersona, valuesPersona)

        queryUsuario = """INSERT INTO usuarios (tipo, personas_idpersonas, contraseña, usuario, apellido)
                        VALUES ( %s , LAST_INSERT_ID() , %s , %s , %s )"""
        valuesUsuario = (usuario.getTipoUsuario(), usuario.getPasswd(), usuario.getUsuario(), usuario.getApellido())
        self.conexion.cursor.execute(queryUsuario, valuesUsuario)

        self.conexion.db.commit()
        self.conexion.cerrarConexion()

    def borrarUsuario(self, usuario):
        queryTelefono = """
                            DELETE telefonos
                            FROM telefonos
                            WHERE telefonos.personas_idpersonas = %s
                        """
        valuesTelefono = usuario.getIdPersona()

        queryUsuario = """
                            DELETE usuarios
                            FROM usuarios
                            WHERE usuarios.idusuarios = %s
                       """

        valuesUsuario = usuario.getIdUsuario()

        queryPersona = """
                            DELETE personas
                            FROM personas
                            WHERE personas.idpersonas = %s
                       """

        valuesPersona = usuario.getIdPersona()

        queryDireccion = """
                            DELETE direcciones
                            FROM direcciones
                            WHERE direcciones.iddirecciones = %s
                         """

        valuesDireccion = usuario.getDireccion().getIdDireccion()

        self.conexion.abrirConexion()
        self.conexion.cursor.execute(queryTelefono, valuesTelefono)
        self.conexion.db.commit()
        self.conexion.cursor.execute(queryUsuario, valuesUsuario)
        self.conexion.db.commit()
        self.conexion.cursor.execute(queryPersona, valuesPersona)
        self.conexion.db.commit()
        self.conexion.cursor.execute(queryDireccion, valuesDireccion)
        self.conexion.db.commit()

        self.conexion.cerrarConexion()


    def validarUsuario(self, usuario):
        query = "SELECT usuario, tipo FROM usuarios WHERE usuario= %s and contraseña = %s"
        values = (usuario.getUsuario(), usuario.getPasswd())
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        auxUsuario = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return auxUsuario
