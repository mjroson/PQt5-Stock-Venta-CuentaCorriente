import sys

from PyQt5 import uic
from Modelo.producto import Producto
from Conexion.conexionGeneral import ConexionGenerales
from Componentes.tableModel import MyTableModel
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QWidget
from PyQt5.Qt import QDesktopServices, QUrl
import datetime
from PyQt5.Qt import QTextDocument, QPrinter
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


        self.winNot.btnDesactivar.setEnabled(False)
        self.winNot.btnGenerarPdf.clicked.connect(self.generateList)

        self.winNot.exec()


        #sys.executable(self.winNot.exec_())


    def cargarTabla(self):
        self.listProducto = self.conexionGeneral.selectProductoStock()

        header = ['ID', 'Nombre', 'Cant', 'Cant Min']
        if len(self.listProducto) > 0:
            tableModel = MyTableModel(self.winNot.tvDetalle, self.listProducto, header)
            self.winNot.tvDetalle.setModel(tableModel)
            self.winNot.tvDetalle.selectionModel().currentChanged.connect(self.changeSelectedTable)


            self.winNot.tvDetalle.setColumnHidden(0, True)
            self.winNot.tvDetalle.setColumnWidth(1, 128)
            self.winNot.tvDetalle.setColumnWidth(2, 70)
            self.winNot.tvDetalle.setColumnWidth(3, 70)
        else:
            self.winNot.btnGenerarPdf.setEnabled(False)




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


    def generateList(self):
        hoy = str(datetime.datetime.now().year) + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + str(datetime.datetime.now().hour) + str(datetime.datetime.now().minute) + str(datetime.datetime.now().second)

        nombrePdf = '../archivos/' + str(hoy + 'LIST') + '.pdf'
        listTable = ""
        for lista in self.listProducto:
            listTable += """
                                        <tr height="80">
                                            <td width="60%" align="left" >
                                            <br>""" + str(lista[1])  + """<br>
                                            </td>
                                            <td width="20%" align="center">
                                                <br> &nbsp;&nbsp;""" + str(lista[3])  + """<br>
                                            </td>
                                            <td width="20%" align="center">
                                               <br>&nbsp;&nbsp; """ + str(lista[2])  + """<br>
                                            </td>
                                        </tr>
                                   """


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
                        LISTADO DE PRODUCTOS SIN STOCK :
                    </p>
                    <br>
                    <table width="600" height="0" style="border-color: black; border-width: 0.5px; border-spacing: 0;">
                      <tr  style=" background-color: gray; border-style: inset;">
                        <td width="60%"  align="center" valign="middle">
                            <b>
                            PRODUCTOS
                            </b>
                        </td>
                        <td width="20%"  align="center" valign="middle">
                            <b>
                                CANTIDAD MINIMA
                            </b>
                        </td>
                        <td width="20%"  align="center" valign="middle">
                            <b>
                            CANTIDAD
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
