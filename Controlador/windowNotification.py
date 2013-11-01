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

        #self.winNot.show()

        self.cargarTabla()

        self.winNot.btnSalir.clicked.connect(self.close)
        self.winNot.btnDesactivar.clicked.connect(self.desactivarProducto)


        self.winNot.tvDetalle.setSortingEnabled(True)
        self.winNot.tvDetalle.setMouseTracking(True)
        self.winNot.tvDetalle.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.winNot.exec()

        #sys.executable(self.winNot.exec_())


    def cargarTabla(self):
        pass

    def close(self):
        pass

    def desactivarProducto(self):
        pass