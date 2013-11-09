import sys

from PyQt5 import uic
from Modelo.producto import Producto
from Conexion.conexionGeneral import ConexionGenerales
from Componentes.tableModel import MyTableModel
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QWidget

from PyQt5.QtWidgets import QMessageBox, QDialog

class WindowNotification():

    def __init__(self):

        self.winNot = uic.loadUi('../Vista/windowListNotify.ui')

        self.producto = Producto()

        self.conexionGeneral = ConexionGenerales()

        self.cargarTabla()

        self.winNot.btnSalir.clicked.connect(self.close)
        self.winNot.btnDesactivar.clicked.connect(self.desactivarProducto)

        self.winNot.tvDetalle.setSortingEnabled(True)
        self.winNot.tvDetalle.setMouseTracking(True)
        self.winNot.tvDetalle.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.winNot.exec()

        self.winNot.btnDesactivar.setEnabled(False)
        #sys.executable(self.winNot.exec_())


    def cargarTabla(self):
        listProducto = self.conexionGeneral.selectProductoStock()

        header = ['ID', 'Nombre', 'Cant', 'Cant Min']
        if len(listProducto) > 0:
            tableModel = MyTableModel(self.winNot.tvDetalle, listProducto, header)
            self.winNot.tvDetalle.setModel(tableModel)
            self.winNot.tvDetalle.selectionModel().currentChanged.connect(self.changeSelectedTable)


            self.winNot.tvDetalle.setColumnHidden(0, True)
            self.winNot.tvDetalle.setColumnWidth(1, 128)
            self.winNot.tvDetalle.setColumnWidth(2, 70)
            self.winNot.tvDetalle.setColumnWidth(3, 70)



    def changeSelectedTable(self, selected, deselected):
        listProductos = selected.model().mylist
        productoSelected = ()
        productoSelected = tuple(listProductos[selected.row()])

        self.productoSelected = selected.row()

        self.producto = Producto()
        self.producto.setIdProducto(int(productoSelected[0]))
        self.producto.setNombre(str(productoSelected[1]))
        self.producto.setCantidad(int(productoSelected[2]))
        self.producto.setCantidadMinima(int(productoSelected[3]))

        self.winNot.btnDesactivar.setEnabled(True)

    def close(self):
        alert = QDialog()
        confirm  = QMessageBox.question(alert, "Mensaje", "¿ Desea salir de la ventana de notificaciones ?", QMessageBox.Yes,
             QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.winNot.close()

    def desactivarProducto(self):
        self.conexionGeneral.changeStateProduct(self.producto)
        self.winNot.btnDesactivar.setEnabled(False)
        self.cargarTabla()

