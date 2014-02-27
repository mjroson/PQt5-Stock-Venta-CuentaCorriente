from Conexion.conexionPagos import ConexionPagos
from Modelo.cliente import Cliente
from Modelo.proveedor import Proveedor
from Modelo.producto import Producto
from PyQt5.QtWidgets import QLineEdit
from Componentes.tableModel import MyTableModel
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.Qt import QKeyEvent
from PyQt5.QtWidgets import QMessageBox, QDialog
import datetime
from PyQt5.Qt import QDesktopServices, QUrl
from PyQt5.Qt import QTextDocument, QPrinter, QPrintDialog


class PestaniaPagos():


    def __init__(self, winPrincipal):
        self.conexionPagos = ConexionPagos()
        self.winPrincipal = winPrincipal
        self.cliente = Cliente()
        self.proveedor = Proveedor()
        self.state = 'COBRANZA'

        self.configInit()

    def configInit(self):
        self.winPrincipal.tvCuentaCorriente_pag.setSortingEnabled(True)
        self.winPrincipal.tvCuentaCorriente_pag.setMouseTracking(True)
        self.winPrincipal.tvCuentaCorriente_pag.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.winPrincipal.btnAceptar_pag.clicked.connect(self.OnClickAceptar)
        self.winPrincipal.btnCancelar_pag.clicked.connect(self.OnClickCancelar)

        #self.winPrincipal.txtFilterPagos_pag.textChanged.connect(self.cargarTablaCliente)
        self.winPrincipal.txtFilterPagos_pag.returnPressed.connect(self.search)

        self.winPrincipal.txtMonto_pag.textChanged.connect(self.activateField)

        self.winPrincipal.rbCobranza_pag.clicked.connect(self.OnClickCobranza)
        self.winPrincipal.rbPago_pag.clicked.connect(self.OnClickPago)



    def cargarTablaCliente(self):
        tipoParametro = ''
        if self.winPrincipal.cbFilterCliente_pag.currentText() == 'Apellido':
            tipoParametro = 'c.apellido'
        elif self.winPrincipal.cbFilterCliente_pag.currentText() == 'Nombre':
            tipoParametro = 'p.nombre'

        parametro = self.winPrincipal.txtFilterPagos_pag.text()

        listaClientes = self.conexionPagos.selectClientes(tipoParametro, parametro)
        if len(listaClientes) > 0:
            header = ['ID','Apellido','Nombre','Email']
            tablaModel = MyTableModel(self.winPrincipal.tvCuentaCorriente_pag, listaClientes, header)
            self.winPrincipal.tvCuentaCorriente_pag.setModel(tablaModel)
            self.winPrincipal.tvCuentaCorriente_pag.selectionModel().currentChanged.connect(self.changeSelectedTable)


            self.winPrincipal.tvCuentaCorriente_pag.setColumnHidden(0, True)
            self.winPrincipal.tvCuentaCorriente_pag.setColumnWidth(1, 140)
            self.winPrincipal.tvCuentaCorriente_pag.setColumnWidth(2, 140)
            self.winPrincipal.tvCuentaCorriente_pag.setColumnWidth(3, 207)
        else:
            self.winPrincipal.tvCuentaCorriente_pag.setModel(None)


    def changeSelectedTable(self, selected, deselected):
        listPersonas = selected.model().mylist

        personaSelected = ()
        personaSelected = tuple(listPersonas[selected.row()])

        if self.state == "COBRANZA":
            self.cliente = Cliente()
            self.cliente.setIdCliente(int(personaSelected[0]))
            self.cliente.setApellido(str(personaSelected[1]))
            self.cliente.setNombre(str(personaSelected[2]))
            self.cliente.setEmail(str(personaSelected[3]))

        elif self.state == "PAGO":
            self.proveedor = Proveedor()
            self.proveedor.setIdProveedor(int(personaSelected[0]))
            self.proveedor.setDescripcion(str(personaSelected[1]))
            self.proveedor.setNombre(str(personaSelected[2]))
            self.proveedor.setEmail(str(personaSelected[3]))

        self.calcularTransaccion()


    def calcularTransaccion(self):
        listTransacciones = []

        listPagos = []
        #Total de los pagos
        pagosTotal = 0
        #Total de las transacciones en estado 0
        transaccionesTotal = 0

        #Lista completa (transacciones + pagos)
        listDetalle = []
        if self.state == "COBRANZA":
            listPagos = self.conexionPagos.selectListPagosCliente(self.cliente)
            listTransacciones = self.conexionPagos.selectListTransaccionCliente(self.cliente)


            if len(listPagos) > 0:
                for pagos in listPagos:
                    pagosTotal += float(pagos[1])
                    auxMonto = "$  + " + str("{0:.2f}".format(pagos[1]))
                    auxPagos = (str(pagos[0]), auxMonto, str(pagos[2]))
                    listDetalle.append(auxPagos)
            else:
                pagosTotal = 0

            if len(listTransacciones):
                for transacciones in listTransacciones:
                    transaccionesTotal += transacciones[1]
                    auxMonto = "$  - " + str("{0:.2f}".format(transacciones[1]))
                    auxTransaccion = (str(transacciones[0]), auxMonto, str(transacciones[2]))
                    listDetalle.append(auxTransaccion)
            else:
                transaccionesTotal = 0

            total = pagosTotal  - transaccionesTotal

        elif self.state == "PAGO":
            listPagos = self.conexionPagos.selectListPagosProveedor(self.proveedor)
            listTransacciones = self.conexionPagos.selectListTransaccionProveedor(self.proveedor)

            if len(listPagos) > 0:
                for pagos in listPagos:
                    pagosTotal += float(pagos[1])
                    auxMonto = "$  + " + str("{0:.2f}".format(pagos[1]))
                    auxPagos = (str(pagos[0]), auxMonto, str(pagos[2]))
                    listDetalle.append(auxPagos)
            else:
                pagosTotal = 0

            if len(listTransacciones):
                for transacciones in listTransacciones:
                    transaccionesTotal += transacciones[1]
                    auxMonto = "$  - " + str("{0:.2f}".format(transacciones[1]))
                    auxTransaccion = (str(transacciones[0]), auxMonto, str(transacciones[2]))
                    listDetalle.append(auxTransaccion)
            else:
                transaccionesTotal = 0


            total = pagosTotal - transaccionesTotal


        self.winPrincipal.lblTotalDeuda_pag.setText(str(total))

        if len(listDetalle) > 0:
                header = ['Fecha','Monto', 'Tipo de movimiento']
                tablaModel = MyTableModel(self.winPrincipal.tvDetalleTransaccion_pag, listDetalle, header)
                self.winPrincipal.tvDetalleTransaccion_pag.setModel(tablaModel)

                self.winPrincipal.tvDetalleTransaccion_pag.setColumnWidth(0, 190)
                self.winPrincipal.tvDetalleTransaccion_pag.setColumnWidth(1, 190)
                self.winPrincipal.tvDetalleTransaccion_pag.setColumnWidth(2, 190)


    def cargarTablaProveedor(self):

        tipoParametro = ''

        if self.winPrincipal.cbFilterCliente_pag.currentText() == 'Apellido':
            tipoParametro = 'prov.descripcion'
        elif self.winPrincipal.cbFilterCliente_pag.currentText() == 'Nombre':
            tipoParametro = 'p.nombre'

        parametro = self.winPrincipal.txtFilterPagos_pag.text()


        listaClientes = self.conexionPagos.selectProveedores(tipoParametro, parametro)
        if len(listaClientes) >0:
            header = ['ID','Descripcion','Nombre','Email']
            tablaModel = MyTableModel(self.winPrincipal.tvCuentaCorriente_pag, listaClientes, header)
            self.winPrincipal.tvCuentaCorriente_pag.setModel(tablaModel)
            self.winPrincipal.tvCuentaCorriente_pag.selectionModel().currentChanged.connect(self.changeSelectedTable)


            self.winPrincipal.tvCuentaCorriente_pag.setColumnHidden(0, True)
            self.winPrincipal.tvCuentaCorriente_pag.setColumnWidth(1, 140)
            self.winPrincipal.tvCuentaCorriente_pag.setColumnWidth(2, 140)
            self.winPrincipal.tvCuentaCorriente_pag.setColumnWidth(3, 207)
        else:
            self.winPrincipal.tvCuentaCorriente_pag.setModel(None)



    def OnClickAceptar(self):
        total = float(self.winPrincipal.txtMonto_pag.text())
        subNom = ''
        idRecibo = 0
        if self.state == 'COBRANZA':
            idRecibo = self.conexionPagos.cargarCobranza(self.cliente, total)
            subNom ='COBRANZA'
        elif self.state == 'PAGO':
            idRecibo = self.conexionPagos.cargarPago(self.proveedor, total)
            subNom = 'PAGO'

        totalDeuda = float(self.winPrincipal.lblTotalDeuda_pag.text())

        alert = QDialog()
        confirm = QMessageBox.question(alert, "Mensaje", "¿ Desea generar Recibo ?", QMessageBox.Yes, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.createRecibo(subNom=subNom, idRecibo=idRecibo, total=total, totDeuda=totalDeuda, totPago=total)
        self.limpiarCampos()
        self.winPrincipal.txtFilterPagos_pag.setFocus(True)

    def OnClickCancelar(self):
        self.limpiarCampos()

    def OnClickCobranza(self):
        self.state = 'COBRANZA'


    def OnClickPago(self):
        self.state = 'PAGO'


    def limpiarCampos(self):
        self.winPrincipal.txtMonto_pag.setText('')
        self.winPrincipal.txtFilterPagos_pag.setText('')
        self.winPrincipal.txtFilterPagos_pag.setEnabled(True)
        self.winPrincipal.tvCuentaCorriente_pag.setEnabled(True)
        self.winPrincipal.tvCuentaCorriente_pag.setModel(None)
        self.winPrincipal.btnAceptar_pag.setEnabled(False)
        self.winPrincipal.btnCancelar_pag.setEnabled(False)
        self.winPrincipal.lblTotalDeuda_pag.setText('0.00')

        self.winPrincipal.tvDetalleTransaccion_pag.setModel(None)



    def finish(self):
        #self.winPrincipal.txtFilterPagos_pag.disconnect()
        #self.winPrincipal.txtMonto_pag.disconnect()
        self.winPrincipal.btnAceptar_pag.disconnect()
        self.winPrincipal.btnCancelar_pag.disconnect()
        self.winPrincipal.rbPago_pag.disconnect()
        self.winPrincipal.rbCobranza_pag.disconnect()

    def activateField(self):
        if self.winPrincipal.btnAceptar_pag.isEnabled() is False:
            self.winPrincipal.txtFilterPagos_pag.setEnabled(False)
            self.winPrincipal.tvCuentaCorriente_pag.setEnabled(False)
            self.winPrincipal.btnAceptar_pag.setEnabled(True)
            self.winPrincipal.btnCancelar_pag.setEnabled(True)

    def search(self):
        if self.winPrincipal.txtFilterPagos_pag.hasFocus() is True:
            if self.state == "COBRANZA":
            #if self.winPrincipal.rbCobranza_pag.isChecked() is True:
                self.cargarTablaCliente()
            else:
                self.cargarTablaProveedor()




    def createRecibo(self, subNom, idRecibo, total, totDeuda, totPago):
        hoy = str(datetime.datetime.now().year) + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + str(datetime.datetime.now().hour) + str(datetime.datetime.now().minute) + str(datetime.datetime.now().second)

        nombrePdf = '../archivos/' + str(hoy + subNom) + '.pdf'
        listTransaccionTable = ""


        nombre = ""
        apellido = ""

        if(self.state == "COBRANZA"):
            nombre = self.cliente.getNombre()
            apellido = self.cliente.getApellido()
        elif(self.state == "PAGO"):
            nombre = self.proveedor.getNombre()
            apellido = self.proveedor.getDescripcion()

        totalDeuda = float(totDeuda)
        deudaString = "$  " + "{0:.2f}".format(totalDeuda)
        totalPago = float(totPago)
        pagoString = "$  +" +  "{0:.2f}".format(totalPago)

        total = float(totalDeuda + totalPago)
        totalString = "{0:.2f}".format(total)
        fecha = str(datetime.datetime.now())
        html =  """
                     <table width="600">
                        <tr width="600" color="#000000">
                            <td width="80%">
                               Perfumeria La que vende perfumes <br>
                               LABOULAYE, CORDOBA, ARGENTINA <br>
                               TEL: 0351-111111  <br>
                               MAIL: MAIL@MAIL.COM  <br>
                            </td>
                            <td width="20%" align="right">
                                <IMG SRC="kde1.png">
                            </td>
                        </tr>

                    </table>
                _______________________________________________________________________________________________________
                    <p>
                        DATOS DEL CLIENTE:
                    </p>
                    <br>
                    <table>

                        <tr>
                            <td>
                                NOMBRE:   """+ nombre +"""  <br>
                                APELLIDO: """ + apellido + """ <br>

                            </td>
                            <td>
                            </td>
                        </tr>
                    </table>

                    <br>
                    _______________________________________________________________________________________________________
                    <br>
                    <p>
                        DETALLES DEL RECIBO:
                    </p>
                    <br>
                    <table width="600" height="0" style="border-color: black; border-width: 0.5px; border-spacing: 0;">
                      <tr  style=" background-color: gray; border-style: inset;">
                        <td width="80%"  align="center" valign="middle">
                            <b>
                            DESCRIPCION
                            </b>
                        </td>
                        <td width="20%"  align="center" valign="middle">
                            <b>
                                MONTO
                            </b>
                        </td>

                      </tr>
                  </table>

                  <br>
                  <br>
                  <br>
                  <br>

                  <table  height="350" width="600" style="border-color: gray; border-width: .4px; border-collapse: collapse;">
                      <tr height="80">
                            <td width="80%" align="left" >
                            <br>DEUDA <br>
                            </td>
                            <td width="20%" >
                                <br> &nbsp;&nbsp; """ + str(deudaString) + """<br>
                            </td>

                        </tr>
                        <tr height="80">
                            <td width="80%" align="left" >
                            <br> PAGO<br>
                            </td>
                            <td width="20%" >
                                <br> &nbsp;&nbsp;""" + str(pagoString)  + """<br>
                            </td>

                        </tr>
                  </table>
                    <br>
                    <br>
                    <table width="600" border="0.5" height="0" style="border-color: black; border-width: 0.5px; border-spacing: 0;">
                        <tr >
                            <td width="90%" align="right">
                                <br>
                                TOTAL..................................................................................................................
                                <br>
                            </td>
                            <td width="10%" align="center">
                              <br> $ """ + str(totalString) + """<br>
                            </td>
                        </tr>
                    </table>

                    <br>
                    <br>
                    <br>
                    <br>
                    <br>
                    <br>
                    <p width="600" align="center" style=" font-size: 10; " >
                    Por cualquier consulta, sobre este recibo, dirigirse al local que se encuentra ubicado en la calle
                    independencia 450. <br> O Comunicarse a los telefonos 03382-123123123 / 4231231
                    </p>
                    <br>
                    <br>
                    <br>
                    <br>
                    <br>
                    _______________________________________________________________________________________________________
                    <br>
                    <table width="600">
                        <tr>
                            <td align="right" width="80%">
                            FECHA/HORA : """+ fecha + """
                            </td>
                            <td align="right">
                            N° : """+ str(idRecibo) +"""
                            </td>
                        </tr>
                    </table>
                    _______________________________________________________________________________________________________
                """

        doc = QTextDocument()
        doc.setHtml(html)
        printer = QPrinter()
        printer.setOutputFileName(nombrePdf)

        printer.setOutputFormat(QPrinter.PdfFormat)
        doc.print(printer)
        printer.newPage()
        url = QUrl
        url = QUrl(nombrePdf)
        QDesktopServices.openUrl(url)
