#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Modelo.proveedor import Proveedor
from Modelo.persona import Persona
from Conexion.conexionProveedor import conexionProveedor
from PyQt5.QtWidgets import QAbstractItemView, QTableView
from Componentes.tableModel import MyTableModel
from Modelo.direccion import Direccion
from Conexion.conexionTelefono import conexionTelefono
from Modelo.telefono import Telefono
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5 import QtCore, QtGui

class PestaniaProveedor():

    def __init__(self, winPrincipal):
        self.proveedor = Proveedor()
        self.winPrincipal = winPrincipal
        self.conexionProveedor = conexionProveedor()
        self.conexionTelefono = conexionTelefono()
        self.estado = ""
        self.direccion = Direccion()


        self.configInit()


    def configInit(self):
        """
        Configuracion inicial de la pestaña probeedor, setea todas las señales de los botones y carga la tabla
        @return: void
        """
         #Configurando botones Generales
        self.winPrincipal.btnGuardar_prov.clicked.connect(self.onClickGuardar)
        self.winPrincipal.btnAgregar_prov.clicked.connect(self.onClickAgregar)
        self.winPrincipal.btnModificar_prov.clicked.connect(self.onClickModificar)
        self.winPrincipal.btnBorrar_prov.clicked.connect(self.onClickBorrar)

        #Configurando botones ABM telefono
        self.winPrincipal.btnSumarTelefono_prov.clicked.connect(self.onClickSumarTelefono)
        self.winPrincipal.btnRestarTelefono_prov.clicked.connect(self.onClickRestarTelefono)
        self.winPrincipal.btnCancelarTelefono_prov.clicked.connect(self.onClickCancelarTelefono)
        self.winPrincipal.btnCancelarTelefono_prov.setVisible(False)
        self.winPrincipal.btnRestarTelefono_prov.setEnabled(False)

        #configurando botones tipo telefono
        self.winPrincipal.btnTelefono_prov.clicked.connect(self.onClickTelefono)
        self.winPrincipal.btnCelular_prov.clicked.connect(self.onClickCelular)
        self.winPrincipal.btnFax_prov.clicked.connect(self.onClickFax)

        self.winPrincipal.txtFilterProveedores_prov.returnPressed.connect(self.search)

        #Seteando model y propieades de la tabla
        self.winPrincipal.tvProveedores_prov.setSortingEnabled(True)
        self.winPrincipal.tvProveedores_prov.setMouseTracking(True)
        self.winPrincipal.tvProveedores_prov.setSelectionBehavior(QAbstractItemView.SelectRows)

        #Seteando proiedades de la tabla telefono
        self.winPrincipal.tvTelefonos_prov.setSortingEnabled(True)
        self.winPrincipal.tvTelefonos_prov.setMouseTracking(True)
        self.winPrincipal.tvTelefonos_prov.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.winPrincipal.txtFilterProveedores_prov.setFocus(True)


    def finish(self):
        self.winPrincipal.btnAgregar_prov.disconnect()
        self.winPrincipal.btnBorrar_prov.disconnect()
        self.winPrincipal.btnModificar_prov.disconnect()
        self.winPrincipal.btnGuardar_prov.disconnect()

        self.winPrincipal.btnCancelarTelefono_prov.disconnect()
        self.winPrincipal.btnSumarTelefono_prov.disconnect()
        self.winPrincipal.btnRestarTelefono_prov.disconnect()

        self.winPrincipal.btnCelular_prov.disconnect()
        self.winPrincipal.btnFax_prov.disconnect()
        self.winPrincipal.btnTelefono_prov.disconnect()

        self.winPrincipal.tvTelefonos_prov.disconnect()
        self.winPrincipal.tvProveedores_prov.disconnect()

    def search(self):
        if self.winPrincipal.txtFilterProveedores_prov.hasFocus() is True:
            self.cargarTabla()

    def onClickAgregar(self):
        self.estado = 'AGREGAR'
        self.validarBotones(button='AGREGAR')


    def onClickGuardar(self):
        validar = self.validar()

        if validar != "":
            print(validar)
            alert = QDialog()
            QMessageBox.information(alert,"ERROR", validar)
        else:
            self.proveedor.setDescripcion(str(self.winPrincipal.txtDescripcion_prov.text()))
            self.proveedor.setWeb(str(self.winPrincipal.txtWeb_prov.text()))
            self.proveedor.setEmail(str(self.winPrincipal.txtEmail_prov.text()))
            self.proveedor.setNombre(str(self.winPrincipal.txtNombre_prov.text()))
            self.direccion.setDireccion(str(self.winPrincipal.txtDireccion_prov.text()))
            if self.winPrincipal.txtDDpto_prov.text() != "":
                self.direccion.setDpto(str(self.winPrincipal.txtDDpto_prov.text()))
            else:
                self.direccion.setDpto("")
            if self.winPrincipal.txtDNumero_prov.text() != "":
                self.direccion.setNumero(int(self.winPrincipal.txtDNumero_prov.text()))
            else:
                self.direccion.setNumero(0)
            if self.winPrincipal.txtDPiso_prov.text() != "":
                self.direccion.setPiso(int(self.winPrincipal.txtDPiso_prov.text()))
            else:
                self.direccion.setPiso(0)

            self.proveedor.setDireccion(self.direccion)

            if self.winPrincipal.cbEstado_prov.currentText() == 'ACTIVO':
                self.proveedor.setEstado(1)
            else:
                self.proveedor.setEstado(0)

            self.validarBotones(button='GUARDAR')

            if self.estado == 'AGREGAR':
                self.insertProveedor()
                self.insertTelefono()
            elif self.estado == 'MODIFICAR':
                self.modificarProveedor()
                self.updateTelefono()


    def onClickModificar(self):
        self.estado = 'MODIFICAR'
        self.validarBotones(button='MODIFICAR')


    def onClickBorrar(self):

        if self.winPrincipal.btnGuardar_prov.isEnabled() != True:
            self.conexionProveedor.borrarProveedor(self.proveedor)
            self.cargarTabla()

        self.validarBotones(button='BORRAR')


    def cargarTabla(self):
        parameter = self.winPrincipal.txtFilterProveedores_prov.text()
        typeParameter = ''

        if self.winPrincipal.cbFilterProveedores_prov.currentText() == 'Descripcion':
            typeParameter = 'prov.descripcion'
        else:
            typeParameter = 'p.nombre'

        parameterState = 1
        if self.winPrincipal.cbInactivo_prov.isChecked() is True:
            parameterState = 0

        listProveedores = self.conexionProveedor.selectProveedor(typeParameter, parameter, parameterState)

        if len(listProveedores) > 0:
            header = ['ID', 'Descripcion', 'Nombre', 'Email', 'Web', 'Direccion', 'N°', 'P', 'D', 'idper', 'iddir', 'Estado' ]
            tableModel = MyTableModel(self.winPrincipal.tvProveedores_prov, listProveedores, header)
            self.winPrincipal.tvProveedores_prov.setModel(tableModel)
            self.winPrincipal.tvProveedores_prov.selectionModel().currentChanged.connect(self.changeSelectedTable)

            self.winPrincipal.tvProveedores_prov.setColumnHidden(0, True)
            self.winPrincipal.tvProveedores_prov.setColumnWidth(1, 190)

            self.winPrincipal.tvProveedores_prov.setColumnWidth(2, 190)
            self.winPrincipal.tvProveedores_prov.setColumnWidth(3, 263)
            self.winPrincipal.tvProveedores_prov.setColumnWidth(4, 240)


            self.winPrincipal.tvProveedores_prov.setColumnWidth(5, 200)
            self.winPrincipal.tvProveedores_prov.setColumnWidth(6, 50)
            self.winPrincipal.tvProveedores_prov.setColumnHidden(7, True)
            self.winPrincipal.tvProveedores_prov.setColumnHidden(8, True)
            self.winPrincipal.tvProveedores_prov.setColumnHidden(9, True)
            self.winPrincipal.tvProveedores_prov.setColumnHidden(10, True)
            self.winPrincipal.tvProveedores_prov.setColumnHidden(11, True)
        else:
            self.winPrincipal.tvProveedores_prov.setModel(None)


    def changeSelectedTable(self, selected, deselected):
        proveedorList = selected.model().mylist
        proveedorSelected = proveedorList[selected.row()]
        self.proveedor = Proveedor()
        self.direccion = Direccion()
        self.proveedor.setIdProveedor(int(proveedorSelected[0]))
        self.proveedor.setDescripcion(str(proveedorSelected[1]))
        self.proveedor.setNombre(str(proveedorSelected[2]))
        self.proveedor.setEmail(str(proveedorSelected[3]))
        self.proveedor.setWeb(str(proveedorSelected[4]))

        self.direccion.setDireccion(str(proveedorSelected[5]))
        if proveedorSelected[6] != None:
            self.direccion.setNumero(int(proveedorSelected[6]))

        if proveedorSelected[7] != None:
            self.direccion.setPiso(int(proveedorSelected[7]))

        if proveedorSelected[8] != None:
            self.direccion.setDpto(proveedorSelected[8])

        self.direccion.setIdDireccion(int(proveedorSelected[10]))
        self.proveedor.setDireccion(self.direccion)

        self.proveedor.setIdPersona(int(proveedorSelected[9]))

        self.proveedor.setEstado(int(proveedorSelected[11]))

        self.winPrincipal.tvProveedores_prov.setRowHeight(deselected.row(), 28)
        self.winPrincipal.tvProveedores_prov.setRowHeight(selected.row(), 45)

        self.setCampos()
        self.winPrincipal.btnModificar_prov.setEnabled(True)
        self.winPrincipal.btnBorrar_prov.setEnabled(True)
        self.winPrincipal.tvTelefonos_prov.setModel(None)
        self.cargarTablaTelefono()


    def validarBotones(self, button):

        if button == 'AGREGAR':
            self.winPrincipal.btnAgregar_prov.setEnabled(False)
            self.winPrincipal.btnModificar_prov.setEnabled(False)
            self.winPrincipal.btnGuardar_prov.setEnabled(True)
            self.winPrincipal.btnBorrar_prov.setEnabled(True)
            self.winPrincipal.tvProveedores_prov.setEnabled(False)
            self.winPrincipal.wDatosProveedor.setEnabled(True)
            self.winPrincipal.btnBorrar_prov.setText('CANCELAR')
            self.limpiarCampos()
        elif button == 'GUARDAR':
            self.winPrincipal.btnAgregar_prov.setEnabled(True)
            self.winPrincipal.btnModificar_prov.setEnabled(False)
            self.winPrincipal.btnGuardar_prov.setEnabled(False)
            self.winPrincipal.btnBorrar_prov.setEnabled(False)
            self.winPrincipal.tvProveedores_prov.setEnabled(True)
            self.winPrincipal.wDatosProveedor.setEnabled(False)
            self.winPrincipal.btnBorrar_prov.setText('BORRAR')
            self.limpiarCampos()
        elif button == 'MODIFICAR':
            self.winPrincipal.btnAgregar_prov.setEnabled(False)
            self.winPrincipal.btnModificar_prov.setEnabled(False)
            self.winPrincipal.btnGuardar_prov.setEnabled(True)
            self.winPrincipal.btnBorrar_prov.setEnabled(True)
            self.winPrincipal.tvProveedores_prov.setEnabled(False)
            self.winPrincipal.wDatosProveedor.setEnabled(True)
            self.winPrincipal.btnBorrar_prov.setText('CANCELAR')
        elif button == 'BORRAR':
            self.winPrincipal.btnAgregar_prov.setEnabled(True)
            self.winPrincipal.btnModificar_prov.setEnabled(False)
            self.winPrincipal.btnGuardar_prov.setEnabled(False)
            self.winPrincipal.btnBorrar_prov.setEnabled(False)
            self.winPrincipal.tvProveedores_prov.setEnabled(True)
            self.winPrincipal.wDatosProveedor.setEnabled(False)
            self.winPrincipal.btnBorrar_prov.setText('BORRAR')
            self.limpiarCampos()


    def insertProveedor(self):
        self.conexionProveedor.insertarProveedor(proveedor=self.proveedor)
        self.cargarTabla()


    def modificarProveedor(self):
        self.conexionProveedor.modificarProveedor(proveedor=self.proveedor)
        self.cargarTabla()


    def limpiarCampos(self):
        self.winPrincipal.txtNombre_prov.setText('')
        self.winPrincipal.txtDescripcion_prov.setText('')
        self.winPrincipal.txtEmail_prov.setText('')
        self.winPrincipal.txtDireccion_prov.setText('')
        self.winPrincipal.txtDNumero_prov.setText('')
        self.winPrincipal.txtDPiso_prov.setText('')
        self.winPrincipal.txtDDpto_prov.setText('')
        self.winPrincipal.txtWeb_prov.setText('')
        self.winPrincipal.tvTelefonos_prov.setModel(None)
        self.winPrincipal.cbEstado_prov.setCurrentIndex(0)
        self.winPrincipal.txtFilterProveedores_prov.setText('')
        self.winPrincipal.tvProveedores_prov.setModel(None)

        self.winPrincipal.txtFilterProveedores_prov.setFocus(True)


    def setCampos(self):
        self.winPrincipal.txtDescripcion_prov.setText(str(self.proveedor.getDescripcion()))
        self.winPrincipal.txtEmail_prov.setText(str(self.proveedor.getEmail()))
        self.winPrincipal.txtNombre_prov.setText(str(self.proveedor.getNombre()))
        self.winPrincipal.txtWeb_prov.setText(str(self.proveedor.getWeb()))

        self.winPrincipal.txtDireccion_prov.setText(str(self.proveedor.getDireccion().getDireccion()))

        if self.proveedor.getDireccion().getNumero() is not None:
            self.winPrincipal.txtDNumero_prov.setText(str(self.proveedor.getDireccion().getNumero()))
        else:
            self.winPrincipal.txtDNumero_prov.setText('')

        if self.proveedor.getDireccion().getPiso() is not None:
            self.winPrincipal.txtDPiso_prov.setText(str(self.proveedor.getDireccion().getPiso()))
        else:
            self.winPrincipal.txtDPiso_prov.setText('')

        if self.proveedor.getDireccion().getDpto() is not None:
            self.winPrincipal.txtDDpto_prov.setText(self.proveedor.getDireccion().getDpto())
        else:
            self.winPrincipal.txtDDpto_prov.setText('')

        if self.proveedor.getEstado() == 1:
            self.winPrincipal.cbEstado_prov.setCurrentIndex(0)
        else:
            self.winPrincipal.cbEstado_prov.setCurrentIndex(1)


    def validar(self):
        mensaje = ''
        if self.winPrincipal.txtNombre_prov.text() == '':
            mensaje = "Falta ingresar un Nombre"
        elif self.winPrincipal.txtDescripcion_prov.text() == '':
            mensaje = "Falta ingresa la descripcion"
        elif self.winPrincipal.txtDireccion_prov.text() == '':
            mensaje = "Falta ingresar una Direccion"
        elif self.winPrincipal.txtDNumero_prov.text() == '':
            mensaje = "Falta ingresar un N° de Direccion"

        return mensaje


    def cargarTablaTelefono(self):
        self.listTelefonosInit = self.conexionTelefono.selectTelefono(self.proveedor)
        if len(self.listTelefonosInit) >0:
            header = ['ID', 'Numero', 'TIPO']
            tableModel = MyTableModel(self.winPrincipal, self.listTelefonosInit, header)
            self.winPrincipal.tvTelefonos_prov.setModel(tableModel)
            self.winPrincipal.tvTelefonos_prov.selectionModel().currentChanged.connect(self.changeSelectedTableTel)

            self.winPrincipal.tvTelefonos_prov.setColumnHidden(0, True)
            self.winPrincipal.tvTelefonos_prov.setColumnWidth(1, 36)
            self.winPrincipal.tvTelefonos_prov.setColumnWidth(2, 175)

            for r in range(0, len(self.listTelefonosInit)):
                self.winPrincipal.tvTelefonos_prov.setRowHidden(r, False)


    def changeSelectedTableTel(self, selected, deselected):
        listTelefonos = selected.model().mylist
        self.telefonoSelected = ()
        self.telefonoSelected = listTelefonos[selected.row()]

        self.telefonoSelectedRow = selected.row()
        self.winPrincipal.txtTelefono_prov.setText(str(self.telefonoSelected[2]))

        self.setTipoTelefono(str(self.telefonoSelected[1]))
        self.winPrincipal.btnCancelarTelefono_prov.setVisible(True)
        self.winPrincipal.btnRestarTelefono_prov.setEnabled(True)
        self.winPrincipal.tvTelefonos_prov.setEnabled(False)

        self.winPrincipal.btnGuardar_prov.setEnabled(False)
        self.winPrincipal.btnBorrar_prov.setEnabled(False)


    def updateTelefono(self):

        listTelefono = []
        if self.winPrincipal.tvTelefonos_prov.model() != None and \
                        len(self.winPrincipal.tvTelefonos_prov.model().mylist) > 0:
            listTelefono = list(self.winPrincipal.tvTelefonos_prov.model().mylist).copy()

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
                            telNew.setIdPersona(self.proveedor.getIdPersona())
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
                            telNew.setIdPersona(self.proveedor.getIdPersona())
                            telNew.setIdTelefono(telN[0])
                            telNew.setTipo(telN[1])
                            telNew.setTelefono(telN[2])
                            self.conexionTelefono.insertarTelefono(telNew)


    def insertTelefono(self):

        listTelefonosNew = []
        tel = self.winPrincipal.tvTelefonos_prov.model()

        listTelefonosNew = list(self.winPrincipal.tvTelefonos_prov.model().mylist).copy()

        if len(listTelefonosNew) > 0:
            self.conexionTelefono.insertTelefonoInit(listTelefonosNew)


    def onClickCancelarTelefono(self):
        self.winPrincipal.btnCancelarTelefono_prov.setVisible(False)
        self.winPrincipal.txtTelefono_prov.setText('')

        self.winPrincipal.btnRestarTelefono_prov.setEnabled(False)
        self.winPrincipal.tvTelefonos_prov.clearSelection()
        self.winPrincipal.tvTelefonos_prov.setEnabled(True)

        self.winPrincipal.btnGuardar_prov.setEnabled(True)
        self.winPrincipal.btnBorrar_prov.setEnabled(True)


    def onClickSumarTelefono(self):
        numTelefono = self.winPrincipal.txtTelefono_prov.text()

        if numTelefono.isdigit() == True:
            if self.winPrincipal.btnCancelarTelefono_prov.isVisible() is True:
                self.updateTelefonoTabla()
            else:
                self.insertTelefonoTabla()

            self.winPrincipal.tvTelefonos_prov.clearSelection()
            self.winPrincipal.btnRestarTelefono_prov.setEnabled(False)
            self.winPrincipal.btnCancelarTelefono_prov.setVisible(False)
            self.winPrincipal.txtTelefono_prov.setText('')
            self.winPrincipal.tvTelefonos_prov.setEnabled(True)

            self.winPrincipal.btnGuardar_prov.setEnabled(True)
        else:
            alert = QDialog()
            QMessageBox.information(alert,"ERROR", "El numero de telefono no es valido.")


    def onClickRestarTelefono(self):
        listTabTel = []

        #tipoTel = str(self.getTipoTelefono())
        listTelefonosNew = []

        listTabTel = list(self.winPrincipal.tvTelefonos_prov.model().mylist).copy()

        header = ['Id', 'Tipo', 'Numero']
        telDel = [self.telefonoSelected[0], self.telefonoSelected[1], '']
        listTabTel[self.telefonoSelectedRow] = telDel
        tableTelModel = MyTableModel(self.winPrincipal, listTabTel, header)
        self.winPrincipal.tvTelefonos_prov.setModel(tableTelModel)
        self.winPrincipal.tvTelefonos_prov.selectionModel().currentChanged.connect(self.changeSelectedTableTel)
        self.winPrincipal.tvTelefonos_prov.setRowHidden(self.telefonoSelectedRow, True)

        self.winPrincipal.btnCancelarTelefono_prov.setVisible(False)
        self.winPrincipal.txtTelefono_prov.setText('')
        self.winPrincipal.btnRestarTelefono_prov.setEnabled(False)
        self.winPrincipal.tvTelefonos_prov.setEnabled(True)

        self.winPrincipal.btnGuardar_prov.setEnabled(True)
        self.winPrincipal.btnBorrar_prov.setEnabled(True)


    def onClickTelefono(self):
        self.changeTipoTelefono(button='TEL')


    def onClickCelular(self):
        self.changeTipoTelefono(button='CEL')


    def onClickFax(self):
        self.changeTipoTelefono(button='FAX')


    def changeTipoTelefono(self, button):

        if button == 'TEL':
            self.winPrincipal.btnTelefono_prov.setEnabled(False)
            self.winPrincipal.btnCelular_prov.setEnabled(True)
            self.winPrincipal.btnFax_prov.setEnabled(True)
        elif button == 'CEL':
            self.winPrincipal.btnTelefono_prov.setEnabled(True)
            self.winPrincipal.btnCelular_prov.setEnabled(False)
            self.winPrincipal.btnFax_prov.setEnabled(True)
        elif button == 'FAX':
            self.winPrincipal.btnTelefono_prov.setEnabled(True)
            self.winPrincipal.btnCelular_prov.setEnabled(True)
            self.winPrincipal.btnFax_prov.setEnabled(False)


    def setTipoTelefono(self, tipoTelefono):

        if tipoTelefono == 'TEL':
            self.winPrincipal.btnTelefono_prov.setEnabled(False)
            self.winPrincipal.btnCelular_prov.setEnabled(True)
            self.winPrincipal.btnFax_prov.setEnabled(True)
        elif tipoTelefono == 'CEL':
            self.winPrincipal.btnTelefono_prov.setEnabled(True)
            self.winPrincipal.btnCelular_prov.setEnabled(False)
            self.winPrincipal.btnFax_prov.setEnabled(True)
        elif tipoTelefono == 'FAX':
            self.winPrincipal.btnTelefono_prov.setEnabled(True)
            self.winPrincipal.btnCelular_prov.setEnabled(True)
            self.winPrincipal.btnFax_prov.setEnabled(False)


    def getTipoTelefono(self):

        if self.winPrincipal.btnTelefono_prov.isEnabled() != True:
            return 'TEL'
        elif self.winPrincipal.btnCelular_prov.isEnabled() != True:
            return 'CEL'
        elif self.winPrincipal.btnFax_prov.isEnabled() != True:
            return 'FAX'


    def insertTelefonoTabla(self):
        numTel = self.winPrincipal.txtTelefono_prov.text()
        tipoTel = str(self.getTipoTelefono())

        modelListTelefono = self.winPrincipal.tvTelefonos_prov.model()
        header = ['ID', 'Tipo', 'Numero']

        if modelListTelefono is not None:
            listTabTel = list(self.winPrincipal.tvTelefonos_prov.model().mylist)

            if len(listTabTel) > 0 or listTabTel is not None:
                tuplaTel = ('0', tipoTel, numTel )
                listTabTel.append(tuplaTel)
                tupleTable = tuple(listTabTel)

                tableModel = MyTableModel(self.winPrincipal, tupleTable , header)
                self.winPrincipal.tvTelefonos_prov.setModel(tableModel)
                self.winPrincipal.tvTelefonos_prov.selectionModel().currentChanged.connect(self.changeSelectedTableTel)
        else:
            lista = []
            tuplaTel = ('0', tipoTel, numTel )
            lista.append(tuplaTel)

            tableModel = MyTableModel(self.winPrincipal, lista , header)
            self.winPrincipal.tvTelefonos_prov.setModel(tableModel)
            self.winPrincipal.tvTelefonos_prov.selectionModel().currentChanged.connect(self.changeSelectedTableTel)
            self.winPrincipal.tvTelefonos_prov.setColumnHidden(0, True)
            self.winPrincipal.tvTelefonos_prov.setColumnWidth(1, 36)
            self.winPrincipal.tvTelefonos_prov.setColumnWidth(2, 175)


    def updateTelefonoTabla(self):
        listTabTel = []

        tipoTel = str(self.getTipoTelefono())
        listTelefonosNew = []
        prob = self.winPrincipal.tvTelefonos_prov.selectionModel()
        prob1 = self.winPrincipal.tvTelefonos_prov.model()
        listTabTel = list(self.winPrincipal.tvTelefonos_prov.model().mylist).copy()

        telUpd = (self.telefonoSelected[0], tipoTel, int(self.winPrincipal.txtTelefono_prov.text()))
        listTabTel[self.telefonoSelectedRow] = telUpd
        header = ['ID', 'Tipo', 'Numero']
        tableModel = MyTableModel(self.winPrincipal, listTabTel , header)
        self.winPrincipal.tvTelefonos_prov.setModel(tableModel)
        self.winPrincipal.tvTelefonos_prov.selectionModel().currentChanged.connect(self.changeSelectedTableTel)