from Conexion.conexionTransacciones import ConexionTransacciones
from Modelo.cliente import Cliente
from Modelo.proveedor import Proveedor
from Modelo.producto import Producto
from PyQt5.QtWidgets import QRadioButton
from Componentes.tableModel import MyTableModel
from PyQt5.QtWidgets import QAbstractItemView


class PestaniaPagos():


    def __init__(self, winPrincipal):
        self.conexionTransacciones = ConexionTransacciones()
        self.winPrincipal = winPrincipal
        self.cliente = Cliente()

        self.cargarTabla()
        self.configInit()

    def configInit(self):
        self.winPrincipal.tvCuentaCorriente_pag.setSortingEnabled(True)
        self.winPrincipal.tvCuentaCorriente_pag.setMouseTracking(True)
        self.winPrincipal.tvCuentaCorriente_pag.setSelectionBehavior(QAbstractItemView.SelectRows)

    def cargarTabla(self):
        if self.winPrincipal.cbFilterCliente_t.currentText() == 'Apellido':
            tipoParametro = 'c.apellido'
        elif self.winPrincipal.cbFilterCliente_t.currentText() == 'Email':
            tipoParametro = 'p.email'

        parametro = self.winPrincipal.txtFilterCliente_t.text()
        listaClientes = self.conexionTransacciones.selectClientes(tipoParametro, parametro)

        header = ['ID','Apellido','Nombre','Email']
        tablaModel = MyTableModel(self.winPrincipal.tvCuentaCorriente_pag, listaClientes, header)
        self.winPrincipal.tvCuentaCorriente_pag.setModel(tablaModel)
        #self.winPrincipal.tvCuentaCorriente_pag.selectionModel().currentChanged.connect(self.changeSelectedTable)


        self.winPrincipal.tvCuentaCorriente_pag.setColumnHidden(0, True)
        self.winPrincipal.tvCuentaCorriente_pag.setColumnWidth(1, 230)
        self.winPrincipal.tvCuentaCorriente_pag.setColumnWidth(2, 230)
        self.winPrincipal.tvCuentaCorriente_pag.setColumnWidth(3, 250)