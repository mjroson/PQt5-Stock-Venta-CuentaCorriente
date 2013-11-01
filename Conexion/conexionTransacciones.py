from Conexion.conexion import Conexion
from Modelo.cliente import Cliente
from Modelo.proveedor import Proveedor
import datetime


class ConexionTransacciones(object):

    def __init__(self):
        self.conexion = Conexion()
        self.cliente = Cliente()
        self.proveedor = Proveedor()


    def selectProveedores(self, tipoParametro, parametro):
        query = """
                    SELECT prov.idproveedores , prov.descripcion, p.nombre, p.email
                    FROM proveedores prov, personas p
                    WHERE p.idpersonas = prov.personas_idpersonas
                """
        values = (tipoParametro, parametro)
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query)
        listProveedores = self.conexion.cursor.fetchall()

        self.conexion.cerrarConexion()

        return listProveedores

    def selectClientes(self, tipoParametro, parametro):
        query = """
                    SELECT c.idclientes, c.apellido, p.nombre, p.email
                    FROM clientes c, personas p
                    WHERE p.idpersonas = c.personas_idpersonas
                """
        values = (tipoParametro, parametro)
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query)
        listClientes = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listClientes

    def selectProductos(self):
        query = """
                    SELECT p.idproductos, p.nombre, p.descripcion, p.cantidad, p.pCompra, p.pVenta, m.descripcion
                    FROM productos p, marcas m
                    WHERE p.marcas_idmarcas = m.idmarcas
                """
        values = ""
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query)
        listProductos = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listProductos

    def cargarTransaccionCompra(self, listMovimiento, proveedor):
        hoy = datetime.datetime.now().date()

        self.conexion.abrirConexion()

        queryTipoMovimiento = """
                                INSERT INTO tipo_movimiento (tipo_movimiento, proveedores_idproveedores)
                                VALUES ('compra', %s)
                              """
        valuesTipoMovimiento = proveedor.getIdProveedor()

        self.conexion.cursor.execute(queryTipoMovimiento, valuesTipoMovimiento)
        self.conexion.db.commit()
        idTipoMovimiento = self.conexion.cursor.lastrowid
        cantRowAffect = self.conexion.cursor.rowcount


        queryMovimiento = """
                            INSERT INTO movimiento (fecha, tipo_movimiento_idtipo_movimiento)
                            VALUES ( %s , %s)
                          """
        valuesMovimiento = (hoy, idTipoMovimiento)

        self.conexion.cursor.execute(queryMovimiento, valuesMovimiento)
        self.conexion.db.commit()
        idMovimiento = self.conexion.cursor.lastrowid
        cantRowAffect = self.conexion.cursor.rowcount


        queryDetalleMovimiento = """
                            INSERT INTO detalle_movimiento (cantidad, precio_unitario, productos_idproductos,
                                movimiento_idMovimiento)
                            VALUES (%s, %s , %s, %s)
                           """
        for detalleMovimiento in listMovimiento:
            valuesDetalleMovimiento = (detalleMovimiento[1], detalleMovimiento[5], detalleMovimiento[2], idMovimiento)
            self.conexion.cursor.execute(queryDetalleMovimiento, valuesDetalleMovimiento)
            self.conexion.db.commit()
            lastId = self.conexion.cursor.lastrowid
            cantRowAffect = self.conexion.cursor.rowcount

        self.conexion.cerrarConexion()
        return idMovimiento

    def cargarTransaccionVenta(self, listMovimiento, cliente):
        hoy = datetime.datetime.now().date()

        self.conexion.abrirConexion()

        queryTipoMovimiento = """
                                INSERT INTO tipo_movimiento (tipo_movimiento, clientes_idClientes)
                                VALUES ('venta', %s)
                              """
        valuesTipoMovimiento = cliente.getIdCliente()

        self.conexion.cursor.execute(queryTipoMovimiento, valuesTipoMovimiento)
        self.conexion.db.commit()
        idTipoMovimiento = self.conexion.cursor.lastrowid
        cantRowAffect = self.conexion.cursor.rowcount


        queryMovimiento = """
                            INSERT INTO movimiento (fecha, tipo_movimiento_idtipo_movimiento)
                            VALUES ( %s , %s);
                          """
        valuesMovimiento = (hoy, idTipoMovimiento)

        self.conexion.cursor.execute(queryMovimiento, valuesMovimiento)
        self.conexion.db.commit()
        idMovimiento = self.conexion.cursor.lastrowid
        cantRowAffect = self.conexion.cursor.rowcount


        queryDetalleMovimiento = """
                            INSERT INTO detalle_movimiento (cantidad, precio_unitario, productos_idproductos,
                                movimiento_idMovimiento)
                            VALUES (%s, %s , %s, %s)
                           """
        for detalleMovimiento in listMovimiento:
            valuesDetalleMovimiento = (detalleMovimiento[1], detalleMovimiento[5], detalleMovimiento[2], idMovimiento)
            self.conexion.cursor.execute(queryDetalleMovimiento, valuesDetalleMovimiento)
            self.conexion.db.commit()
            lastId = self.conexion.cursor.lastrowid
            cantRowAffect = self.conexion.cursor.rowcount

        self.conexion.cerrarConexion()

        return idMovimiento


    def modificarStock(self, tipoT, producto):
        pass

