import unittest

from PyQt5 import QtSql

import conexion
import var


class MyTestCase(unittest.TestCase):
    def test_conexion(self):
        value = conexion.Conexion.db_connect(var.filedb)
        msg = 'Conexion no válida'
        self.assertTrue(value, msg)  #

    def test_fact(self):
        valor = 40.03
        codfac = 91
        try:
            msg = 'Calculos Incorrectos'
            var.subfac = 0.00
            query = QtSql.QSqlQuery()
            query1 = QtSql.QSqlQuery()
            query.prepare('select codventa, codpro, cantidad from ventas where codfac = :codfac')
            query.bindValue(':codfac',codfac)
            if query.exec_():
                while query.next():
                    codpro = query.value(1)
                    cantidad = query.value(2)
                    query1.prepare('select producto, precio from productos where codigo = :codpro')
                    query1.bindValue(':codpro',codpro)
                    if query1.exec_():
                        while query1.next():
                            precio = query.value(1)
                            subtotal = round(float(cantidad) * float(precio),2)
                    var.subfac = round(float(subtotal)+float(var.subfac),2)
            var.iva= round(float(var.subfac) * 0.21, 2)
            var.fac = round(float(var.iva)+float(var.subfac), 2)

        except Exception as error:
            print(error)
        self.assertEqual(round(float(valor),2),round(float(var.fac), 2), msg)  #
    # add assertion here


if __name__ == '__main__':
    unittest.main()
