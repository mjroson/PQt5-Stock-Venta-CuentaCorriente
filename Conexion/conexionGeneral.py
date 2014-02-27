
from Conexion.conexion import Conexion
from Modelo.producto import Producto
from Modelo.proveedor import Proveedor
from Modelo.cliente import Cliente


class ConexionGenerales(object):

    def __init__(self):
        self.conexion = Conexion()
        self.producto = Producto()
        proveedor = Proveedor()
        cliente = Cliente()


    def selectProductoStock(self):

        query = """
                   SELECT idproductos, nombre, cantidad, cant_minima
                   FROM productos
                   WHERE estado = 1 and cantidad BETWEEN 0 and cant_minima
               """

        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query)
        listProductos = self.conexion.cursor.fetchall()

        self.conexion.cerrarConexion()

        return listProductos

    def changeStateProduct(self, producto):
        query ="""
                    UPDATE productos
                    SET estado = '0'
                    WHERE idproductos = %s
               """
        values = producto.getIdProducto()

        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        self.conexion.db.commit()
        self.conexion.cerrarConexion()

    def selectVentasMensuales(self):
        query = """
                    SELECT m.fecha , CAST(SUM(dm.cantidad) AS CHAR)
                    FROM clientes c, movimiento m, tipo_movimiento tm, detalle_movimiento dm
                    WHERE c.idclientes = tm.clientes_idclientes and
                        m.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                        m.idmovimiento = dm.movimiento_idmovimiento
                    GROUP BY month(m.fecha)
                """
        self.conexion.abrirConexion()

        self.conexion.cursor.execute(query)
        listVentasMes = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listVentasMes




    def selectComprasMensuales(self):
        query = """
                    SELECT m.fecha , CAST(SUM(dm.cantidad) AS CHAR)
                    FROM proveedores prov, movimiento m, tipo_movimiento tm, detalle_movimiento dm
                    WHERE prov.idproveedores = tm.proveedores_idproveedores and
                        m.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                        m.idmovimiento = dm.movimiento_idmovimiento
                    GROUP BY month(m.fecha)
                """

        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query)
        listComprasMes = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listComprasMes


    def selectVentasAnuales(self):
        query = """
                    SELECT m.fecha , CAST(SUM(dm.cantidad) AS CHAR)
                    FROM clientes c, movimiento m, tipo_movimiento tm, detalle_movimiento dm
                    WHERE c.idclientes = tm.clientes_idclientes and
                        m.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                        m.idmovimiento = dm.movimiento_idmovimiento
                    GROUP BY year(m.fecha)
                """
        self.conexion.abrirConexion()

        self.conexion.cursor.execute(query)

        listVentasAnuales = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listVentasAnuales

    def selectComprasAnuales(self):
        query = """
                    SELECT m.fecha , CAST(SUM(dm.cantidad) AS CHAR)
                    FROM proveedores prov, movimiento m, tipo_movimiento tm, detalle_movimiento dm
                    WHERE prov.idproveedores = tm.proveedores_idproveedores and
                        m.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                        m.idmovimiento = dm.movimiento_idmovimiento
                    GROUP BY year(m.fecha)
                """

        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query)
        listComprasAnuales = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listComprasAnuales


    def selectVentas(self, intervalo, desde, hasta):
        query = """
                    SELECT CONCAT(CAST(year(m.fecha) AS CHAR) ,"-", CAST("""+intervalo+"""(m.fecha) AS CHAR)) AS fecha,
                           CAST(SUM(dm.cantidad) AS CHAR) as cantidad
                    FROM clientes c, movimiento m, tipo_movimiento tm, detalle_movimiento dm
                    WHERE c.idclientes = tm.clientes_idclientes and
                          m.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                          m.idmovimiento = dm.movimiento_idmovimiento and
						  m.fecha between %s and %s
                    GROUP BY """+ intervalo +"""(m.fecha)
					ORDER BY m.fecha
                """
        values = (desde, hasta)


        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listVentas = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listVentas

    def selectCompras(self, intervalo, desde, hasta):
        query = """
                    SELECT CONCAT(CAST(year(m.fecha) AS CHAR) ,"-", CAST("""+intervalo+"""(m.fecha) AS CHAR)) AS fecha,
                           CAST(SUM(dm.cantidad) AS CHAR) as cantidad
                    FROM proveedores prov, movimiento m, tipo_movimiento tm, detalle_movimiento dm
                    WHERE prov.idproveedores = tm.proveedores_idproveedores and
                          m.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                          m.idmovimiento = dm.movimiento_idmovimiento and
                          m.idmovimiento = dm.movimiento_idmovimiento and
						  m.fecha between %s and %s
                    GROUP BY """+ intervalo +"""(m.fecha)
					ORDER BY m.fecha
                """
        values = (desde, hasta)
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listCompras = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listCompras

    def selectProveedor(self, parameter):
        query ="""
                    SELECT prov.idproveedores, prov.descripcion, p.nombre
                    FROM proveedores prov, personas p
                    WHERE p.idpersonas = prov.personas_idpersonas and
                    prov.descripcion LIKE %s
               """
        param = parameter+ '%'
        values = param
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listProveedor = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listProveedor

    def selectCliente(self, parameter):
        query = """
                    SELECT cli.idClientes, cli.apellido, p.nombre
                    FROM clientes cli, personas p
                    WHERE p.idpersonas = cli.personas_idpersonas and
                            cli.apellido LIKE %s
                """
        param = parameter+ '%'
        values = param
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listCliente = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()
        return listCliente


    def selectListPagosProveedor(self, proveedor, intervalo, desde, hasta):

        selectFecha = ''
        if intervalo == 'day':
            selectFecha = "p.fecha"
        else:
            selectFecha = """CONCAT(CAST(year(p.fecha) AS CHAR) ,"-", CAST("""+intervalo+"""(p.fecha) AS CHAR))"""
        query = """
                    SELECT """+ selectFecha +""" AS fecha , SUM(p.monto), tm.tipo_movimiento
                    FROM proveedores prov, pagos p, tipo_movimiento tm
                    WHERE tm.proveedores_idproveedores = prov.idproveedores and
                        p.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                        prov.idproveedores = %s and
	                    p.fecha between %s and %s
                    GROUP BY """+ intervalo +"""(p.fecha)
					ORDER BY p.fecha
                """
        values = (proveedor.getIdProveedor(), desde, hasta)
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listPagos = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listPagos

    def selectListTransaccionProveedor(self, proveedor, intervalo, desde, hasta):

        selectFecha = ''
        if intervalo == 'day':
            selectFecha = "m.fecha"
        else:
            selectFecha = """CONCAT(CAST(year(m.fecha) AS CHAR) ,"-", CAST("""+intervalo+"""(m.fecha) AS CHAR))"""
        query = """
                    SELECT """+ selectFecha +""" AS fecha,
                    SUM(dm.precio_unitario * dm.cantidad) as monto, tm.tipo_movimiento
                    FROM proveedores prov, movimiento m, tipo_movimiento tm, detalle_movimiento dm
                    WHERE prov.idproveedores = tm.proveedores_idproveedores and
                        m.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                        m.idmovimiento = dm.movimiento_idmovimiento and m.estado = 0 and
                        prov.idproveedores = % s and
	                    m.fecha between %s and %s
                    GROUP BY """+ intervalo +"""(m.fecha)
					ORDER BY m.fecha
                """
        values = (proveedor.getIdProveedor(), desde, hasta)

        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listTransacciones = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listTransacciones

    def selectListPagosCliente(self, cliente, intervalo, desde, hasta):

        selectFecha = ''
        if intervalo == 'day':
            selectFecha = "p.fecha"
        else:
            selectFecha = """CONCAT(CAST(year(p.fecha) AS CHAR) ,"-", CAST("""+intervalo+"""(p.fecha) AS CHAR))"""

        query = """
                    SELECT """+ selectFecha +""" AS fecha, SUM(p.monto), tm.tipo_movimiento
                    FROM clientes c, pagos p, tipo_movimiento tm
                    WHERE tm.clientes_idclientes = c.idclientes and
                        p.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                        c.idclientes = %s and
	                    p.fecha between %s and %s
                    GROUP BY """+ intervalo +"""(p.fecha)
					ORDER BY p.fecha
                """
        values = (cliente.getIdCliente(), desde, hasta)
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listPagos = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listPagos

    def selectListTransaccionCliente(self, cliente, intervalo, desde, hasta):

        selectFecha = ''
        if intervalo == 'day':
            selectFecha = "m.fecha"
        else:
            selectFecha = """CONCAT(CAST(year(m.fecha) AS CHAR) ,"-", CAST("""+intervalo+"""(m.fecha) AS CHAR))"""

        query = """
                    SELECT """+ selectFecha +""" AS fecha,
                    SUM(dm.precio_unitario * dm.cantidad) as monto, tm.tipo_movimiento
                    FROM clientes c, movimiento m, tipo_movimiento tm, detalle_movimiento dm
                    WHERE c.idclientes = tm.clientes_idclientes and
                        m.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                        m.idmovimiento = dm.movimiento_idmovimiento and m.estado = 0 and
                        c.idclientes = %s and
	                    m.fecha between %s and %s
                    GROUP BY """+ intervalo +"""(m.fecha)
					ORDER BY m.fecha
                """
        values = (cliente.getIdCliente(), desde, hasta)
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listTransacciones = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listTransacciones

    def selectEntradasTransacciones(self, intervalo, desde, hasta):
        selectFecha = ''
        if intervalo == 'day':
            selectFecha = "m.fecha"
        else:
            selectFecha = """CONCAT(CAST(year(m.fecha) AS CHAR) ,"-", CAST("""+intervalo+"""(m.fecha) AS CHAR))"""

        query = """
                    SELECT """+ selectFecha +""" AS fecha,
                    SUM(dm.precio_unitario * dm.cantidad) as monto, tm.tipo_movimiento
                    FROM clientes c, movimiento m, tipo_movimiento tm, detalle_movimiento dm
                    WHERE c.idclientes = tm.clientes_idclientes and
                        m.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                        m.idmovimiento = dm.movimiento_idmovimiento and m.estado = 1 and
	                    m.fecha between %s and %s
                    GROUP BY """+ intervalo +"""(m.fecha)
					ORDER BY m.fecha
                """
        values = (desde, hasta)
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listEntradaTransacciones = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listEntradaTransacciones


    def selectSalidaTransacciones(self, intervalo, desde, hasta):
        selectFecha = ''
        if intervalo == 'day':
            selectFecha = "m.fecha"
        else:
            selectFecha = """CONCAT(CAST(year(m.fecha) AS CHAR) ,"-", CAST("""+intervalo+"""(m.fecha) AS CHAR))"""

        query = """
                    SELECT """+ selectFecha +""" AS fecha,
                    SUM(dm.precio_unitario * dm.cantidad) as monto, tm.tipo_movimiento
                    FROM proveedores prov, movimiento m, tipo_movimiento tm, detalle_movimiento dm
                    WHERE prov.idproveedores = tm.proveedores_idproveedores and
                        m.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                        m.idmovimiento = dm.movimiento_idmovimiento and m.estado = 1 and
	                    m.fecha between %s and %s
                    GROUP BY """+ intervalo +"""(m.fecha)
					ORDER BY m.fecha
                """
        values = (desde, hasta)
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listSalidaTransacciones = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listSalidaTransacciones


    def selectEntradaPagos(self, intervalo, desde, hasta):
        selectFecha = ''
        if intervalo == 'day':
            selectFecha = "p.fecha"
        else:
            selectFecha = """CONCAT(CAST(year(p.fecha) AS CHAR) ,"-", CAST("""+intervalo+"""(p.fecha) AS CHAR))"""

        query = """
                    SELECT """+ selectFecha +""" AS fecha , SUM(p.monto), tm.tipo_movimiento
                    FROM clientes c, pagos p, tipo_movimiento tm
                    WHERE tm.clientes_idclientes = c.idclientes and
                        p.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
	                    p.fecha between %s and %s
                    GROUP BY """+ intervalo +"""(p.fecha)
					ORDER BY p.fecha
                """
        values = (desde, hasta)
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listEntradaPagos = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listEntradaPagos

    def selectSalidaPagos(self, intervalo, desde, hasta):
        selectFecha = ''
        if intervalo == 'day':
            selectFecha = "p.fecha"
        else:
            selectFecha = """CONCAT(CAST(year(p.fecha) AS CHAR) ,"-", CAST("""+intervalo+"""(p.fecha) AS CHAR))"""

        query = """
                    SELECT """+ selectFecha +""" AS fecha , SUM(p.monto), tm.tipo_movimiento
                    FROM proveedores prov, pagos p, tipo_movimiento tm
                    WHERE tm.proveedores_idproveedores = prov.idproveedores and
                        p.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
	                    p.fecha between %s and %s
                    GROUP BY """+ intervalo +"""(p.fecha)
					ORDER BY p.fecha
                """
        values = (desde, hasta)
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query, values)
        listSalidaPagos = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listSalidaPagos