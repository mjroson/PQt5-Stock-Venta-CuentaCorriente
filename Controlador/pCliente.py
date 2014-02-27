#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Modelo.cliente import Cliente
from Componentes.tableModel import MyTableModel
from PyQt5.QtWidgets import QTableView, QAbstractItemView
from Conexion.conexionCliente import conexionCliente
from Modelo.direccion import Direccion
from Conexion.conexionTelefono import conexionTelefono
from Modelo.telefono import Telefono
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.QtWidgets import QTableWidgetItem

class PestaniaCliente():

    def __init__(self, winPrincipal):
        self.winPrincipal = winPrincipal
        self.cliente = Cliente()
        self.conexionCliente = conexionCliente()
        self.conexionTelefono = conexionTelefono()

        self.listTelefonosInit = []

        self.estado = ""
        self.direccion = Direccion()

        self.configInit()


    def configInit(self):
        #Configurando botones Generales
        self.winPrincipal.btnAgregar_c.clicked.connect(self.onClickAgregar_c)
        self.winPrincipal.btnGuardar_c.clicked.connect(self.onClickGuardar_c)
        self.winPrincipal.btnBorrar_c.clicked.connect(self.onClickBorrar_c)
        self.winPrincipal.btnModificar_c.clicked.connect(self.onClickModificar_c)

        #Configurando botones ABM telefono
        self.winPrincipal.btnSumarTelefono_c.clicked.connect(self.onClickSumarTelefono)
        self.winPrincipal.btnRestarTelefono_c.clicked.connect(self.onClickRestarTelefono)
        self.winPrincipal.btnCancelarTelefono_c.clicked.connect(self.onClickCancelarTelefono)
        self.winPrincipal.btnCancelarTelefono_c.setVisible(False)
        self.winPrincipal.btnRestarTelefono_c.setEnabled(False)

        #configurando botones tipo telefono
        self.winPrincipal.btnTelefono_c.clicked.connect(self.onClickTelefono)
        self.winPrincipal.btnCelular_c.clicked.connect(self.onClickCelular)
        self.winPrincipal.btnFax_c.clicked.connect(self.onClickFax)


        self.winPrincipal.txtFilterClientes_c.returnPressed.connect(self.search)

        #Seteando model y propiedades a la tabla
        self.winPrincipal.tvClientes_c.setSortingEnabled(True)
        self.winPrincipal.tvClientes_c.setMouseTracking(True)
        self.winPrincipal.tvClientes_c.setSelectionBehavior(QAbstractItemView.SelectRows)


        #Seteando proiedades de la tabla telefono
        self.winPrincipal.tvTelefonos_c.setSortingEnabled(True)
        self.winPrincipal.tvTelefonos_c.setMouseTracking(True)
        self.winPrincipal.tvTelefonos_c.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.winPrincipal.txtFilterClientes_c.setFocus(True)

    def finish(self):
        self.winPrincipal.btnAgregar_c.disconnect()
        self.winPrincipal.btnBorrar_c.disconnect()
        self.winPrincipal.btnModificar_c.disconnect()
        self.winPrincipal.btnGuardar_c.disconnect()

        self.winPrincipal.btnCancelarTelefono_c.disconnect()
        self.winPrincipal.btnSumarTelefono_c.disconnect()
        self.winPrincipal.btnRestarTelefono_c.disconnect()

        self.winPrincipal.btnCelular_c.disconnect()
        self.winPrincipal.btnFax_c.disconnect()
        self.winPrincipal.btnTelefono_c.disconnect()

        self.winPrincipal.tvTelefonos_c.disconnect()
        self.winPrincipal.tvClientes_c.disconnect()


    def search(self):
        if self.winPrincipal.txtFilterClientes_c.hasFocus() is True:
            self.cargarTabla()


    def onClickAgregar_c(self):
        self.estado = 'AGREGAR'
        self.validarBotones(button='AGREGAR')


    def onClickGuardar_c(self):
        validar = self.validar()

        if validar != "":
            print(validar)
            alert = QDialog()
            QMessageBox.information(alert,"ERROR", validar)
        else:
            self.cliente.setApellido(self.winPrincipal.txtApellido_c.text())
            self.cliente.setNombre(self.winPrincipal.txtNombre_c.text())
            self.direccion.setDireccion(self.winPrincipal.txtDireccion_c.text())
            self.cliente.setEmail(self.winPrincipal.txtEmail_c.text())

            if self.winPrincipal.txtDDpto_c.text() != "":
                self.direccion.setDpto(str(self.winPrincipal.txtDDpto_c.text()))
            else:
                self.direccion.setDpto("")
            if self.winPrincipal.txtDNumero_c.text() != "":
                self.direccion.setNumero(int(self.winPrincipal.txtDNumero_c.text()))
            else:
                self.direccion.setNumero(0)
            if self.winPrincipal.txtDPiso_c.text() != "":
                self.direccion.setPiso(int(self.winPrincipal.txtDPiso_c.text()))
            else:
                self.direccion.setPiso(0)
            self.cliente.setDireccion(self.direccion)

            if self.winPrincipal.cbEstado_c.currentText() == 'ACTIVO':
                self.cliente.setEstado(1)
            else:
                self.cliente.setEstado(0)

            if self.estado == 'AGREGAR':
                self.insertCliente()
                self.insertTelefono()
            elif self.estado == 'MODIFICAR':
                self.modificarCliente()
                self.updateTelefono()

            self.validarBotones(button='GUARDAR')


    def onClickModificar_c(self):
        self.estado = 'MODIFICAR'
        self.validarBotones(button='MODIFICAR')


    def onClickBorrar_c(self):
        if self.winPrincipal.btnGuardar_c.isEnabled() != True:
            self.conexionCliente.borrarCliente(self.cliente)
            self.cargarTabla()

        self.validarBotones(button='BORRAR')


    def cargarTabla(self):
        parameter = self.winPrincipal.txtFilterClientes_c.text()
        typeParameter = ''

        if self.winPrincipal.cbFilterClientes_c.currentText() == 'Apellido':
            typeParameter = 'cli.apellido'
        else:
            typeParameter = 'p.nombre'

        parameterState = 1
        if self.winPrincipal.cbInactivo_c.isChecked() is True:
            parameterState = 0

        listaClientes = self.conexionCliente.selectCliente(typeParameter, parameter, parameterState)

        if len(listaClientes) > 0:
            header = ['ID','Apellido','Nombre','Email','Direccion', 'N°', 'Piso', 'Dpto', 'iddir', 'idper', 'Estado']
            self.tablaModel = MyTableModel(self.winPrincipal.tvClientes_c, listaClientes, header)
            self.winPrincipal.tvClientes_c.setModel(self.tablaModel)
            self.winPrincipal.tvClientes_c.selectionModel().currentChanged.connect(self.changeSelectedTable)


            self.winPrincipal.tvClientes_c.setColumnHidden(0, True)
            self.winPrincipal.tvClientes_c.setColumnWidth(1, 208)
            self.winPrincipal.tvClientes_c.setColumnWidth(2, 220)
            self.winPrincipal.tvClientes_c.setColumnWidth(3, 280)
            self.winPrincipal.tvClientes_c.setColumnWidth(4, 364)
            self.winPrincipal.tvClientes_c.setColumnWidth(5, 50)
            self.winPrincipal.tvClientes_c.setColumnHidden(6, True)
            self.winPrincipal.tvClientes_c.setColumnHidden(7, True)
            self.winPrincipal.tvClientes_c.setColumnHidden(8, True)
            self.winPrincipal.tvClientes_c.setColumnHidden(9, True)
            self.winPrincipal.tvClientes_c.setColumnHidden(10, True)
        else:
            self.winPrincipal.tvClientes_c.setModel(None)


    def changeSelectedTable(self, selected, deselected):

            clienteList = selected.model().mylist
            clienteSelected = clienteList[selected.row()]
            self.cliente = Cliente()
            self.direccion = Direccion()
            self.cliente.setIdCliente(int(clienteSelected[0]))
            self.cliente.setApellido(clienteSelected[1])
            self.cliente.setNombre(clienteSelected[2])
            self.cliente.setEmail(clienteSelected[3])
            self.direccion = Direccion()
            self.direccion.setDireccion(clienteSelected[4])

            if clienteSelected[5] != None:
                self.direccion.setNumero(int(clienteSelected[5]))

            if clienteSelected[6] != None:
                self.direccion.setPiso(int(clienteSelected[6]))

            if clienteSelected[7] != None:
                self.direccion.setDpto(clienteSelected[7])

            self.direccion.setIdDireccion(int(clienteSelected[8]))
            self.cliente.setDireccion(self.direccion)

            self.cliente.setIdPersona(clienteSelected[9])

            self.winPrincipal.tvClientes_c.setRowHeight(deselected.row(), 28)
            self.winPrincipal.tvClientes_c.setRowHeight(selected.row(), 45)

            self.cliente.setEstado(int(clienteSelected[10]))

            self.setCampos()
            self.winPrincipal.btnModificar_c.setEnabled(True)
            self.winPrincipal.btnBorrar_c.setEnabled(True)
            self.winPrincipal.tvTelefonos_c.setModel(None)
            self.cargarTablaTelefono()


    def validarBotones(self, button):
        if button == 'AGREGAR' :
            self.winPrincipal.wDatosCliente.setEnabled(True)
            self.winPrincipal.btnBorrar_c.setEnabled(True)
            self.winPrincipal.btnBorrar_c.setText('CANCELAR')
            self.winPrincipal.btnGuardar_c.setEnabled(True)
            self.winPrincipal.btnModificar_c.setEnabled(False)
            self.winPrincipal.btnAgregar_c.setEnabled(False)
            self.winPrincipal.tvClientes_c.setEnabled(False)
            self.limpiarCampos()

        elif button=='GUARDAR':
            self.winPrincipal.btnModificar_c.setEnabled(False)
            self.winPrincipal.btnAgregar_c.setEnabled(True)
            self.winPrincipal.btnGuardar_c.setEnabled(False)
            self.winPrincipal.btnBorrar_c.setText('BORRAR')
            self.winPrincipal.btnBorrar_c.setEnabled(False)
            self.winPrincipal.tvClientes_c.setEnabled(True)
            self.winPrincipal.wDatosCliente.setEnabled(False)
            self.limpiarCampos()

        elif button == 'MODIFICAR':
            self.winPrincipal.btnModificar_c.setEnabled(False)
            self.winPrincipal.btnAgregar_c.setEnabled(False)
            self.winPrincipal.btnGuardar_c.setEnabled(True)
            self.winPrincipal.btnBorrar_c.setText('Cancelar')
            self.winPrincipal.btnBorrar_c.setEnabled(True)
            self.winPrincipal.tvClientes_c.setEnabled(False)
            self.winPrincipal.wDatosCliente.setEnabled(True)

        elif button=='BORRAR':
            self.winPrincipal.btnModificar_c.setEnabled(False)
            self.winPrincipal.btnAgregar_c.setEnabled(True)
            self.winPrincipal.btnGuardar_c.setEnabled(False)
            self.winPrincipal.btnBorrar_c.setText('BORRAR')
            self.winPrincipal.btnBorrar_c.setEnabled(False)
            self.winPrincipal.tvClientes_c.setEnabled(True)
            self.winPrincipal.wDatosCliente.setEnabled(False)
            self.limpiarCampos()


    def insertCliente(self):
        if self.cliente.getApellido() != '':
            self.conexionCliente.insertarCliente(cliente=self.cliente)
            self.cargarTabla()


    def modificarCliente(self):
            self.conexionCliente.modificarCliente(self.cliente)
            self.cargarTabla()


    def limpiarCampos(self):
        self.winPrincipal.txtApellido_c.setText('')
        self.winPrincipal.txtNombre_c.setText('')
        self.winPrincipal.txtDireccion_c.setText('')
        self.winPrincipal.txtDNumero_c.setText('')
        self.winPrincipal.txtDPiso_c.setText('')
        self.winPrincipal.txtDDpto_c.setText('')
        self.winPrincipal.txtEmail_c.setText('')
        self.winPrincipal.tvTelefonos_c.setModel(None)
        self.winPrincipal.cbEstado_c.setCurrentIndex(0)
        self.winPrincipal.txtFilterClientes_c.setText('')
        self.winPrincipal.tvClientes_c.setModel(None)

        self.winPrincipal.txtFilterClientes_c.setFocus(True)


    def setCampos(self):
        self.winPrincipal.txtApellido_c.setText(self.cliente.getApellido())
        self.winPrincipal.txtNombre_c.setText(self.cliente.getNombre())
        self.winPrincipal.txtEmail_c.setText(self.cliente.getEmail())

        self.winPrincipal.txtDireccion_c.setText(self.cliente.getDireccion().getDireccion())
        
        if self.cliente.getDireccion().getNumero() != None:
            self.winPrincipal.txtDNumero_c.setText(str(self.cliente.getDireccion().getNumero()))
        else:
            self.winPrincipal.txtDNumero_c.setText('')            
        
        if self.cliente.getDireccion().getPiso() != None:
            self.winPrincipal.txtDPiso_c.setText(str(self.cliente.getDireccion().getPiso()))
        else:
            self.winPrincipal.txtDPiso_c.setText('')

        if self.cliente.getDireccion().getDpto() != None:
            self.winPrincipal.txtDDpto_c.setText(self.cliente.getDireccion().getDpto())
        else:
            self.winPrincipal.txtDDpto_c.setText('')

        if self.cliente.getEstado() == 1:
            self.winPrincipal.cbEstado_c.setCurrentIndex(0)
        else:
            self.winPrincipal.cbEstado_c.setCurrentIndex(1)

    def validar(self):
        mensaje = ''
        if self.winPrincipal.txtNombre_c.text() == '':
            mensaje = "Falta ingresar un Nombre"
        elif self.winPrincipal.txtApellido_c.text() == '':
            mensaje = "Falta ingresar Apellido"
        elif self.winPrincipal.txtDireccion_c.text() == '':
            mensaje = "Falta ingresar una Direccion"
        elif self.winPrincipal.txtDNumero_c.text() == '':
            mensaje = "Falta ingresar un N° de Direccion"

        return mensaje


    def cargarTablaTelefono(self):
        self.listTelefonosInit = self.conexionTelefono.selectTelefono(self.cliente)
        if len(self.listTelefonosInit) >0:
            header = ['ID', 'Numero', 'TIPO']
            tableModel = MyTableModel(self.winPrincipal, self.listTelefonosInit, header)
            self.winPrincipal.tvTelefonos_c.setModel(tableModel)
            self.winPrincipal.tvTelefonos_c.selectionModel().currentChanged.connect(self.changeSelectedTableTel)

            self.winPrincipal.tvTelefonos_c.setColumnHidden(0, True)
            self.winPrincipal.tvTelefonos_c.setColumnWidth(1, 36)
            self.winPrincipal.tvTelefonos_c.setColumnWidth(2, 175)

            for r in range(0, len(self.listTelefonosInit)):
                self.winPrincipal.tvTelefonos_c.setRowHidden(r, False)


    def changeSelectedTableTel(self, selected, deselected):
        listTelefonos = selected.model().mylist
        self.telefonoSelected = ()
        self.telefonoSelected = listTelefonos[selected.row()]

        self.telefonoSelectedRow = selected.row()
        self.winPrincipal.txtTelefono_c.setText(str(self.telefonoSelected[2]))

        self.setTipoTelefono(str(self.telefonoSelected[1]))
        self.winPrincipal.btnCancelarTelefono_c.setVisible(True)
        self.winPrincipal.btnRestarTelefono_c.setEnabled(True)
        self.winPrincipal.tvTelefonos_c.setEnabled(False)

        self.winPrincipal.btnGuardar_c.setEnabled(False)
        self.winPrincipal.btnBorrar_c.setEnabled(False)


    def updateTelefono(self):

        listTelefono = []
        if self.winPrincipal.tvTelefonos_c.model() != None and \
                        len(self.winPrincipal.tvTelefonos_c.model().mylist) > 0:
            listTelefono = list(self.winPrincipal.tvTelefonos_c.model().mylist).copy()

            estado = ''
            telNew = Telefono()
            if len(listTelefono) > 0:
                if len(self.listTelefonosInit) > 0:

                    listTelInit = list(self.listTelefonosInit)
                    parche = (listTelefono[0][0], listTelefono[0][1], str(listTelefono[0][2]))
                    listTelefono[0] = parche
                    #Recorre la lista de telefono inicial
                    for telInit in listTelInit:
                        #recorre la lista de telefonos nueva
                        for tel in listTelefono:
                            telNew.setIdPersona(self.cliente.getIdPersona())
                            telNew.setIdTelefono(tel[0])
                            telNew.setTipo(tel[1])
                            if tel[2] == "":
                                estado = 'DEL'
                                break
                            else:
                                telNew.setTelefono(tel[2])

                            if tel[0] == 0:
                                estado = 'INS'
                                break

                            if telInit[0] == tel[0]:
                                if telInit[1] != tel[1] or telInit[2] != tel[2]:
                                    estado = 'UPD'
                                    break

                        if estado == 'UPD':
                            self.conexionTelefono.modificarTelefono(telNew)
                        elif estado == "INS":
                            self.conexionTelefono.insertarTelefono(telNew)
                        elif estado == 'DEL':
                            self.conexionTelefono.borrarTelefono(telNew)
                #Si la lista de telefono inicial es cero
                else:
                    #recorre la lista de telefonos nueva para agregarlos a todos
                    for telN in listTelefono:
                        if telN[2] != '':
                            telNew = Telefono()
                            telNew.setIdPersona(self.cliente.getIdPersona())
                            telNew.setIdTelefono(telN[0])
                            telNew.setTipo(telN[1])
                            telNew.setTelefono(telN[2])
                            self.conexionTelefono.insertarTelefono(telNew)


    def insertTelefono(self):

        listTelefonosNew = []
        tel = self.winPrincipal.tvTelefonos_c.model()

        listTelefonosNew = list(self.winPrincipal.tvTelefonos_c.model().mylist).copy()

        if len(listTelefonosNew) > 0:
            self.conexionTelefono.insertTelefonoInit(listTelefonosNew)


    def onClickCancelarTelefono(self):
        self.winPrincipal.btnCancelarTelefono_c.setVisible(False)
        self.winPrincipal.txtTelefono_c.setText('')

        self.winPrincipal.btnRestarTelefono_c.setEnabled(False)
        self.winPrincipal.tvTelefonos_c.clearSelection()
        self.winPrincipal.tvTelefonos_c.setEnabled(True)

        self.winPrincipal.btnGuardar_c.setEnabled(True)
        self.winPrincipal.btnBorrar_c.setEnabled(True)


    def onClickSumarTelefono(self):
        numTelefono = self.winPrincipal.txtTelefono_c.text()

        if numTelefono.isdigit() == True:
            if self.winPrincipal.btnCancelarTelefono_c.isVisible() is True:
                self.updateTelefonoTabla()
            else:
                self.insertTelefonoTabla()

            self.winPrincipal.tvTelefonos_c.clearSelection()
            self.winPrincipal.btnRestarTelefono_c.setEnabled(False)
            self.winPrincipal.btnCancelarTelefono_c.setVisible(False)
            self.winPrincipal.txtTelefono_c.setText('')
            self.winPrincipal.tvTelefonos_c.setEnabled(True)

            self.winPrincipal.btnGuardar_c.setEnabled(True)
        else:
            alert = QDialog()
            QMessageBox.information(alert,"ERROR", "El numero de telefono no es valido.")


    def onClickRestarTelefono(self):
        listTabTel = []
        #listTabTel = list(self.winPrincipal.tvTelefonos_c.model().mylist).copy()
        #tipoTel = str(self.getTipoTelefono())
        listTelefonosNew = []

        listTabTel = list(self.winPrincipal.tvTelefonos_c.model().mylist).copy()

        header = ['Id', 'Tipo', 'Numero']
        telDel = [self.telefonoSelected[0], self.telefonoSelected[1], '']
        listTabTel[self.telefonoSelectedRow] = telDel
        tableTelModel = MyTableModel(self.winPrincipal, listTabTel, header)
        self.winPrincipal.tvTelefonos_c.setModel(tableTelModel)
        self.winPrincipal.tvTelefonos_c.selectionModel().currentChanged.connect(self.changeSelectedTableTel)
        self.winPrincipal.tvTelefonos_c.setRowHidden(self.telefonoSelectedRow, True)

        self.winPrincipal.btnCancelarTelefono_c.setVisible(False)
        self.winPrincipal.txtTelefono_c.setText('')
        self.winPrincipal.btnRestarTelefono_c.setEnabled(False)
        self.winPrincipal.tvTelefonos_c.setEnabled(True)

        self.winPrincipal.btnGuardar_c.setEnabled(True)
        self.winPrincipal.btnBorrar_c.setEnabled(True)


    def onClickTelefono(self):
        self.changeTipoTelefono(button='TEL')


    def onClickCelular(self):
        self.changeTipoTelefono(button='CEL')


    def onClickFax(self):
        self.changeTipoTelefono(button='FAX')


    def changeTipoTelefono(self, button):

        if button == 'TEL':
            self.winPrincipal.btnTelefono_c.setEnabled(False)
            self.winPrincipal.btnCelular_c.setEnabled(True)
            self.winPrincipal.btnFax_c.setEnabled(True)
        elif button == 'CEL':
            self.winPrincipal.btnTelefono_c.setEnabled(True)
            self.winPrincipal.btnCelular_c.setEnabled(False)
            self.winPrincipal.btnFax_c.setEnabled(True)
        elif button == 'FAX':
            self.winPrincipal.btnTelefono_c.setEnabled(True)
            self.winPrincipal.btnCelular_c.setEnabled(True)
            self.winPrincipal.btnFax_c.setEnabled(False)


    def setTipoTelefono(self, tipoTelefono):

        if tipoTelefono == 'TEL':
            self.winPrincipal.btnTelefono_c.setEnabled(False)
            self.winPrincipal.btnCelular_c.setEnabled(True)
            self.winPrincipal.btnFax_c.setEnabled(True)
        elif tipoTelefono == 'CEL':
            self.winPrincipal.btnTelefono_c.setEnabled(True)
            self.winPrincipal.btnCelular_c.setEnabled(False)
            self.winPrincipal.btnFax_c.setEnabled(True)
        elif tipoTelefono == 'FAX':
            self.winPrincipal.btnTelefono_c.setEnabled(True)
            self.winPrincipal.btnCelular_c.setEnabled(True)
            self.winPrincipal.btnFax_c.setEnabled(False)


    def getTipoTelefono(self):

        if self.winPrincipal.btnTelefono_c.isEnabled() != True:
            return 'TEL'
        elif self.winPrincipal.btnCelular_c.isEnabled() != True:
            return 'CEL'
        elif self.winPrincipal.btnFax_c.isEnabled() != True:
            return 'FAX'


    def insertTelefonoTabla(self):
        numTel = self.winPrincipal.txtTelefono_c.text()
        tipoTel = str(self.getTipoTelefono())

        modelListTelefono = self.winPrincipal.tvTelefonos_c.model()
        header = ['ID', 'Tipo', 'Numero']

        if modelListTelefono is not None:
            listTabTel = list(self.winPrincipal.tvTelefonos_c.model().mylist)

            if len(listTabTel) > 0 or listTabTel is not None:
                tuplaTel = ('0', tipoTel, numTel )
                listTabTel.append(tuplaTel)
                tupleTable = tuple(listTabTel)

                tableModel = MyTableModel(self.winPrincipal, tupleTable , header)
                self.winPrincipal.tvTelefonos_c.setModel(tableModel)
                self.winPrincipal.tvTelefonos_c.selectionModel().currentChanged.connect(self.changeSelectedTableTel)
        else:
            lista = []
            tuplaTel = ('0', tipoTel, numTel )
            lista.append(tuplaTel)

            tableModel = MyTableModel(self.winPrincipal, lista , header)
            self.winPrincipal.tvTelefonos_c.setModel(tableModel)
            self.winPrincipal.tvTelefonos_c.selectionModel().currentChanged.connect(self.changeSelectedTableTel)
            self.winPrincipal.tvTelefonos_c.setColumnHidden(0, True)
            self.winPrincipal.tvTelefonos_c.setColumnWidth(1, 36)
            self.winPrincipal.tvTelefonos_c.setColumnWidth(2, 175)


    def updateTelefonoTabla(self):
        listTabTel = []
        #listTabTel = list(self.winPrincipal.tvTelefonos_c.model().mylist).copy()
        tipoTel = str(self.getTipoTelefono())
        listTelefonosNew = []
        #prob = self.winPrincipal.tvTelefonos_c.selectionModel()
        #prob1 = self.winPrincipal.tvTelefonos_c.model()
        listTabTel = list(self.winPrincipal.tvTelefonos_c.model().mylist).copy()
        """
        for lt in listTabTel:
            if lt[0] == self.telefonoSelected[0]:
                lt = (self.telefonoSelected[0], tipoTel, self.winPrincipal.txtTelefono_c.text())

            listTelefonosNew.append(lt)
        """
        telUpd = (self.telefonoSelected[0], tipoTel, int(self.winPrincipal.txtTelefono_c.text()))
        listTabTel[self.telefonoSelectedRow] = telUpd
        header = ['ID', 'Tipo', 'Numero']
        tableModel = MyTableModel(self.winPrincipal, listTabTel , header)
        self.winPrincipal.tvTelefonos_c.setModel(tableModel)
        self.winPrincipal.tvTelefonos_c.selectionModel().currentChanged.connect(self.changeSelectedTableTel)