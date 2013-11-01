#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql




class Conexion(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.db_host ='localhost'
        self.db_port = 3306
        self.db_user = 'root'
        self.db_pass = 'laserjet1'
        self.db_name ='db_perfumeria'
        

    def conectar(self):
        self.db = pymysql.connect(host=self.db_host, user=self.db_user,
                                  passwd=self.db_pass, db=self.db_name)

    def abrir_cursor(self):
        self.cursor = self.db.cursor()

        
    def cerrar_cursor(self):
        self.cursor.close()
        
    def cerrar_conexion(self):
        self.db.close()

    def abrirConexion(self):
        if (self.db_host and self.db_name and self.db_pass and self.db_port and self.db_user):
            self.conectar()
            self.abrir_cursor()
    
    def cerrarConexion(self):
        self.cerrar_cursor()
        self.cerrar_conexion()
            