#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Modelo.usuario import Usuario
from Conexion.conexionUsuario import conexionUsuario
from PyQt5.QtWidgets import QAbstractItemView
from Componentes.tableModel import MyTableModel
from Modelo.direccion import Direccion
from Conexion.conexionTelefono import conexionTelefono
from Modelo.telefono import Telefono
from PyQt5.QtWidgets import QMessageBox, QDialog

class PestaniaUsuario():

    def __init__(self, winPrincipal):
        self.winPrincipal = winPrincipal
        self.usuario = Usuario()
        self.conexionUsuario = conexionUsuario()
        self.conexionTelefono = conexionTelefono()
        self.estado = ""
        self.direccion = Direccion()

        self.configInit()


    def configInit(self):
        self.limpiarCampos()
        #Configurando botones Generales
        self.winPrincipal.btnAgregar_u.clicked.connect(self.onClickAgregar_u)
        self.winPrincipal.btnGuardar_u.clicked.connect(self.onClickGuardar_u)
        self.winPrincipal.btnBorrar_u.clicked.connect(self.onClickBorrar_u)
        self.winPrincipal.btnModificar_u.clicked.connect(self.onClickModificar_u)

        #Configurando botones ABM telefono
        self.winPrincipal.btnSumarTelefono_u.clicked.connect(self.onClickSumarTelefono)
        self.winPrincipal.btnRestarTelefono_u.clicked.connect(self.onClickRestarTelefono)
        self.winPrincipal.btnCancelarTelefono_u.clicked.connect(self.onClickCancelarTelefono)
        self.winPrincipal.btnCancelarTelefono_u.setVisible(False)
        self.winPrincipal.btnRestarTelefono_u.setEnabled(False)

        #configurando botones tipo telefono
        self.winPrincipal.btnTelefono_u.clicked.connect(self.onClickTelefono)
        self.winPrincipal.btnCelular_u.clicked.connect(self.onClickCelular)
        self.winPrincipal.btnFax_u.clicked.connect(self.onClickFax)

        self.winPrincipal.txtFilterUsuarios_u.returnPressed.connect(self.search)

        #Seteando model y propieades de la tabla
        self.winPrincipal.tvUsuarios_u.setSortingEnabled(True)
        self.winPrincipal.tvUsuarios_u.setMouseTracking(True)
        self.winPrincipal.tvUsuarios_u.setSelectionBehavior(QAbstractItemView.SelectRows)

        #Seteando proiedades de la tabla telefono
        self.winPrincipal.tvTelefonos_u.setSortingEnabled(True)
        self.winPrincipal.tvTelefonos_u.setMouseTracking(True)
        self.winPrincipal.tvTelefonos_u.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.winPrincipal.txtFilterUsuarios_u.setFocus(True)

    def finish(self):
        self.winPrincipal.btnAgregar_u.disconnect()
        self.winPrincipal.btnBorrar_u.disconnect()
        self.winPrincipal.btnModificar_u.disconnect()
        self.winPrincipal.btnGuardar_u.disconnect()

        self.winPrincipal.btnCancelarTelefono_u.disconnect()
        self.winPrincipal.btnSumarTelefono_u.disconnect()
        self.winPrincipal.btnRestarTelefono_u.disconnect()

        self.winPrincipal.btnCelular_u.disconnect()
        self.winPrincipal.btnFax_u.disconnect()
        self.winPrincipal.btnTelefono_u.disconnect()

        self.winPrincipal.tvTelefonos_u.disconnect()
        self.winPrincipal.tvUsuarios_u.disconnect()

    def search(self):
        if self.winPrincipal.txtFilterUsuarios_u.hasFocus() is True:
            self.cargarTabla()


    def onClickAgregar_u(self):
        self.estado = 'AGREGAR'
        self.validarBotones(button='AGREGAR')


    def onClickGuardar_u(self):
        validar = self.validar()

        if validar != "":
            print(validar)
            alert = QDialog()
            QMessageBox.information(alert,"ERROR", validar)
        else:
            self.usuario.setNombre(str(self.winPrincipal.txtNombre_u.text()))
            self.usuario.setApellido(str(self.winPrincipal.txtApellido_u.text()))
            self.usuario.setEmail(str(self.winPrincipal.txtEmail_u.text()))
            self.usuario.setPasswd(str(self.winPrincipal.txtContrasena_u.text()))
            self.usuario.setUsuario(str(self.winPrincipal.txtUsuario_u.text()))


            if self.winPrincipal.cbTipoUsuario_u.currentText() == 'user':
                self.usuario.setTipoUsuario("USR")
            else:
                self.usuario.setTipoUsuario("ADM")




            self.direccion.setDireccion(str(self.winPrincipal.txtDireccion_u.text()))
            if self.winPrincipal.txtDDpto_u.text() != "":
                self.direccion.setDpto(str(self.winPrincipal.txtDDpto_u.text()))
            else:
                self.direccion.setDpto("")
            if self.winPrincipal.txtDNumero_u.text() != "":
                self.direccion.setNumero(int(self.winPrincipal.txtDNumero_u.text()))
            else:
                self.direccion.setNumero(0)
            if self.winPrincipal.txtDPiso_u.text() != "":
                self.direccion.setPiso(int(self.winPrincipal.txtDPiso_u.text()))
            else:
                self.direccion.setPiso(0)

            self.usuario.setDireccion(self.direccion)

            self.validarBotones(button='GUARDAR')

            if self.estado == 'AGREGAR':
                self.insertUsuario()
                self.insertTelefono()
            elif self.estado == 'MODIFICAR':
                self.modificarUsuario()
                self.updateTelefono()


    def onClickModificar_u(self):
        self.estado = 'MODIFICAR'
        self.validarBotones(button='MODIFICAR')


    def onClickBorrar_u(self):
        if self.winPrincipal.btnGuardar_u.isEnabled() != True:
            self.conexionUsuario.borrarUsuario(self.usuario)
            self.cargarTabla()

        self.validarBotones(button='BORRAR')


    def cargarTabla(self):
        parameter = self.winPrincipal.txtFilterUsuarios_u.text()
        typeParameter = ''

        if self.winPrincipal.cbFilterUsuario_u.currentText() == 'Apellido':
            typeParameter = 'u.apellido'
        if self.winPrincipal.cbFilterUsuario_u.currentText() == 'Usuario':
            typeParameter = 'u.usuario'
        else:
            typeParameter = 'u.tipo'

        listaUsuarios = self.conexionUsuario.selectUsuario(typeParameter, parameter)
        if len(listaUsuarios) > 0:

            header = ['ID', 'Nombre', 'Apellido', 'Usuario', 'Tipo', 'Contraseña', 'Email','Direccion', 'N°', 'P', 'D',
                      'iddire', 'idpers']
            tableModel = MyTableModel(self.winPrincipal.tvUsuarios_u, listaUsuarios, header)
            self.winPrincipal.tvUsuarios_u.setModel(tableModel)
            self.winPrincipal.tvUsuarios_u.selectionModel().currentChanged.connect(self.changeSelectedTable)

            self.winPrincipal.tvUsuarios_u.setColumnHidden(0, True)
            self.winPrincipal.tvUsuarios_u.setColumnWidth(1, 200)
            self.winPrincipal.tvUsuarios_u.setColumnWidth(2, 200)
            self.winPrincipal.tvUsuarios_u.setColumnHidden(3, True)
            self.winPrincipal.tvUsuarios_u.setColumnWidth(4, 80)
            self.winPrincipal.tvUsuarios_u.setColumnHidden(5, True)
            self.winPrincipal.tvUsuarios_u.setColumnWidth(6, 270)
            self.winPrincipal.tvUsuarios_u.setColumnWidth(7, 333)
            self.winPrincipal.tvUsuarios_u.setColumnWidth(8, 50)
            self.winPrincipal.tvUsuarios_u.setColumnHidden(9, True)
            self.winPrincipal.tvUsuarios_u.setColumnHidden(10, True)
            self.winPrincipal.tvUsuarios_u.setColumnHidden(11, True)
            self.winPrincipal.tvUsuarios_u.setColumnHidden(12, True)
        else:
            self.winPrincipal.tvUsuarios_u.setModel(None)


    def changeSelectedTable(self, selected, deselected):
        usuarioList = selected.model().mylist
        usuarioSelected = usuarioList[selected.row()]
        self.usuario = Usuario()
        self.direccion = Direccion()
        self.usuario.setIdUsuario(int(usuarioSelected[0]))
        self.usuario.setNombre(str(usuarioSelected[1]))
        self.usuario.setApellido(str(usuarioSelected[2]))
        self.usuario.setUsuario(str(usuarioSelected[3]))


        self.usuario.setTipoUsuario(str(usuarioSelected[4]))

        self.usuario.setPasswd(str(usuarioSelected[5]))
        self.usuario.setEmail(str(usuarioSelected[6]))

        self.direccion.setDireccion(str(usuarioSelected[7]))
        if usuarioSelected[8] != None:
            self.direccion.setNumero(int(usuarioSelected[8]))

        if usuarioSelected[9] != None:
            self.direccion.setPiso(int(usuarioSelected[9]))

        if usuarioSelected[10] != None:
            self.direccion.setDpto(usuarioSelected[10])

        self.direccion.setIdDireccion(usuarioSelected[11])
        self.usuario.setDireccion(self.direccion)
        self.usuario.setIdPersona(usuarioSelected[12])
        self.winPrincipal.tvUsuarios_u.setRowHeight(deselected.row(), 28)
        self.winPrincipal.tvUsuarios_u.setRowHeight(selected.row(), 45)

        self.setCampos()
        self.winPrincipal.btnBorrar_u.setEnabled(True)
        self.winPrincipal.btnModificar_u.setEnabled(True)
        self.winPrincipal.tvTelefonos_u.setModel(None)
        self.cargarTablaTelefono()


    def validarBotones(self, button):
        if button == 'AGREGAR' :
            self.winPrincipal.wDatosUsuario.setEnabled(True)
            self.winPrincipal.btnBorrar_u.setEnabled(True)
            self.winPrincipal.btnBorrar_u.setText('CANCELAR')
            self.winPrincipal.btnGuardar_u.setEnabled(True)
            self.winPrincipal.btnModificar_u.setEnabled(False)
            self.winPrincipal.btnAgregar_u.setEnabled(False)
            self.winPrincipal.tvUsuarios_u.setEnabled(False)
            self.limpiarCampos()

        elif button=='GUARDAR':
            self.winPrincipal.btnModificar_u.setEnabled(False)
            self.winPrincipal.btnAgregar_u.setEnabled(True)
            self.winPrincipal.btnGuardar_u.setEnabled(False)
            self.winPrincipal.btnBorrar_u.setText('BORRAR')
            self.winPrincipal.btnBorrar_u.setEnabled(False)
            self.winPrincipal.tvUsuarios_u.setEnabled(True)
            self.winPrincipal.wDatosUsuario.setEnabled(False)
            self.limpiarCampos()

        elif button == 'MODIFICAR':
            self.winPrincipal.btnModificar_u.setEnabled(False)
            self.winPrincipal.btnAgregar_u.setEnabled(False)
            self.winPrincipal.btnGuardar_u.setEnabled(True)
            self.winPrincipal.btnBorrar_u.setText('CANCELAR')
            self.winPrincipal.btnBorrar_u.setEnabled(True)
            self.winPrincipal.tvUsuarios_u.setEnabled(False)
            self.winPrincipal.wDatosUsuario.setEnabled(True)

        elif button=='BORRAR':
            self.winPrincipal.btnModificar_u.setEnabled(False)
            self.winPrincipal.btnAgregar_u.setEnabled(True)
            self.winPrincipal.btnGuardar_u.setEnabled(False)
            self.winPrincipal.btnBorrar_u.setText('BORRAR')
            self.winPrincipal.btnBorrar_u.setEnabled(False)
            self.winPrincipal.tvUsuarios_u.setEnabled(True)
            self.winPrincipal.wDatosUsuario.setEnabled(False)
            self.limpiarCampos()

    def insertUsuario(self):
        self.conexionUsuario.insertarUsuario(self.usuario)
        self.cargarTabla()

    def modificarUsuario(self):
        self.conexionUsuario.modificarUsuario(self.usuario)
        self.cargarTabla()


    def limpiarCampos(self):
        self.winPrincipal.txtApellido_u.setText('')
        self.winPrincipal.txtContrasena_u.setText('')
        self.winPrincipal.txtDireccion_u.setText('')
        self.winPrincipal.txtEmail_u.setText('')
        self.winPrincipal.txtNombre_u.setText('')
        self.winPrincipal.txtUsuario_u.setText('')
        self.winPrincipal.cbTipoUsuario_u.setCurrentIndex(0)
        self.winPrincipal.txtDNumero_u.setText('')
        self.winPrincipal.txtDPiso_u.setText('')
        self.winPrincipal.txtDDpto_u.setText('')
        self.winPrincipal.tvTelefonos_u.setModel(None)
        self.winPrincipal.txtFilterUsuarios_u.setText('')
        self.winPrincipal.tvUsuarios_u.setModel(None)

        self.winPrincipal.txtFilterUsuarios_u.setFocus(True)

    def setCampos(self):
        self.winPrincipal.txtApellido_u.setText(str(self.usuario.getApellido()))
        self.winPrincipal.txtContrasena_u.setText(str(self.usuario.getPasswd()))
        self.winPrincipal.txtEmail_u.setText(str(self.usuario.getEmail()))
        self.winPrincipal.txtNombre_u.setText(str(self.usuario.getNombre()))

        self.winPrincipal.txtUsuario_u.setText(str(self.usuario.getUsuario()))
        if self.usuario.getTipoUsuario() == 'ADM':
            self.winPrincipal.cbTipoUsuario_u.setCurrentIndex(1)
        elif self.usuario.getTipoUsuario() == 'USR':
            self.winPrincipal.cbTipoUsuario_u.setCurrentIndex(0)

        self.winPrincipal.txtDireccion_u.setText(str(self.usuario.getDireccion().getDireccion()))

        if self.usuario.getDireccion().getNumero() != None:
            self.winPrincipal.txtDNumero_u.setText(str(self.usuario.getDireccion().getNumero()))
        else:
            self.winPrincipal.txtDNumero_u.setText('')

        if self.usuario.getDireccion().getPiso() != None:
            self.winPrincipal.txtDPiso_u.setText(str(self.usuario.getDireccion().getPiso()))
        else:
            self.winPrincipal.txtDPiso_u.setText('')

        if self.usuario.getDireccion().getDpto() != None:
            self.winPrincipal.txtDDpto_u.setText(self.usuario.getDireccion().getDpto())
        else:
            self.winPrincipal.txtDDpto_u.setText('')


    def validar(self):
        mensaje = ""

        if self.winPrincipal.txtApellido_u.text() == '':
            mensaje = "Falta ingresar un apellido."
        elif self.winPrincipal.txtNombre_u.text() == '':
            mensaje = "Falta ingresar un nombre."
        elif self.winPrincipal.txtDireccion_u.text() == '':
            mensaje = "Falta ingresar la Direccion"
        elif self.winPrincipal.txtUsuario_u.text() == '':
            mensaje = "Falta ingresar el nombre de usuario"
        elif self.winPrincipal.txtContrasena_u.text() == '':
            mensaje = "Falta ingresa la contraseña."

        return mensaje




    def cargarTablaTelefono(self):
        self.listTelefonosInit = self.conexionTelefono.selectTelefono(self.usuario)
        if len(self.listTelefonosInit) >0:
            header = ['ID', 'Numero', 'TIPO']
            tableModel = MyTableModel(self.winPrincipal, self.listTelefonosInit, header)
            self.winPrincipal.tvTelefonos_u.setModel(tableModel)
            self.winPrincipal.tvTelefonos_u.selectionModel().currentChanged.connect(self.changeSelectedTableTel)

            self.winPrincipal.tvTelefonos_u.setColumnHidden(0, True)
            self.winPrincipal.tvTelefonos_u.setColumnWidth(1, 36)
            self.winPrincipal.tvTelefonos_u.setColumnWidth(2, 175)

            for r in range(0, len(self.listTelefonosInit)):
                self.winPrincipal.tvTelefonos_u.setRowHidden(r, False)



    def changeSelectedTableTel(self, selected, deselected):
        listTelefonos = selected.model().mylist
        self.telefonoSelected = ()
        self.telefonoSelected = listTelefonos[selected.row()]

        self.telefonoSelectedRow = selected.row()
        self.winPrincipal.txtTelefono_u.setText(str(self.telefonoSelected[2]))

        self.setTipoTelefono(str(self.telefonoSelected[1]))
        self.winPrincipal.btnCancelarTelefono_u.setVisible(True)
        self.winPrincipal.btnRestarTelefono_u.setEnabled(True)
        self.winPrincipal.tvTelefonos_u.setEnabled(False)

        self.winPrincipal.btnGuardar_u.setEnabled(False)
        self.winPrincipal.btnBorrar_u.setEnabled(False)

    def updateTelefono(self):

        listTelefono = []
        listTelefono = list(self.winPrincipal.tvTelefonos_u.model().mylist).copy()

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
                        telNew.setIdPersona(self.usuario.getIdPersona())
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
                        telNew.setIdPersona(self.usuario.getIdPersona())
                        telNew.setIdTelefono(telN[0])
                        telNew.setTipo(telN[1])
                        telNew.setTelefono(telN[2])
                        self.conexionTelefono.insertarTelefono(telNew)



    def insertTelefono(self):

        listTelefonosNew = []
        tel = self.winPrincipal.tvTelefonos_u.model()

        listTelefonosNew = list(self.winPrincipal.tvTelefonos_u.model().mylist).copy()

        if len(listTelefonosNew) > 0:
            self.conexionTelefono.insertTelefonoInit(listTelefonosNew)


    def onClickCancelarTelefono(self):
        self.winPrincipal.btnCancelarTelefono_u.setVisible(False)
        self.winPrincipal.txtTelefono_u.setText('')

        self.winPrincipal.btnRestarTelefono_u.setEnabled(False)
        self.winPrincipal.tvTelefonos_u.clearSelection()
        self.winPrincipal.tvTelefonos_u.setEnabled(True)

        self.winPrincipal.btnGuardar_u.setEnabled(True)
        self.winPrincipal.btnBorrar_u.setEnabled(True)

    def onClickSumarTelefono(self):
        numTelefono = self.winPrincipal.txtTelefono_u.text()

        if numTelefono.isdigit() == True:
            if self.winPrincipal.btnCancelarTelefono_u.isVisible() is True:
                self.updateTelefonoTabla()
            else:
                self.insertTelefonoTabla()

            self.winPrincipal.tvTelefonos_u.clearSelection()
            self.winPrincipal.btnRestarTelefono_u.setEnabled(False)
            self.winPrincipal.btnCancelarTelefono_u.setVisible(False)
            self.winPrincipal.txtTelefono_u.setText('')
            self.winPrincipal.tvTelefonos_u.setEnabled(True)

            self.winPrincipal.btnGuardar_u.setEnabled(True)
        else:
            alert = QDialog()
            QMessageBox.information(alert,"ERROR", "El numero de telefono no es valido.")


    def onClickRestarTelefono(self):
        listTabTel = []
        tipoTel = str(self.getTipoTelefono())
        listTelefonosNew = []

        listTabTel = list(self.winPrincipal.tvTelefonos_u.model().mylist).copy()

        header = ['Id', 'Tipo', 'Numero']
        telDel = [self.telefonoSelected[0], self.telefonoSelected[1], '']
        listTabTel[self.telefonoSelectedRow] = telDel
        tableTelModel = MyTableModel(self.winPrincipal, listTabTel, header)
        self.winPrincipal.tvTelefonos_u.setModel(tableTelModel)
        self.winPrincipal.tvTelefonos_u.selectionModel().currentChanged.connect(self.changeSelectedTableTel)
        self.winPrincipal.tvTelefonos_u.setRowHidden(self.telefonoSelectedRow, True)

        self.winPrincipal.btnCancelarTelefono_u.setVisible(False)
        self.winPrincipal.txtTelefono_u.setText('')
        self.winPrincipal.btnRestarTelefono_u.setEnabled(False)
        self.winPrincipal.tvTelefonos_u.setEnabled(True)

        self.winPrincipal.btnGuardar_u.setEnabled(True)
        self.winPrincipal.btnBorrar_u.setEnabled(True)

    def onClickTelefono(self):
        self.changeTipoTelefono(button='TEL')

    def onClickCelular(self):
        self.changeTipoTelefono(button='CEL')

    def onClickFax(self):
        self.changeTipoTelefono(button='FAX')

    def changeTipoTelefono(self, button):

        if button == 'TEL':
            self.winPrincipal.btnTelefono_u.setEnabled(False)
            self.winPrincipal.btnCelular_u.setEnabled(True)
            self.winPrincipal.btnFax_u.setEnabled(True)
        elif button == 'CEL':
            self.winPrincipal.btnTelefono_u.setEnabled(True)
            self.winPrincipal.btnCelular_u.setEnabled(False)
            self.winPrincipal.btnFax_u.setEnabled(True)
        elif button == 'FAX':
            self.winPrincipal.btnTelefono_u.setEnabled(True)
            self.winPrincipal.btnCelular_u.setEnabled(True)
            self.winPrincipal.btnFax_u.setEnabled(False)


    def setTipoTelefono(self, tipoTelefono):

        if tipoTelefono == 'TEL':
            self.winPrincipal.btnTelefono_u.setEnabled(False)
            self.winPrincipal.btnCelular_u.setEnabled(True)
            self.winPrincipal.btnFax_u.setEnabled(True)
        elif tipoTelefono == 'CEL':
            self.winPrincipal.btnTelefono_u.setEnabled(True)
            self.winPrincipal.btnCelular_u.setEnabled(False)
            self.winPrincipal.btnFax_u.setEnabled(True)
        elif tipoTelefono == 'FAX':
            self.winPrincipal.btnTelefono_u.setEnabled(True)
            self.winPrincipal.btnCelular_u.setEnabled(True)
            self.winPrincipal.btnFax_u.setEnabled(False)

    def getTipoTelefono(self):

        if self.winPrincipal.btnTelefono_u.isEnabled() != True:
            return 'TEL'
        elif self.winPrincipal.btnCelular_u.isEnabled() != True:
            return 'CEL'
        elif self.winPrincipal.btnFax_u.isEnabled() != True:
            return 'FAX'


    def insertTelefonoTabla(self):
        numTel = self.winPrincipal.txtTelefono_u.text()
        tipoTel = str(self.getTipoTelefono())

        modelListTelefono = self.winPrincipal.tvTelefonos_u.model()
        header = ['ID', 'Tipo', 'Numero']

        if modelListTelefono is not None:
            listTabTel = list(self.winPrincipal.tvTelefonos_u.model().mylist)

            if len(listTabTel) > 0 or listTabTel is not None:
                tuplaTel = ('0', tipoTel, numTel )
                listTabTel.append(tuplaTel)
                tupleTable = tuple(listTabTel)

                tableModel = MyTableModel(self.winPrincipal, tupleTable , header)
                self.winPrincipal.tvTelefonos_u.setModel(tableModel)
                self.winPrincipal.tvTelefonos_u.selectionModel().currentChanged.connect(self.changeSelectedTableTel)
        else:
            lista = []
            tuplaTel = ('0', tipoTel, numTel )
            lista.append(tuplaTel)

            tableModel = MyTableModel(self.winPrincipal, lista , header)
            self.winPrincipal.tvTelefonos_u.setModel(tableModel)
            self.winPrincipal.tvTelefonos_u.selectionModel().currentChanged.connect(self.changeSelectedTableTel)
            self.winPrincipal.tvTelefonos_u.setColumnHidden(0, True)
            self.winPrincipal.tvTelefonos_u.setColumnWidth(1, 36)
            self.winPrincipal.tvTelefonos_u.setColumnWidth(2, 175)


    def updateTelefonoTabla(self):
        listTabTel = []
        tipoTel = str(self.getTipoTelefono())
        listTelefonosNew = []
        prob = self.winPrincipal.tvTelefonos_u.selectionModel()
        prob1 = self.winPrincipal.tvTelefonos_u.model()
        listTabTel = list(self.winPrincipal.tvTelefonos_u.model().mylist).copy()

        telUpd = (self.telefonoSelected[0], tipoTel, int(self.winPrincipal.txtTelefono_u.text()))
        listTabTel[self.telefonoSelectedRow] = telUpd
        header = ['ID', 'Tipo', 'Numero']
        tableModel = MyTableModel(self.winPrincipal, listTabTel , header)
        self.winPrincipal.tvTelefonos_u.setModel(tableModel)
        self.winPrincipal.tvTelefonos_u.selectionModel().currentChanged.connect(self.changeSelectedTableTel)