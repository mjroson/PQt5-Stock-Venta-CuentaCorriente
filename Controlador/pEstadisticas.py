from Conexion.conexionGeneral import ConexionGenerales
from PyQt5.Qt import QDesktopServices, QUrl
import datetime
from PyQt5.Qt import QTextDocument, QPrinter
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtWidgets import QMessageBox, QDialog
from Modelo.cliente import Cliente
from Modelo.proveedor import Proveedor
from Componentes.tableModel import MyTableModel
import matplotlib.pyplot as pyplot
import numpy as np
from PyQt5.QtWidgets import QAbstractItemView

class PestaniaEstadisticas():

    def __init__(self, winPrincipal):
        self.conexionesGenerales = ConexionGenerales()
        self.winPrincipal = winPrincipal


        hoy = datetime.datetime.now().date()
        self.winPrincipal.deHasta_stock.setDate(hoy)
        self.winPrincipal.deHasta_dinero.setDate(hoy)
        self.winPrincipal.deHasta_saldos.setDate(hoy)

        self.winPrincipal.btnGenerarPdf_dinero.clicked.connect(self.generarDinero)
        self.winPrincipal.btnGenerarPdf_stock.clicked.connect(self.generarStock)
        self.winPrincipal.btnGenerarPdf_saldos.clicked.connect(self.generarSaldos)
        self.winPrincipal.txtFilterPersona_saldos.returnPressed.connect(self.buscarPersonas)
        self.winPrincipal.rbClientes_saldos.clicked.connect(self.changePersona)
        self.winPrincipal.rbProveedores_saldos.clicked.connect(self.changePersona)

        self.winPrincipal.chbTodos_saldos.clicked.connect(self.clickTodos)

        self.winPrincipal.chbHoy_stock.clicked.connect(self.clickHoy_stock)
        self.winPrincipal.chbHoy_saldos.clicked.connect(self.clickHoy_saldos)
        self.winPrincipal.chbHoy_dinero.clicked.connect(self.clickHoy_dinero)


        self.winPrincipal.tvPersonas_saldos.setSortingEnabled(True)
        self.winPrincipal.tvPersonas_saldos.setMouseTracking(True)
        self.winPrincipal.tvPersonas_saldos.setSelectionBehavior(QAbstractItemView.SelectRows)


    def generarDinero(self):
        intervalo = 'month'
        if self.winPrincipal.cbIntervalo_dinero.currentText() == 'Semana':
            intervalo = 'week'
        elif self.winPrincipal.cbIntervalo_dinero.currentText() == 'Año':
            intervalo = 'year'
        elif self.winPrincipal.cbIntervalo_dinero.currentText() == 'Dia':
            intervalo = 'day'

        auxDesde = self.winPrincipal.deDesde_dinero.text()

        desde = auxDesde[6:10] + '-' + auxDesde[3:5] + '-' + auxDesde[0:2]

        auxHasta = self.winPrincipal.deHasta_dinero.text()
        hasta = auxHasta[6:10] + '-' + auxHasta[3:5] + '-' + auxHasta[0:2]

        listaEntradaTransacciones = self.conexionesGenerales.selectEntradasTransacciones(intervalo, desde, hasta)
        listaEntradaPagos = self.conexionesGenerales.selectEntradaPagos(intervalo, desde, hasta)

        listaSalidaTransacciones = self.conexionesGenerales.selectSalidaTransacciones(intervalo, desde, hasta)
        listaSalidaPagos = self.conexionesGenerales.selectSalidaPagos(intervalo, desde, hasta)

        listaGeneral =[]

        if len(listaEntradaPagos) < 1 and len(listaEntradaTransacciones) < 1 and len(listaSalidaPagos) < 1 and len(listaSalidaTransacciones) < 1:
            pass

        else:
            dineroEntrada = 0
            dineroSalida = 0
            for entradaP in listaEntradaPagos:
                dineroEntrada += float(entradaP[1])
                monto = '$ + ' + str("{0:.2f}".format(entradaP[1]))
                entrada = []
                entrada.append(entradaP[0])
                entrada.append(monto)
                entrada.append(entradaP[2])
                #entrada = (entradaP[0] + monto + entradaP[2] )
                listaGeneral.append(entrada)

            for entradaT in listaEntradaTransacciones:
                dineroEntrada += float(entradaT[1])
                monto = '$ + ' + str("{0:.2f}".format(entradaT[1]))
                entrada = []
                entrada.append(entradaT[0])
                entrada.append(monto)
                entrada.append(entradaT[2])
                #entrada = (entradaT[0], monto, entradaT[2])
                listaGeneral.append(entrada)

            for salidaP in listaSalidaPagos:
                dineroSalida += float(salidaP[1])
                monto = '$ - ' + str("{0:.2f}".format(salidaP[1]))
                salida = []
                salida.append(salidaP[0])
                salida.append(monto)
                salida.append(salidaP[2])
                #salida = (salidaP[0], monto, salidaP[2])
                listaGeneral.append(salida)

            for salidaT in listaSalidaTransacciones:
                dineroSalida += float(salidaT[1])
                monto = '$ - ' + str("{0:.2f}".format(salidaT[1]))
                salida = []
                salida.append(salidaT[0])
                salida.append(monto)
                salida.append(salidaT[2])
                #salida = (salidaT[0], monto, salidaT[2])
                listaGeneral.append(salida)

            listTable = ""
            listaGeneral.sort()
            for lista in listaGeneral:
                listTable += """
                                <tr height="80">
                                    <td width="60%" align="left" >
                                    <br>""" + str(lista[0])  + """<br>
                                    </td>
                                    <td width="20%" align="right">
                                        <br> &nbsp;&nbsp;""" + str(lista[1])  + """<br>
                                    </td>
                                    <td width="20%" align="center">
                                       <br>&nbsp;&nbsp; """ + str(lista[2])  + """<br>
                                    </td>
                                </tr>
                           """

            contenido = """
                             <table width="600" height="0" style="border-color: black; border-width: 0.5px; border-spacing: 0;">
                              <tr  style=" background-color: gray; border-style: inset;">
                                <td width="60%"  align="center" valign="middle">
                                    <b>
                                    FECHA
                                    </b>
                                </td>
                                <td width="20%"  align="center" valign="middle">
                                    <b>
                                        DINERO
                                    </b>
                                </td>
                                <td width="20%"  align="center" valign="middle">
                                    <b>
                                        TIPO MOVIMIENTO
                                    </b>
                                </td>
                              </tr>
                          </table>
                          <br>
                          <table width="600" >
                            """+listTable +"""

                          </table>

                          <p>
                            <br>
                            Dinero entrante = $ + """ +str("{0:.2f}".format(dineroEntrada)) + """
                            <br>
                            Dinero salida = $ - """+ str("{0:.2f}".format(dineroSalida)) + """
                            <br>
                            <br>
                            Total .... : $ """+ str("{0:.2f}".format(dineroEntrada - dineroSalida)) +"""
                          </p>
                        """
            self.generatePDF(contenido)


    def generarStock(self):
        self.listFinal = []
        self.title = "intervalo"

        intervalo = 'month'
        if self.winPrincipal.cbIntervalo_stock.currentText() == 'Semana':
            intervalo = 'week'
        elif self.winPrincipal.cbIntervalo_stock.currentText() == 'Año':
            intervalo = 'year'


        auxDesde = self.winPrincipal.deDesde_stock.text()

        desde = auxDesde[6:10] + '-' + auxDesde[3:5] + '-' + auxDesde[0:2]

        auxHasta = self.winPrincipal.deHasta_stock.text()
        hasta = auxHasta[6:10] + '-' + auxHasta[3:5] + '-' + auxHasta[0:2]

        listVentas = self.conexionesGenerales.selectVentas(intervalo, desde, hasta)
        listCompras = self.conexionesGenerales.selectCompras(intervalo, desde, hasta)

        if len(listCompras) < 1 and len(listVentas) < 1:
            alert = QDialog()
            confirm = QMessageBox.question(alert, "Mensaje", "Verifique los valores, la consulta no tiene ningun dato.", QMessageBox.Ok)

        else:
            i= 0
            for ventas in listVentas:
                itemList = (str(ventas[0]), listCompras[i][1], ventas[1])
                self.listFinal.append(itemList)
                i += 1


            listTable = ""
            cantMax = 0
            tupleFecha = []
            tupleCompra = []
            tupleVenta = []
            listFechas = []
            for lista in self.listFinal:
                i = 0
                listTable += """
                                            <tr height="80">
                                                <td width="60%" align="left" >
                                                <br>""" + str(lista[0])  + """<br>
                                                </td>
                                                <td width="20%" align="center">
                                                    <br> &nbsp;&nbsp;""" + str(lista[1])  + """<br>
                                                </td>
                                                <td width="20%" align="center">
                                                   <br>&nbsp;&nbsp; """ + str(lista[2])  + """<br>
                                                </td>
                                            </tr>
                                       """
                if int(lista[1]) > int(lista[2]):
                    if int(lista[1]) > cantMax:
                        cantMax = int(lista[1])
                else:
                    if int(lista[2]) > cantMax:
                        cantMax = int(lista[2])

                listFechas.append(str(lista[0]))

                tupleFecha.append(str(lista[0])) #+= str(lista[0])
                tupleCompra.append(int(lista[1]))
                tupleVenta.append(int(lista[2]))
                i = i + 1

            generateGraphic = []
            tdFecha = ""
            trCantFechas = ""

            betweenCant = int(cantMax/12)
            listRange = []
            for i in range(0, cantMax, betweenCant):
                listRange.append(i)
                tdFecha = ""
                for lista in self.listFinal:

                    if i < int(lista[1]):
                        tdCantCompra = """
                                            <td width="50" style=" background-color: red;">
                                            </td>
                                       """
                    else:
                        tdCantCompra = """
                                            <td width="50">
                                            </td>
                                       """

                    if i < int(lista[2]):
                        tdCantVenta = """
                                            <td width="50" style=" background-color: blue;">
                                            </td>
                                      """
                    else:
                       tdCantVenta = """
                                            <td width="50">
                                            </td>
                                      """

                    tdFecha += tdCantCompra + tdCantVenta

                tr = """
                        <tr>
                            <td width="60">
                                """+ str(i) +"""
                            </td>
                            """+ str(tdFecha) +"""
                        </tr>
                     """

                generateGraphic.append(tr)


            n_groups = len(tupleFecha)

            fig, ax = pyplot.subplots()

            index = np.arange(n_groups)
            bar_width = 0.20

            opacity = 0.4
            error_config = {'ecolor': '0.3'}

            rects1 = pyplot.bar(index, tupleVenta, bar_width,
                             alpha=opacity,
                             color='b',
                             error_kw=error_config,
                             label='Venta')

            rects2 = pyplot.bar(index + bar_width, tupleCompra, bar_width,
                             alpha=opacity,
                             color='r',
                             error_kw=error_config,
                             label='Compra')

            pyplot.xlabel('Fecha')
            pyplot.ylabel('Cantidad')
            pyplot.title('Cantidad por fechas')
            pyplot.xticks(index + bar_width, tupleFecha)
            pyplot.legend()

            pyplot.tight_layout()
            pyplot.savefig('../archivos/picture1.png')

            trFechas = """<tr> <td width="60">CANT/FECHAS</td>"""
            for fecha in listFechas:
                tdFecha = """<td width="50" align="right" font-size="8"> """+ str(fecha) +"""</td> <td width="50"> </td> """
                trFechas += tdFecha

            trFechas += "</tr>"

            generateGraphic.reverse()

            generateGraphic.append(trFechas)

            finalGraphic = ""

            for graphic in generateGraphic:
                finalGraphic += graphic


            contenido = """
                         <table width="600" height="0" style="border-color: black; border-width: 0.5px; border-spacing: 0;">
                              <tr  style=" background-color: gray; border-style: inset;">
                                <td width="60%"  align="center" valign="middle">
                                    <b>
                                    FECHA
                                    </b>
                                </td>
                                <td width="20%"  align="center" valign="middle" style=" background-color: red;">
                                    <b>
                                        PRODUCTOS COMPRADOS
                                    </b>
                                </td>
                                <td width="20%"  align="center" valign="middle" style="background-color: blue;">
                                    <b>
                                        PRODUCTOS VENDIDOS
                                    </b>
                                </td>
                              </tr>
                          </table>

                          <br>
                          <br>
                          <br>

                          <table width="600" height="0" style="border-color: black; border-width: 0.5px; border-spacing: 0;">
                                """ + listTable + """
                          </table>
                            <br>
                            <br>

                            <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>



                          <br><br><br><br><br><br><br>
                          <IMG SRC="../archivos/picture1.png" width="600" height="600">
                          <br><br><br><br><br><br><br><br><br><br>
                            <br>

                            <hr>
                            <br>
                            <table width="600">
                                <tr>
                                    <td align="right" width="100%">
                                    FECHA/HORA : """+ fecha + """
                                    </td>
                                </tr>
                            </table>
                           <hr>
                        """

            self.generatePDF(contenido)


    def clickHoy_stock(self):
        if self.winPrincipal.chbHoy_stock.isChecked() == True:
            self.winPrincipal.deHasta_stock.setEnabled(False)
            hoy = datetime.datetime.now().date()
            self.winPrincipal.deHasta_stock.setDate(hoy)
        else:
            self.winPrincipal.deHasta_stock.setEnabled(True)

    def clickHoy_saldos(self):
        if self.winPrincipal.chbHoy_saldos.isChecked() == True:
            self.winPrincipal.deHasta_saldos.setEnabled(False)
            hoy = datetime.datetime.now().date()
            self.winPrincipal.deHasta_saldos.setDate(hoy)
        else:
            self.winPrincipal.deHasta_saldos.setEnabled(True)

    def clickHoy_dinero(self):
        if self.winPrincipal.chbHoy_dinero.isChecked() == True:
            self.winPrincipal.deHasta_dinero.setEnabled(False)
            hoy = datetime.datetime.now().date()
            self.winPrincipal.deHasta_dinero.setDate(hoy)
        else:
            self.winPrincipal.deHasta_dinero.setEnabled(True)

    def generarSaldos(self):
        validate = True
        if self.winPrincipal.chbTodos_saldos.isChecked() == False:
            if self.winPrincipal.rbProveedores_saldos.isChecked() == True:
                if self.proveedores is None:
                    validate = False
            else:
                if self.clientes is None:
                    validate = False

        if validate == True:
            if self.winPrincipal.chbTodos_saldos.isChecked() == True:
                if self.winPrincipal.rbProveedores_saldos.isChecked() == True:
                    listProveedores = self.conexionesGenerales.selectProveedor('')
                    contenido = ""
                    for proveedores in listProveedores:
                        self.proveedores = Proveedor()
                        self.proveedores.setIdProveedor(int(proveedores[0]))
                        self.proveedores.setDescripcion(str(proveedores[1]))
                        self.proveedores.setNombre(str(proveedores[2]))

                        contenido += self.generateTable('PROVEEDOR', self.proveedores)
                else:
                    listClientes = self.conexionesGenerales.selectCliente('')
                    contenido = ""
                    for clientes in listClientes:
                        self.clientes = Cliente()
                        self.clientes.setIdCliente(int(clientes[0]))
                        self.clientes.setApellido(str(clientes[1]))
                        self.clientes.setNombre(str(clientes[2]))

                        contenido += self.generateTable('CLIENTE', self.clientes)
            else:
                if self.winPrincipal.rbProveedores_saldos.isChecked() == True:
                    contenido = self.generateTable('PROVEEDOR', self.proveedores)
                else:
                    contenido = self.generateTable('CLIENTE', self.clientes)


            self.generatePDF(contenido)
        else:
            alert = QDialog()
            confirm = QMessageBox.question(alert, "Mensaje", "Falta selecciona la/s persona/s.", QMessageBox.Ok)




    def generateTable(self, type, persona):

        intervalo = 'month'
        if self.winPrincipal.cbIntervalo_saldos.currentText() == 'Semana':
            intervalo = 'week'
        elif self.winPrincipal.cbIntervalo_saldos.currentText() == 'Año':
            intervalo = 'year'
        elif self.winPrincipal.cbIntervalo_saldos.currentText() == 'Dia':
            intervalo = 'day'


        auxDesde = self.winPrincipal.deDesde_saldos.text()

        desde = auxDesde[6:10] + '-' + auxDesde[3:5] + '-' + auxDesde[0:2]

        auxHasta = self.winPrincipal.deHasta_saldos.text()
        hasta = auxHasta[6:10] + '-' + auxHasta[3:5] + '-' + auxHasta[0:2]

        listTransacciones = []
        listPagos = []
        #Total de los pagos
        pagosTotal = 0
        #Total de las transacciones en estado 0
        transaccionesTotal = 0
        total = 0
        #Lista completa (transacciones + pagos)
        listDetalle = []
        apellido = ''
        if type == "CLIENTE":
            listPagos = self.conexionesGenerales.selectListPagosCliente(persona, intervalo, desde, hasta)
            listTransacciones = self.conexionesGenerales.selectListTransaccionCliente(persona, intervalo, desde, hasta)


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
            apellido = persona.getApellido()
        elif type == "PROVEEDOR":
            listPagos = self.conexionesGenerales.selectListPagosProveedor(persona, intervalo, desde, hasta)
            listTransacciones = self.conexionesGenerales.selectListTransaccionProveedor(persona, intervalo, desde, hasta)

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
            apellido = persona.getDescripcion()


        listDetalle.sort()
        listTable = ""
        for lista in listDetalle:
                listTable += """
                                            <tr height="80">
                                                <td width="60%" align="left" >
                                                <br>""" + str(lista[0])  + """<br>
                                                </td>
                                                <td width="20%" align="right">
                                                    <br> &nbsp;&nbsp;""" + str(lista[1])  + """<br>
                                                </td>
                                                <td width="20%" align="center">
                                                   <br>&nbsp;&nbsp; """ + str(lista[2])  + """<br>
                                                </td>
                                            </tr>
                                       """

        contenido = """
                            <br>
                            <br>
                          <table width="600" height="100">
                            <tr>
                                <br> Nombre : """+ persona.getNombre() +""" <br>
                                Apellido : """ + apellido + """<br>
                            </tr>
                          </table>
                          <table width="600"  >
                                <tr height="80" style=" background-color: gray; border-style: inset;">
                                    <td width="60%" align="center" >
                                        <br>FECHA<br>
                                        </td>
                                        <td width="20%" align="center">
                                            <br> MONTO <br>
                                        </td>
                                        <td width="20%" align="center">
                                           <br>ACCION<br>
                                        </td>
                                </tr>
                                """ + listTable + """
                          </table>

                          <table width="600" height="0" style="border-color: black; border-width: 0.5px; border-spacing: 0;">
                            <tr>
                                <td width="70%"><br>SALDO..............<br></td>
                                <td><br> $ """ + str("{0:.2f}".format(total))+ """ <br></td>
                            </tr>
                          </table>
                          <br>
                          <br>
                          <br>
                          <br>
                          <br>
                          <br>
                          <br>
                            <br>
                    """

        return contenido



    def buscarPersonas(self):
         if self.winPrincipal.txtFilterPersona_saldos.hasFocus() is True:
            self.cargarTablaSaldos()



    def cargarTablaSaldos(self):

        parameter = self.winPrincipal.txtFilterPersona_saldos.text()

        if self.winPrincipal.rbProveedores_saldos.isChecked() is True:
            listaProveedores = self.conexionesGenerales.selectProveedor(parameter)

            if len(listaProveedores) > 0:
                header = ['ID','Apellido','Nombre']
                self.tablaModel = MyTableModel(self.winPrincipal.tvPersonas_saldos, listaProveedores, header)
                self.winPrincipal.tvPersonas_saldos.setModel(self.tablaModel)
                self.winPrincipal.tvPersonas_saldos.selectionModel().currentChanged.connect(self.changeSelectedTable)


                self.winPrincipal.tvPersonas_saldos.setColumnHidden(0, True)
                self.winPrincipal.tvPersonas_saldos.setColumnWidth(1, 120)
                self.winPrincipal.tvPersonas_saldos.setColumnWidth(2, 120)
        else:
            listaClientes = self.conexionesGenerales.selectCliente(parameter)

            if len(listaClientes) > 0:
                header = ['ID','Apellido','Nombre']
                self.tablaModel = MyTableModel(self.winPrincipal.tvPersonas_saldos, listaClientes, header)
                self.winPrincipal.tvPersonas_saldos.setModel(self.tablaModel)
                self.winPrincipal.tvPersonas_saldos.selectionModel().currentChanged.connect(self.changeSelectedTable)


                self.winPrincipal.tvPersonas_saldos.setColumnHidden(0, True)
                self.winPrincipal.tvPersonas_saldos.setColumnWidth(1, 120)
                self.winPrincipal.tvPersonas_saldos.setColumnWidth(2, 120)



    def changeSelectedTable(self, selected, deselected):
        if self.winPrincipal.rbProveedores_saldos.isChecked() is True:
            proveedorList = selected.model().mylist
            proveedorSelected = proveedorList[selected.row()]

            self.proveedores = Proveedor()

            self.proveedores.setIdProveedor(int(proveedorSelected[0]))
            self.proveedores.setDescripcion(str(proveedorSelected[1]))
            self.proveedores.setNombre(str(proveedorSelected[2]))
        else:
            clienteList = selected.model().mylist
            clienteSelected = clienteList[selected.row()]

            self.clientes = Cliente()

            self.clientes = Cliente()
            self.clientes.setIdCliente(int(clienteSelected[0]))
            self.clientes.setApellido(str(clienteSelected[1]))
            self.clientes.setNombre(str(clienteSelected[2]))

    def changePersona(self):
        self.clientes = None
        self.proveedores = None

        self.winPrincipal.txtFilterPersona_saldos.setText('')
        self.winPrincipal.tvPersonas_saldos.setModel(None)

    def clickTodos(self):
        if self.winPrincipal.chbTodos_saldos.isChecked() == True:
            self.winPrincipal.txtFilterPersona_saldos.setEnabled(False)
            self.winPrincipal.tvPersonas_saldos.setModel(None)
        else:
            self.winPrincipal.txtFilterPersona_saldos.setEnabled(True)


    def generatePDF(self, contenido):
        hoy = str(datetime.datetime.now().year) + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + str(datetime.datetime.now().hour) + str(datetime.datetime.now().minute) + str(datetime.datetime.now().second)

        nombrePdf = '../archivos/' + str(hoy + 'LIST') + '.pdf'

        fecha = str(datetime.datetime.now())

        html =  """
                     <table width="600">
                        <tr width="600" color="#000000">
                            <td width="80%">

                            </td>
                            <td width="20%" align="right">
                                <IMG SRC="kde1.png">
                            </td>
                        </tr>

                    </table>

                   <hr>
                    <br>
                    <p>
                        SALDOS
                    </p>
                    <br>

                  """+ contenido

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


