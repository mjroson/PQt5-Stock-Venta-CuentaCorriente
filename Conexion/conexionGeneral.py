
from Conexion.conexion import Conexion
from Modelo.producto import Producto



class ConexionGenerales(object):

    def __init__(self):
        self.conexion = Conexion()
        self.producto = Producto()


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