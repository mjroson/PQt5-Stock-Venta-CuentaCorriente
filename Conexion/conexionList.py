__author__ = 'Vicio'
from Conexion.conexion import Conexion


class ConexionList():

    def __init__(self):
        self.conexion = Conexion()



    def selectClientesTransacciones(self):
        query = """
                    SELECT c.idclientes, c.apellido, p.nombre, SUM(dm.precio_unitario * dm.cantidad ) as monto
                    FROM clientes c, movimiento m, tipo_movimiento tm, detalle_movimiento dm, personas p
                    WHERE c.idclientes = tm.clientes_idclientes and
                        m.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                        m.idmovimiento = dm.movimiento_idmovimiento and
                        m.estado = 0 and
                        p.idpersonas = c.personas_idpersonas
                    GROUP BY tm.clientes_idclientes
                    ORDER BY monto desc
                """
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query)
        listClientes = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listClientes


    def selectClientesPagos(self):
        query = """
                    SELECT c.idclientes, SUM(p.monto)
                    FROM clientes c, pagos p, tipo_movimiento tm
                    WHERE tm.clientes_idclientes = c.idclientes and
                        p.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento
                    GROUP BY c.idclientes
                """
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query)
        listClientes = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listClientes


    def selectProveedoresTransacciones(self):
        query = """
                    SELECT prov.idproveedores, prov.descripcion, p.nombre, SUM(dm.precio_unitario * dm.cantidad ) as monto
                    FROM proveedores prov, movimiento m, tipo_movimiento tm, detalle_movimiento dm, personas p
                    WHERE prov.idproveedores = tm.proveedores_idproveedores and
                        m.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento and
                        m.idmovimiento = dm.movimiento_idmovimiento and
                        m.estado = 0 and
                        p.idpersonas = prov.personas_idpersonas
                    GROUP BY tm.proveedores_idproveedores
                    ORDER BY monto desc
                """
        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query)
        listProveedores = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listProveedores

    def selectProveedoresPagos(self):
        query = """
                    SELECT prov.idproveedores, SUM(p.monto)
                    FROM  proveedores prov, pagos p, tipo_movimiento tm
                    WHERE tm.proveedores_idproveedores = prov.idproveedores and
                        p.tipo_movimiento_idtipo_movimiento = tm.idtipo_movimiento
                    GROUP BY prov.idproveedores
                """

        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query)
        listProveedores = self.conexion.cursor.fetchall()
        self.conexion.cerrarConexion()

        return listProveedores

