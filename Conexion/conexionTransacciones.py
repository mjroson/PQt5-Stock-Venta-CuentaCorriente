from Conexion.conexion import Conexion
from Modelo.cliente import Cliente
from Modelo.proveedor import Proveedor
from Modelo.producto import Producto
import datetime


class ConexionTransacciones(object):

    def __init__(self):
        self.conexion = Conexion()
        self.cliente = Cliente()
        self.proveedor = Proveedor()


    def selectProveedores(self, typeParameter, parameter):
        query = """
                    SELECT prov.idproveedores , prov.descripcion, p.nombre, p.email
                    FROM proveedores prov, personas p
                    WHERE p.idpersonas = prov.personas_idpersonas and prov.estado = 1 and """+ typeParameter +""" LIKE %s
                """
        param = parameter + '%'
        values = param
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listProveedores = self.conexion.cursor.fetchall()

        self.conexion.cerrarConexion()

        return listProveedores

    def selectClientes(self, typeParameter, parameter):
        query = """
                    SELECT c.idclientes, c.apellido, p.nombre, p.email
                    FROM clientes c, personas p
                    WHERE p.idpersonas = c.personas_idpersonas and c.estado = 1 and """+ typeParameter +""" LIKE %s
                """
        param = parameter + '%'
        values = param
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listClientes = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listClientes

    def selectProductos(self, typeParameter, parameter, parameterTransaccion):
        query = """
                    SELECT p.idproductos, p.nombre, p.descripcion, p.cantidad, CAST(TRUNCATE(p.pCompra, 2) AS CHAR), CAST(TRUNCATE(p.pVenta, 2) AS CHAR), m.descripcion
                    FROM productos p, marcas m
                    WHERE p.marcas_idmarcas = m.idmarcas and """ +typeParameter+ """ LIKE %s
                """
        if parameterTransaccion == 'VNT':
            query += " and p.estado = 1 and p.cantidad > 0"

        param = parameter + '%'
        values = param
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, param)
        listProductos = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listProductos

    def cargarTransaccionCompra(self, listMovimiento, proveedor, estado):
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
                            INSERT INTO movimiento (fecha, tipo_movimiento_idtipo_movimiento, estado)
                            VALUES ( %s , %s, %s)
                          """
        valuesMovimiento = (hoy, idTipoMovimiento, estado)

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
            producto = Producto()
            producto.setIdProducto(int(detalleMovimiento[2]))
            producto.setCantidad(int(detalleMovimiento[1]))
            self.modificarStock('CMP', producto)

        self.conexion.cerrarConexion()
        return idMovimiento

    def cargarTransaccionVenta(self: object, listMovimiento, cliente, estado):
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
                            INSERT INTO movimiento (fecha, tipo_movimiento_idtipo_movimiento, estado)
                            VALUES ( %s , %s, %s);
                          """
        valuesMovimiento = (hoy, idTipoMovimiento, estado)

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

            producto = Producto()
            producto.setIdProducto(int(detalleMovimiento[2]))
            producto.setCantidad(int(detalleMovimiento[1]))
            self.modificarStock(tipoT='VNT', producto=producto)

        self.conexion.cerrarConexion()

        return idMovimiento


    def modificarStock(self, tipoT, producto):
        query = """
                    SELECT cantidad
                    FROM productos
                    WHERE idproductos = %s
                """
        values = producto.getIdProducto()
        #self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        cant = 0
        cantInit = int(self.conexion.cursor.fetchall()[0][0])
        #self.conexion.cerrarConexion()
        if tipoT == 'VNT':
            cant = cantInit - producto.getCantidad()
        else:
            cant = cantInit + producto.getCantidad()

        queryUpdateProducto = """
                                UPDATE productos
                                SET cantidad = %s
                                WHERE idproductos = %s
                              """
        valuesUpdateProducto = (cant, producto.getIdProducto())
        #self.conexion.abrirConexion()
        self.conexion.cursor.execute(queryUpdateProducto, valuesUpdateProducto)
        self.conexion.db.commit()
        #self.conexion.cerrarConexion()