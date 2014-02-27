from PyQt5 import uic
from Modelo.producto import Producto
from Conexion.conexionList import ConexionList
from Componentes.tableModel import MyTableModel
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QWidget
from PyQt5.Qt import QDesktopServices, QUrl
import datetime
from PyQt5.Qt import QTextDocument, QPrinter


from PyQt5.QtWidgets import QMessageBox, QDialog


class WindowList():

    def __init__(self, type):

        self.winList = uic.loadUi('../Vista/windowList.ui')

        self.producto = Producto()

        self.conexionList= ConexionList()



        self.winList.btnSalir.clicked.connect(self.close)

        self.type = type

        if self.type == 'PROV':
            self.cargarTablaProveedores()
        else:
            self.cargarTablaClientes()


        self.winList.btnGenerarPdf.clicked.connect(self.createList)

        self.winList.exec()



    def cargarTablaClientes(self):
        listTransaccionesCliente = []
        listTransaccionesCliente = list(self.conexionList.selectClientesTransacciones())

        listPagosCliente = self.conexionList.selectClientesPagos()
        self.listFinal = []
        index = 0
        for tCliente in listTransaccionesCliente:

            for pCliente in listPagosCliente:
                if tCliente[0] == pCliente[0]:
                    totDeuda = float(tCliente[3] - pCliente[1])
                    if totDeuda <= 0:
                        #listTransaccionesCliente.remove(index)
                        pass
                    else:
                        clienteAdd = (tCliente[1], tCliente[2], "$ " +"{0:.2f}".format(totDeuda))
                        self.listFinal.append(clienteAdd)

                    break

            index += 1

        if len(self.listFinal) > 0:
            header = ['Apellido', 'Nombre', 'Deuda']
            tableModel = MyTableModel(self.winList.tvList, self.listFinal, header)

            self.winList.tvList.setModel(tableModel)

            self.winList.tvList.setColumnWidth(0, 190)
            self.winList.tvList.setColumnWidth(1, 190)
            self.winList.tvList.setColumnWidth(2, 110)

        else:
            self.winList.tvList.setModel(None)
            self.winList.btnGenerarPdf.setEnabled(False)

    def cargarTablaProveedores(self):
        listTransaccionesProveedore = []
        listTransaccionesProveedore = list(self.conexionList.selectProveedoresTransacciones())

        listPagosProveedor = self.conexionList.selectProveedoresPagos()
        self.listFinal = []
        index = 0
        for tProveedor in listTransaccionesProveedore:

            for pProveedor in listPagosProveedor:
                if tProveedor[0] == pProveedor[0]:
                    totDeuda = float(tProveedor[3] - pProveedor[1])
                    if totDeuda <= 0:
                        #listTransaccionesProveedore.remove(index)
                        pass
                    else:
                        proveedorAdd = (tProveedor[1], tProveedor[2], "$ " +"{0:.2f}".format(totDeuda))
                        self.listFinal.append(proveedorAdd)

                    break

            index += 1

        if len(self.listFinal) > 0:
            header = ['Apellido', 'Nombre', 'Deuda']
            tableModel = MyTableModel(self.winList.tvList, self.listFinal, header)

            self.winList.tvList.setModel(tableModel)

            self.winList.tvList.setColumnWidth(0, 190)
            self.winList.tvList.setColumnWidth(1, 190)
            self.winList.tvList.setColumnWidth(2, 110)

        else:
            self.winList.tvList.setModel(None)
            self.winList.btnGenerarPdf.setEnabled(False)





    def createList(self):
        hoy = str(datetime.datetime.now().year) + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + str(datetime.datetime.now().hour) + str(datetime.datetime.now().minute) + str(datetime.datetime.now().second)

        nombrePdf = '../archivos/' + str(hoy + 'LIST') + '.pdf'
        listTable = ""
        for lista in self.listFinal:
            listTable += """
                                        <tr height="80">
                                            <td width="40%" align="center" >
                                            <br>""" + str(lista[0])  + """<br>
                                            </td>
                                            <td width="40%" >
                                                <br> &nbsp;&nbsp;""" + str(lista[1])  + """<br>
                                            </td>
                                            <td width="20%" >
                                               <br>&nbsp;&nbsp; """ + str(lista[2])  + """<br>
                                            </td>
                                        </tr>
                                   """


        subtitle = "Listado de clientes con deudas : "
        if self.type == 'PROV':
            subtitle = "Listado de deudas a proveedores : "


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
                        """+ subtitle + """
                    </p>
                    <br>
                    <table width="600" height="0" style="border-color: black; border-width: 0.5px; border-spacing: 0;">
                      <tr  style=" background-color: gray; border-style: inset;">
                        <td width="40%"  align="center" valign="middle">
                            <b>
                            APELLIDO
                            </b>
                        </td>
                        <td width="40%"  align="center" valign="middle">
                            <b>
                                NOMBRE
                            </b>
                        </td>
                        <td width="20%"  align="center" valign="middle">
                            <b>
                            DEUDA
                            </b>
                        </td>
                      </tr>
                  </table>

                  <br>
                  <br>

                  <table width="600" height="0" style="border-color: black; border-width: 0.5px; border-spacing: 0;">
                      """ + listTable + """
                  </table>
                    <br>
                    <br>

                    <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
                    <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
                    <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
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






    def close(self):
        alert = QDialog()
        confirm  = QMessageBox.question(alert, "Mensaje", "¿ Desea salir de la ventana de Listado?", QMessageBox.Yes,
             QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.winList.close()
