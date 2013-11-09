from Conexion.conexion import Conexion
from Modelo.cliente import Cliente
from Modelo.proveedor import Proveedor
import datetime


class ConexionPagos(object):

    def __init__(self):
        self.conexion = Conexion()
        self.cliente = Cliente()
        self.proveedor = Proveedor()


    def selectProveedores(self, tipoParametro, parametro):
        query = """
                    SELECT prov.idproveedores , prov.descripcion, p.nombre, p.email
                    FROM proveedores prov, personas p
                    WHERE p.idpersonas = prov.personas_idpersonas and prov.estado = 1 and
                    """ + tipoParametro + """ LIKE %s
                """
        parametro = parametro + '%'
        values = parametro
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listProveedores = self.conexion.cursor.fetchall()

        self.conexion.cerrarConexion()

        return listProveedores


    def selectClientes(self, tipoParametro, parametro):
        query = """
                    SELECT c.idclientes, c.apellido, p.nombre, p.email
                    FROM clientes c, personas p
                    WHERE p.idpersonas = c.personas_idpersonas and c.estado = 1 and
                    """+ tipoParametro + """ LIKE %s
                """
        parametro = parametro + '%'
        values = parametro
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listClientes = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listClientes


    def selectListPagosProveedor(self, proveedor):
        query = """
                    SELECT p.fecha, p.monto, tm.tipo_movimiento
                    FROM proveedores prov, pagos p, tipo_movimiento tm
                    WHERE tm.proveedores_idproveedores = prov.idproveedores and
                        p.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                        prov.idproveedores = %s
                """
        values = proveedor.getIdProveedor()
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listPagos = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listPagos

    def selectListTransaccionProveedor(self, proveedor):
        query = """
                    SELECT m.fecha, SUM(dm.precio_unitario * dm.cantidad) as monto, tm.tipo_movimiento
                    FROM proveedores prov, movimiento m, tipo_movimiento tm, detalle_movimiento dm
                    WHERE prov.idproveedores = tm.proveedores_idproveedores and
                        m.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                        m.idmovimiento = dm.movimiento_idmovimiento and m.estado = 0 and
                        prov.idproveedores = %s
                    GROUP BY m.fecha
                """
        values = proveedor.getIdProveedor()

        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listTransacciones = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listTransacciones

    def selectListPagosCliente(self, cliente):
        query = """
                    SELECT p.fecha, p.monto, tm.tipo_movimiento
                    FROM clientes c, pagos p, tipo_movimiento tm
                    WHERE tm.clientes_idclientes = c.idclientes and
                        p.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                        c.idclientes = %s
                """
        values = cliente.getIdCliente()
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listPagos = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listPagos

    def selectListTransaccionCliente(self, cliente):
        query = """
                    SELECT m.fecha, SUM(dm.precio_unitario * dm.cantidad) as monto, tm.tipo_movimiento
                    FROM clientes c, movimiento m, tipo_movimiento tm, detalle_movimiento dm
                    WHERE c.idclientes = tm.clientes_idclientes and
                        m.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                        m.idmovimiento = dm.movimiento_idmovimiento and m.estado = 0 and
                        c.idclientes = %s
                    GROUP BY m.fecha
                """
        values = cliente.getIdCliente()

        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listTransacciones = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listTransacciones

    def cargarCobranza(self, cliente, monto):
        hoy = datetime.datetime.now().date()

        self.conexion.abrirConexion()

        queryTipoMovimiento = """
                                INSERT INTO tipo_movimiento (tipo_movimiento, clientes_idclientes)
                                VALUES ('pago', %s)
                              """
        valuesTipoMovimiento = cliente.getIdCliente()

        self.conexion.cursor.execute(queryTipoMovimiento, valuesTipoMovimiento)
        self.conexion.db.commit()
        idTipoMovimiento = self.conexion.cursor.lastrowid
        cantRowAffect = self.conexion.cursor.rowcount
        self.conexion.cerrarConexion()

        queryPagos = """
                            INSERT INTO pagos (fecha, monto, tipo_movimiento_idtipo_movimiento)
                            VALUES (%s, %s, %s);

                          """
        valuesPagos = (hoy, monto, idTipoMovimiento)
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(queryPagos, valuesPagos)
        self.conexion.db.commit()
        idRecibo = self.conexion.cursor.lastrowid
        self.conexion.cerrarConexion()

        return idRecibo

    def cargarPago(self, proveedor, monto):
        hoy = datetime.datetime.now().date()

        self.conexion.abrirConexion()

        queryTipoMovimiento = """
                                INSERT INTO tipo_movimiento (tipo_movimiento, proveedores_idproveedores)
                                VALUES ('pago', %s)
                              """
        valuesTipoMovimiento = proveedor.getIdProveedor()

        self.conexion.cursor.execute(queryTipoMovimiento, valuesTipoMovimiento)
        self.conexion.db.commit()
        idTipoMovimiento = self.conexion.cursor.lastrowid
        cantRowAffect = self.conexion.cursor.rowcount


        queryPagos = """
                            INSERT INTO pagos (fecha, monto, tipo_movimiento_idtipo_movimiento)
                            VALUES (%s, %s, %s);

                          """
        valuesPagos = (hoy, monto, idTipoMovimiento)

        self.conexion.cursor.execute(queryPagos, valuesPagos)
        self.conexion.db.commit()
        idRecibo = self.conexion.cursor.lastrowid
        self.conexion.cerrarConexion()

        return idRecibo