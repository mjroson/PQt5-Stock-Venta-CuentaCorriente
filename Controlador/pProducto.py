#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Componentes.tableModel import MyTableModel
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QCompleter, QLineEdit
from Conexion.conexionProducto import conexionProducto
from Controlador.windowMarca import windowMarca
from Controlador.windowRubro import windowRubro
from Modelo.proveedor import Proveedor
from Modelo.producto import Producto
from Modelo.rubro import Rubro
from Modelo.marca import Marca
from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractItemModel
from PyQt5 import Qt
from PyQt5.QtWidgets import QMessageBox, QDialog


class PestaniaProducto():

    def __init__(self, winPrincipal):
        self.winPrincipal = winPrincipal
        self.producto = Producto()
        self.proveedor = Proveedor()
        self.marca = Marca()
        self.rubro = Rubro()
        self.estado = ""
        self.conexionProducto = conexionProducto()

        self.completerRubro = QCompleter()
        self.completerMarca = QCompleter()
        self.completerProveedor = QCompleter()
        self.configInit()



    def configInit(self):
        #Configurando botones
        self.winPrincipal.btnAgregar_p.clicked.connect(self.onClickAgregar_p)
        self.winPrincipal.btnGuardar_p.clicked.connect(self.onClickGuardar_p)
        self.winPrincipal.btnBorrar_p.clicked.connect(self.onClickBorrar_p)
        self.winPrincipal.btnModificar_p.clicked.connect(self.onClickModificar_p)

        self.winPrincipal.btnRubro_p.clicked.connect(windowRubro)
        self.winPrincipal.btnMarca_p.clicked.connect(windowMarca)

        #windowMarca.connect(windowMarca, Qt.SIGNAL('destroyed()'), self.onQuitMarca)
        self.winPrincipal.txtFilterProductos_p.returnPressed.connect(self.search)

        #self.cargarTabla()
        self.winPrincipal.tvProductos_p.setMouseTracking(True)
        self.winPrincipal.tvProductos_p.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.setCompleterMarca()
        self.setCompleterRubro()
        self.setCompleterProveedor()

        self.winPrincipal.txtFilterProductos_p.setFocus(True)



    def finish(self):
        self.winPrincipal.btnAgregar_p.disconnect()
        self.winPrincipal.btnGuardar_p.disconnect()
        self.winPrincipal.btnModificar_p.disconnect()
        self.winPrincipal.btnBorrar_p.disconnect()
        self.winPrincipal.btnRubro_p.disconnect()
        self.winPrincipal.btnMarca_p.disconnect()
        self.winPrincipal.tvProductos_p.disconnect()

    def search(self):
        if self.winPrincipal.txtFilterProductos_p.hasFocus() is True:
            self.cargarTabla()

    def onClickAgregar_p(self):
        self.estado = 'AGREGAR'
        self.validarBotones(button='AGREGAR')

    def onClickGuardar_p(self):
        validar = self.validar()

        if validar != "":
            print(validar)
            alert = QDialog()
            QMessageBox.information(alert,"ERROR", validar)
        else:
            self.producto.setDescripcion(str(self.winPrincipal.txtDescripcion_p.toPlainText()))
            self.producto.setCantidad(int(self.winPrincipal.sbCantidad_p.value()))
            self.producto.setCantidadMinima(int(self.winPrincipal.sbCantidadMin_p.value()))
            if self.winPrincipal.cbEstado_p.currentText() == "ACTIVO":
                self.producto.setEstado(1)
            else:
                self.producto.setEstado(0)

            if self.winPrincipal.rbFemenino_p.isChecked() is True:
                self.producto.setGenero("F")
            elif self.winPrincipal.rbMasculino_p.isChecked() is True:
                self.producto.setGenero("M")
            else:
                self.producto.setGenero("I")

            self.producto.setNombre(str(self.winPrincipal.txtNombre_p.text()))
            self.producto.setPrecioCompra(float(self.winPrincipal.txtPrecioCompra_p.text()))
            self.producto.setPrecioVenta(float(self.winPrincipal.txtPrecioVenta_p.text()))

            self.rubro.setRubro(str(self.completerRubro.currentCompletion()))
            self.producto.setRubro(self.rubro)

            self.proveedor.setDescripcion(str(self.completerProveedor.currentCompletion()))
            self.producto.setProveedor(self.proveedor)

            self.marca.setMarca(str(self.completerMarca.currentCompletion()))
            self.producto.setMarca(self.marca)

            if self.estado == 'AGREGAR':
                self.insertarProducto()
            elif self.estado == 'MODIFICAR':
                self.modificarProducto()

            self.validarBotones('GUARDAR')


    def onClickModificar_p(self):
        self.estado = 'MODIFICAR'
        self.validarBotones(button='MODIFICAR')

    def onClickBorrar_p(self):
        if self.winPrincipal.btnGuardar_p.isEnabled() != True:
            self.conexionProducto.borrarProducto(self.producto)
            self.cargarTabla()

        self.validarBotones(button='BORRAR')

    def cargarTabla(self):

        parameter = self.winPrincipal.txtFilterProductos_p.text()
        typeParameter = ''
        if self.winPrincipal.cbFilterProducto_p.currentText() == 'Nombre':
            typeParameter = 'p.nombre'
        elif self.winPrincipal.cbFilterProducto_p.currentText() == 'Marca':
            typeParameter = 'm.descripcion'
        else:
            typeParameter = 'r.descripcion'

        parameterState = 1
        if self.winPrincipal.cbInactivo_p.isChecked() is True:
            parameterState = 0

        parameterStock = 1
        if self.winPrincipal.cbSinStock_p.isChecked() is True:
            parameterStock = 0

        listaProductos = self.conexionProducto.selectProducto(typeParameter, parameter, parameterState, parameterStock)

        if len(listaProductos) > 0:

            header = ['idPro','Nombre', 'Descripcion', 'PC', 'PV', 'G', 'Estado', 'Cant', 'Cantidad Min',
                      'idMar', 'Marca', 'idRubro', 'Rubro', 'idProv', 'Proveedor']
            self.tablaModel = MyTableModel(self.winPrincipal.tvProductos_p, listaProductos, header)
            self.winPrincipal.tvProductos_p.setModel(self.tablaModel)
            self.winPrincipal.tvProductos_p.selectionModel().currentChanged.connect(self.changeSelectedTable)

            self.winPrincipal.tvProductos_p.setColumnHidden(0, True)
            self.winPrincipal.tvProductos_p.setColumnWidth(1, 200)
            self.winPrincipal.tvProductos_p.setColumnWidth(2, 320)
            self.winPrincipal.tvProductos_p.setColumnWidth(3, 60)
            self.winPrincipal.tvProductos_p.setColumnWidth(4, 60)
            self.winPrincipal.tvProductos_p.setColumnWidth(5, 60)
            self.winPrincipal.tvProductos_p.setColumnHidden(6, True)
            self.winPrincipal.tvProductos_p.setColumnWidth(7, 40)
            self.winPrincipal.tvProductos_p.setColumnHidden(8, True)
            self.winPrincipal.tvProductos_p.setColumnHidden(9, True)
            self.winPrincipal.tvProductos_p.setColumnWidth(10, 130)
            self.winPrincipal.tvProductos_p.setColumnHidden(11, True)
            self.winPrincipal.tvProductos_p.setColumnWidth(12, 130)
            self.winPrincipal.tvProductos_p.setColumnHidden(13, True)
            self.winPrincipal.tvProductos_p.setColumnWidth(14, 130)
        else:
            self.winPrincipal.tvProductos_p.setModel(None)



    def changeSelectedTable(self, selected, deselected):

        productoList = selected.model().mylist
        productoSelected = productoList[selected.row()]
        self.producto = Producto()
        self.rubro = Rubro()
        self.proveedor = Proveedor()
        self.marca = Marca()

        self.producto.setIdProducto(productoSelected[0])
        self.producto.setNombre(productoSelected[1])
        self.producto.setDescripcion(productoSelected[2])
        self.producto.setPrecioCompra(productoSelected[3])
        self.producto.setPrecioVenta(productoSelected[4])
        self.producto.setGenero(productoSelected[5])
        self.producto.setEstado(productoSelected[6])
        self.producto.setCantidad(productoSelected[7])
        self.producto.setCantidadMinima(productoSelected[8])

        self.marca.setIdMarca(productoSelected[9])
        self.marca.setMarca(productoSelected[10])
        self.producto.setMarca(self.marca)

        self.rubro.setIdRubro(productoSelected[11])
        self.rubro.setRubro(productoSelected[12])
        self.producto.setRubro(self.rubro)

        self.proveedor.setIdProveedor(productoSelected[13])
        self.proveedor.setDescripcion(productoSelected[14])
        self.producto.setProveedor(self.proveedor)


        self.winPrincipal.tvProductos_p.setRowHeight(deselected.row(),33)
        self.winPrincipal.tvProductos_p.setRowHeight(selected.row(),45)

        self.setCampos()
        self.winPrincipal.btnModificar_p.setEnabled(True)
        self.winPrincipal.btnBorrar_p.setEnabled(True)

    def validarBotones(self, button):
        if button == 'AGREGAR' :
            self.winPrincipal.wDatosProducto.setEnabled(True)
            self.winPrincipal.btnBorrar_p.setEnabled(True)
            self.winPrincipal.btnBorrar_p.setText('CANCELAR')
            self.winPrincipal.btnGuardar_p.setEnabled(True)
            self.winPrincipal.btnModificar_p.setEnabled(False)
            self.winPrincipal.btnAgregar_p.setEnabled(False)
            self.winPrincipal.tvProductos_p.setEnabled(False)
            self.limpiarCampos()

        elif button=='GUARDAR':
            self.winPrincipal.btnModificar_p.setEnabled(False)
            self.winPrincipal.btnAgregar_p.setEnabled(True)
            self.winPrincipal.btnGuardar_p.setEnabled(False)
            self.winPrincipal.btnBorrar_p.setText('BORRAR')
            self.winPrincipal.btnBorrar_p.setEnabled(False)
            self.winPrincipal.tvProductos_p.setEnabled(True)
            self.winPrincipal.wDatosProducto.setEnabled(False)
            self.limpiarCampos()

        elif button == 'MODIFICAR':
            self.winPrincipal.btnModificar_p.setEnabled(False)
            self.winPrincipal.btnAgregar_p.setEnabled(False)
            self.winPrincipal.btnGuardar_p.setEnabled(True)
            self.winPrincipal.btnBorrar_p.setText('CANCELAR')
            self.winPrincipal.btnBorrar_p.setEnabled(True)
            self.winPrincipal.tvProductos_p.setEnabled(False)
            self.winPrincipal.wDatosProducto.setEnabled(True)

        elif button=='BORRAR':
            self.winPrincipal.btnModificar_p.setEnabled(False)
            self.winPrincipal.btnAgregar_p.setEnabled(True)
            self.winPrincipal.btnGuardar_p.setEnabled(False)
            self.winPrincipal.btnBorrar_p.setText('BORRAR')
            self.winPrincipal.btnBorrar_p.setEnabled(False)
            self.winPrincipal.tvProductos_p.setEnabled(True)
            self.winPrincipal.wDatosProducto.setEnabled(False)
            self.limpiarCampos()


    def insertarProducto(self):
        self.conexionProducto.insertarProducto(producto=self.producto)
        self.cargarTabla()

    def modificarProducto(self):
        self.conexionProducto.modificarProducto(self.producto)
        self.cargarTabla()

    def limpiarCampos(self):
        self.winPrincipal.txtNombre_p.setText('')
        self.winPrincipal.txtPrecioCompra_p.setText('')
        self.winPrincipal.txtPrecioVenta_p.setText('')
        self.winPrincipal.sbCantidad_p.setValue(0)
        self.winPrincipal.sbCantidadMin_p.setValue(0)
        self.winPrincipal.txtProveedor_p.setText('')
        self.winPrincipal.txtDescripcion_p.setText('')
        self.winPrincipal.txtRubro_p.setText('')
        self.winPrincipal.txtMarca_p.setText('')
        self.completerProveedor.setCurrentRow(0)
        self.completerRubro.setCurrentRow(0)
        self.completerMarca.setCurrentRow(0)
        self.winPrincipal.txtFilterProductos_p.setText('')
        self.winPrincipal.tvProductos_p.setModel(None)

        self.winPrincipal.txtFilterProductos_p.setFocus(True)

    def setCampos(self):
        self.winPrincipal.txtNombre_p.setText(self.producto.getNombre())
        self.winPrincipal.txtDescripcion_p.setText(str(self.producto.getDescripcion()))
        self.winPrincipal.txtPrecioCompra_p.setText(str(self.producto.getPrecioCompra()))
        self.winPrincipal.txtPrecioVenta_p.setText(str(self.producto.getPrecioVenta()))
        self.winPrincipal.txtProveedor_p.setText(str(self.producto.getProveedor().getDescripcion()))

        self.winPrincipal.sbCantidad_p.setValue(int(self.producto.getCantidad()))
        self.winPrincipal.sbCantidadMin_p.setValue(int(self.producto.getCantidadMinima()))

        self.winPrincipal.txtRubro_p.setText(str(self.producto.getRubro().getRubro()))
        self.winPrincipal.txtMarca_p.setText(str(self.producto.getMarca().getMarca()))

        if self.producto.getEstado() == 1:
            self.winPrincipal.cbEstado_p.setCurrentIndex(0)
        else:
            self.winPrincipal.cbEstado_p.setCurrentIndex(1)

        if self.producto.getGenero() == 'F':
            self.winPrincipal.rbFemenino_p.setChecked(True)
        elif self.producto.getGenero() == 'M':
            self.winPrincipal.rbMasculino_p.setChecked(True)
        else:
            self.winPrincipal.rbIndiferente_p.setChecked(True)




    def validar(self):
        mensaje=''
        if self.winPrincipal.txtNombre_p.text() == '':
            mensaje= "Falta ingresar Nombre"
        elif self.winPrincipal.txtPrecioCompra_p.text() =='':
            mensaje= "Falta ingresar Precio de Compra"
        elif self.winPrincipal.txtPrecioVenta_p.text() =='':
            mensaje= "Falta ingresar Precio de Venta"
        elif self.completerProveedor.currentCompletion() =='':
            mensaje= "Falta ingresar un Proveedor"
        elif self.completerMarca.currentCompletion() == '':
            mensaje = "Falta seleccionar la marca"
        elif self.completerRubro.currentCompletion() == '':
            mensaje = 'Falta seleccionar el rubro'


        """elif self.completerProveedor.currentCompletion() =='' or self.completerProveedor.currentRow() == 0:
            mensaje= "Falta ingresar un Proveedor"
        elif self.completerMarca.currentCompletion() == '' or self.completerMarca.currentRow() == 0:
            mensaje = "Falta seleccionar la marca"
        elif self.completerRubro.currentCompletion() == '' or self.completerRubro.currentRow() == 0:
            mensaje = 'Falta seleccionar el rubro'
        """
        return mensaje

    def setCompleterMarca(self):
        listMarcas = self.conexionProducto.listMarcas()
        self.completerMarca = QCompleter(listMarcas)

        self.completerMarca.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.winPrincipal.txtMarca_p.setCompleter(self.completerMarca)


    def setCompleterRubro(self):
        listRubros = self.conexionProducto.listRubro()
        self.completerRubro = QCompleter(listRubros)
        #self.completerRubro.dynamicPropertyNames()
        self.completerRubro.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.winPrincipal.txtRubro_p.setCompleter(self.completerRubro)



    def setCompleterProveedor(self):
        listProveedores = self.conexionProducto.listProveedor()
        self.completerProveedor = QCompleter(listProveedores)

        self.completerProveedor.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.winPrincipal.txtProveedor_p.setCompleter(self.completerProveedor)


