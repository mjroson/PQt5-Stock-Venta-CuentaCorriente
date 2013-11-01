#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from PyQt5 import uic
from Modelo.rubro import Rubro
from Componentes.tableModel import MyTableModel
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QWidget
from Conexion.conexionRubro import conexionRubro
from Modelo.telefono import Telefono
from PyQt5.QtWidgets import QMessageBox, QDialog

class windowRubro():

    def __init__(self):

        #Definiendo variables
        self.winRubro = uic.loadUi('../Vista/abmRubro.ui')
        self.rubro = Rubro()
        self.conexionRubro = conexionRubro()
        self.contAttr = 0
        self.estado = "" #Variable donde guardo el estado, para saber que accion hace el boton guardar.
        #Configurando botones
        self.winRubro.btnGuardar_r.clicked.connect(self.onClickGuardar_r)
        self.winRubro.btnModificar_r.clicked.connect(self.onClickModificar_r)
        self.winRubro.btnBorrar_r.clicked.connect(self.onClickBorrar_r)
        self.winRubro.btnAgregar_r.clicked.connect(self.onClickAgregar_r)


        #Seteando tabla
        self.cargarTabla()
        #Seteo propiedades de la tabla

        self.winRubro.tvRubros_r.setSortingEnabled(True)
        self.winRubro.tvRubros_r.setMouseTracking(True)
        self.winRubro.tvRubros_r.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.winRubro.exec()
        #sys.executable(self.winRubro.exec_())

    def onClickGuardar_r(self):

        if self.winRubro.txtDescripcion_r.text() != "":

            self.rubro.setRubro(self.winRubro.txtDescripcion_r.text())

            if self.estado == 'AGREGAR':
                self.insertRubro()
            elif self.estado == 'MODIFICAR':
                self.modificarRubro()
        else:
            print("Falta completar el campo descripcion")
            alert = QDialog()
            QMessageBox.information(alert,"ERROR", "Falta completar el campo descripcion")

        self.validarBotones(button='GUARDAR')


    def onClickAgregar_r(self):
        self.estado = 'AGREGAR'
        self.validarBotones(button='AGREGAR')


    def onClickModificar_r(self):
        self.estado = 'MODIFICAR'
        self.validarBotones(button='MODIFICAR')

    def onClickBorrar_r(self):
        if self.rubro and self.winRubro.btnAgregar_r.isEnabled():
            self.conexionRubro.borrarRubro(self.rubro)
            self.cargarTabla()
        self.validarBotones(button='BORRAR')

    def cargarTabla(self):
        #Seteo el dataProvider de la tabla
        listaRubros = self.conexionRubro.selectRubro()
        header = ['ID', 'Rubro']
        self.tablaModel = MyTableModel(self.winRubro.tvRubros_r, listaRubros, header)
        self.winRubro.tvRubros_r.setModel(self.tablaModel)
        self.winRubro.tvRubros_r.selectionModel().currentChanged.connect(self.changeSelectedTable)

        self.winRubro.tvRubros_r.setColumnHidden(0, True)
        self.winRubro.tvRubros_r.setColumnWidth(1, 245)

    def changeSelectedTable(self, selected, deselected):
        self.winRubro.tvRubros_r.selectRow(selected.row())

        rubroList = selected.model().mylist
        rubroSelected = rubroList[selected.row()]

        self.rubro = Rubro()
        self.rubro.setIdRubro(int(rubroSelected[0]))
        self.rubro.setRubro(str(rubroSelected[1]))

        self.winRubro.tvRubros_r.setRowHeight(deselected.row(), 33)
        self.winRubro.tvRubros_r.setRowHeight(selected.row(), 45)

        self.winRubro.txtDescripcion_r.setText(str(self.rubro.getRubro()))
        self.winRubro.btnModificar_r.setEnabled(True)
        self.winRubro.btnBorrar_r.setEnabled(True)


    def validarBotones(self, button):
        if button == 'AGREGAR':
            self.winRubro.btnModificar_r.setEnabled(False)
            self.winRubro.btnAgregar_r.setEnabled(False)
            self.winRubro.btnGuardar_r.setEnabled(True)
            self.winRubro.btnBorrar_r.setText('CANCELAR')
            self.winRubro.btnBorrar_r.setEnabled(True)
            self.winRubro.tvRubros_r.setEnabled(False)
            self.winRubro.txtDescripcion_r.setText('')
            self.winRubro.txtDescripcion_r.setEnabled(True)
        elif button == 'GUARDAR':
            self.winRubro.btnModificar_r.setEnabled(False)
            self.winRubro.btnAgregar_r.setEnabled(True)
            self.winRubro.btnGuardar_r.setEnabled(False)
            self.winRubro.btnBorrar_r.setText('BORRAR')
            self.winRubro.btnBorrar_r.setEnabled(False)
            self.winRubro.tvRubros_r.setEnabled(True)
            self.winRubro.txtDescripcion_r.setText('')
            self.winRubro.txtDescripcion_r.setEnabled(False)
        elif button == 'MODIFICAR':
            self.winRubro.btnModificar_r.setEnabled(False)
            self.winRubro.btnAgregar_r.setEnabled(False)
            self.winRubro.btnGuardar_r.setEnabled(True)
            self.winRubro.btnBorrar_r.setText('CANCELAR')
            self.winRubro.btnBorrar_r.setEnabled(True)
            self.winRubro.tvRubros_r.setEnabled(False)
            self.winRubro.txtDescripcion_r.setEnabled(True)
        elif button == 'BORRAR':
            self.winRubro.btnModificar_r.setEnabled(False)
            self.winRubro.btnAgregar_r.setEnabled(True)
            self.winRubro.btnGuardar_r.setEnabled(False)
            self.winRubro.btnBorrar_r.setText('BORRAR')
            self.winRubro.btnBorrar_r.setEnabled(False)
            self.winRubro.tvRubros_r.setEnabled(True)
            self.winRubro.txtDescripcion_r.setText('')
            self.winRubro.txtDescripcion_r.setEnabled(False)

    def insertRubro(self):
        if self.rubro:
            self.conexionRubro.insertarRubro(self.rubro)
            self.cargarTabla()


    def modificarRubro(self):
         if self.rubro:
            self.conexionRubro.modificarRubro(self.rubro)
            self.cargarTabla()
