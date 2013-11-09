import datetime
from PyQt5.Qt import QDesktopServices, QUrl
from PyQt5.Qt import QTextDocument, QPrinter
from Modelo.persona import Persona

class GenerarPDF():

    def __init__(self):
        self.hoy = str(datetime.datetime.now().year) + str(datetime.datetime.now().month) + \
              str(datetime.datetime.now().day) + str(datetime.datetime.now().hour) + \
              str(datetime.datetime.now().minute) + str(datetime.datetime.now().second)

        self.nombrePdf = ""


    def generateTableTransaction(self, listTable):

        tableHeaderHtml = """
                        <table width="600" height="0" style="border-color: black; border-width: 0.5px; border-spacing: 0;">

                            <tr  style=" background-color: gray; border-style: inset;">
                            <td width="10%"  align="center" valign="middle">
                                <b>
                                CANT
                                </b>
                            </td>
                            <td width="20%"  align="center" valign="middle">
                                <b>
                                    PRODUCTO
                                </b>
                            </td>
                            <td width="50%"  align="center" valign="middle">
                                <b>
                                DESCRIPCION
                                </b>
                            </td>
                            <td width="10%"  align="center" valign="middle">
                                <b>
                                PREC <br>UNIT
                                </b>
                            </td>
                            <td width="10%"  align="center" valign="middle">
                                <b>
                                PREC <br>TOT
                                </b>
                            </td>
                          </tr>
                      </table>
                    """

        rowsHtml = ""
        for transaccion in listTable:
            rowsHtml += """
                            <tr height="80">
                                <td width="10%" align="center" >
                                <br>""" + str(transaccion[1])  + """<br>
                                </td>
                                <td width="20%" >
                                    <br> &nbsp;&nbsp;""" + str(transaccion[3])  + """<br>
                                </td>
                                <td width="50%" >
                                   <br>&nbsp;&nbsp; """ + str(transaccion[4])  + """<br>
                                </td>
                                <td width="10%" align="right" >
                                  <br>  $ """ + str(transaccion[5])  + """&nbsp;&nbsp;<br>
                                </td>
                                <td width="10%" align="right" >
                                  <br>  $ """ + str( int(transaccion[1]) * float(transaccion[5]))  + """&nbsp;&nbsp;<br>
                                </td>
                            </tr>
                        """

        tableDetailHtml = """
                                <table  height="350" width="600" style="border-color: gray; border-width: .4px; border-collapse: collapse;">
                                    """ + rowsHtml + """

                                </table>
                          """




    def generarRecibo(self, listDetail, subName, id, header):
        """

        @param listDetail: lista de detalles
        @param subName: Sub-nombre para generar el PDF
        @param id: Id del recibo
        """
        self.nombrePdf = '../archivos/' + str(self.hoy + subName) + '.pdf'
        listDetalHtml = self.generateTableTransaction(listDetail, header)

        nombre = ""
        apellido = ""

        if(self.tipoTransaccion == "VENTA"):
            nombre = self.cliente.getNombre()
            apellido = self.cliente.getApellido()
        elif(self.tipoTransaccion == "COMPRA"):
            nombre = self.proveedor.getNombre()
            apellido = self.proveedor.getDescripcion()


        total = self.winPrincipal.lblTotal.text()
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
                        DETALLES DE LA COMPRA:
                    </p>
                    <br>
                    <table width="600" height="0" style="border-color: black; border-width: 0.5px; border-spacing: 0;">
                      <tr  style=" background-color: gray; border-style: inset;">
                        <td width="10%"  align="center" valign="middle">
                            <b>
                            CANT
                            </b>
                        </td>
                        <td width="20%"  align="center" valign="middle">
                            <b>
                                PRODUCTO
                            </b>
                        </td>
                        <td width="50%"  align="center" valign="middle">
                            <b>
                            DESCRIPCION
                            </b>
                        </td>
                        <td width="10%"  align="center" valign="middle">
                            <b>
                            PREC <br>UNIT
                            </b>
                        </td>
                        <td width="10%"  align="center" valign="middle">
                            <b>
                            PREC <br>TOT
                            </b>
                        </td>
                      </tr>
                  </table>

                  <br>
                  <br>
                  <br>
                  <br>

                  <table  height="350" width="600" style="border-color: gray; border-width: .4px; border-collapse: collapse;">
                      """ + listTransaccionTable + """
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
                              <br> $ """ + total + """<br>
                            </td>
                        </tr>
                    </table>

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
        #doc.setDefaultStyleSheet(style)
        printer = QPrinter()
        printer.setOutputFileName(nombrePdf)

        printer.setOutputFormat(QPrinter.PdfFormat)
        doc.print(printer)
        printer.newPage()
        url = QUrl
        url = QUrl(nombrePdf)
        QDesktopServices.openUrl(url)


