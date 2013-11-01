
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
                   WHERE cantidad = cant_minima or cantidad < cant_minima and estado = 1
               """

        self.conexion.abrirConexion()
        self.conexion.cursor.execute(query)
        listProductos = self.conexion.cursor.fetchall()

        self.conexion.cerrarConexion()

        return listProductos