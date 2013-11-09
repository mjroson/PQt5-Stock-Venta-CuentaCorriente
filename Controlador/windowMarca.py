#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from PyQt5 import uic
from Modelo.marca import Marca
from Conexion.conexionMarca import conexionMarca
from Componentes.tableModel import MyTableModel
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QWidget
from Modelo.telefono import Telefono
from PyQt5.QtWidgets import QMessageBox, QDialog

class windowMarca():

    def __init__(self):

        self.winMarca = uic.loadUi('../Vista/abmMarca.ui')

        #Configurando botones
        self.marca = Marca()
        self.conexionMarca = conexionMarca()


        self.winMarca.btnGuardar_m.clicked.connect(self.onClickGuardar_m)
        self.winMarca.btnModificar_m.clicked.connect(self.onClickModificar_m)
        self.winMarca.btnBorrar_m.clicked.connect(self.onClickBorrar_m)
        self.winMarca.btnAgregar_m.clicked.connect(self.onClickAgregar_m)

        self.winMarca.txtFilterMarcas_m.returnPressed.connect(self.search)

        self.winMarca.tvMarcas_m.setSortingEnabled(True)
        self.winMarca.tvMarcas_m.setMouseTracking(True)
        self.winMarca.tvMarcas_m.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.winMarca.exec()

    def search(self):
        if self.winMarca.txtFilterMarcas_m.hasFocus() is True:
            self.cargarTabla()

    def onClickGuardar_m(self):

        if self.winMarca.txtDescripcion_m.text() != "":

            self.marca.setMarca(self.winMarca.txtDescripcion_m.text())

            if self.estado == 'AGREGAR':
                self.insertMarca()
            elif self.estado == 'MODIFICAR':
                self.modificarMarca()
        else:
            print("Falta ingresar la descripcion")
            alert = QDialog()
            QMessageBox.information(alert,"ERROR", "Falta ingresar la descripcion")

        self.validarBotones(button='GUARDAR')

    def onClickAgregar_m(self):
        self.estado = 'AGREGAR'
        self.validarBotones(button='AGREGAR')

    def onClickModificar_m(self):
        self.estado='MODIFICAR'
        self.validarBotones(button='MODIFICAR')

    def onClickBorrar_m(self):
        if self.marca.getIdMarca() != 0 and self.winMarca.btnGuardar_m.isEnabled() != True:
                self.conexionMarca.borrarMarca(self.marca)
                self.cargarTabla()
        self.validarBotones(button='BORRAR')

    def cargarTabla(self):
        textFilter = self.winMarca.txtFilterMarcas_m.text()
        listaMarcas = self.conexionMarca.selectMarca(textFilter)
        if len(listaMarcas) > 0:
            #Creo la cabecera
            header = ['ID', 'Marca']
            #Creo el modelo
            self.tablaModel = MyTableModel(self.winMarca.tvMarcas_m, listaMarcas, header)
            #Seteo el modelo
            self.winMarca.tvMarcas_m.setModel(self.tablaModel)
            self.winMarca.tvMarcas_m.selectionModel().currentChanged.connect(self.changeSelectedTable)

            self.winMarca.tvMarcas_m.setColumnHidden(0, True)
            self.winMarca.tvMarcas_m.setColumnWidth(1, 245)
        else:
            self.winMarca.tvMarcas_m.setModel(None)

    def changeSelectedTable(self, selected, deselected):
        self.winMarca.tvMarcas_m.selectRow(selected.row())

        marcaList = selected.model().mylist
        marcaSelected = marcaList[selected.row()]

        self.marca = Marca()
        self.marca.setIdMarca(int(marcaSelected[0]))
        self.marca.setMarca(str(marcaSelected[1]))

        self.winMarca.tvMarcas_m.setRowHeight(deselected.row(), 33)
        self.winMarca.tvMarcas_m.setRowHeight(selected.row(), 45)

        self.winMarca.txtDescripcion_m.setText(self.marca.getMarca())
        self.winMarca.btnModificar_m.setEnabled(True)
        self.winMarca.btnBorrar_m.setEnabled(True)

    def validarBotones(self, button):
        if button == 'AGREGAR':
            self.winMarca.btnModificar_m.setEnabled(False)
            self.winMarca.btnAgregar_m.setEnabled(False)
            self.winMarca.btnGuardar_m.setEnabled(True)
            self.winMarca.btnBorrar_m.setText('CANCELAR')
            self.winMarca.btnBorrar_m.setEnabled(True)
            self.winMarca.tvMarcas_m.setEnabled(False)
            self.winMarca.txtDescripcion_m.setText('')
            self.winMarca.txtDescripcion_m.setEnabled(True)
        elif button == 'GUARDAR':
            self.winMarca.btnModificar_m.setEnabled(False)
            self.winMarca.btnAgregar_m.setEnabled(True)
            self.winMarca.btnGuardar_m.setEnabled(False)
            self.winMarca.btnBorrar_m.setText('BORRAR')
            self.winMarca.btnBorrar_m.setEnabled(False)
            self.winMarca.tvMarcas_m.setEnabled(True)
            self.winMarca.txtDescripcion_m.setText('')
            self.winMarca.txtDescripcion_m.setEnabled(False)
        elif button == 'MODIFICAR':
            self.winMarca.btnModificar_m.setEnabled(False)
            self.winMarca.btnAgregar_m.setEnabled(False)
            self.winMarca.btnGuardar_m.setEnabled(True)
            self.winMarca.btnBorrar_m.setText('CANCELAR')
            self.winMarca.btnBorrar_m.setEnabled(True)
            self.winMarca.tvMarcas_m.setEnabled(False)
            self.winMarca.txtDescripcion_m.setEnabled(True)
        elif button == 'BORRAR':
            self.winMarca.btnModificar_m.setEnabled(False)
            self.winMarca.btnAgregar_m.setEnabled(True)
            self.winMarca.btnGuardar_m.setEnabled(False)
            self.winMarca.btnBorrar_m.setText('BORRAR')
            self.winMarca.btnBorrar_m.setEnabled(False)
            self.winMarca.tvMarcas_m.setEnabled(True)
            self.winMarca.txtDescripcion_m.setText('')
            self.winMarca.txtDescripcion_m.setEnabled(False)

    def insertMarca(self):
        if self.marca:
            self.conexionMarca.insertMarca(self.marca)
            self.cargarTabla()

    def modificarMarca(self):
        if self.marca:
                self.conexionMarca.modificarMarca(self.marca)
                self.cargarTabla()