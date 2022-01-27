'''
Gestion Facturación
'''
from PyQt5 import QtSql, QtWidgets, QtCore
import conexion
import window, var


class Facturas():
    def buscaCli(self):
        try:
            dni = var.ui.txtDNIFac.text().upper()

            var.ui.txtDNIFac.setText(dni)
            registro = conexion.Conexion.buscaCliFac(dni)
            if registro:
                nombre = registro[0] + ', ' + registro[1]
                var.ui.lblCliente.setText(nombre)
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('No existe el cliente')
        except Exception as error:
            print('Error buscar cliente en invoice', error)

    def altaFac(self):
        try:
            registro = []
            dni = var.ui.txtDNIFac.text().upper()
            registro.append(str(dni))
            fecha = var.ui.txtFechaFac.text()
            registro.append(str(fecha))

            conexion.Conexion.altaFac(registro)
            conexion.Conexion.cargarTabFacturas(self)
            codfac = conexion.Conexion.buscaCodFac(self)
            var.ui.lblnumFac.setText(str(codfac))

        except Exception as error:
            print('Error en altaFac en invoice', error)


    def cargarLineaVenta(self):
        try:
            index = 0
            var.cmbProducto = QtWidgets.QComboBox()
            var.cmbProducto.setFixedSize(180, 25)
            conexion.Conexion.cargarCmbProducto(self)
            var.txtCantidad.setFixedSize(60, 25)
            var.txtCantidad.setAlignment(QtCore.Qt.AlignCenter)
            var.ui.tabVentas.setRowCount(index + 1)
            var.ui.tabVentas.setCellWidget(index, 1, var.cmbProducto)
            var.ui.tabVentas.setCellWidget(index, 3, var.txtCantidad)
            var.cmbProducto.currentIndexChanged.connect(Facturas.procesoVenta)
            codfac = var.ui.lblnumFac.text()
            #var.txtCantidad.returnPressed.connect(invoice.Facturas.totalLineaVenta)
            var.txtCantidad.editingFinished.connect(Facturas.totalLineaVenta)
            var.txtCantidad.editingFinished.connect(conexion.Conexion.cargarLineasVenta(codfac))

        except Exception as error:
            print('error en cargarLineaVenta', error)

    def procesoVenta(self):
        try:
            row = var.ui.tabVentas.currentRow()
            articulo = var.cmbProducto.currentText()
            dato = conexion.Conexion.obtenerCodPrecio(articulo)
            var.ui.tabVentas.setItem(row, 2, QtWidgets.QTableWidgetItem(str(dato[1])))
            var.ui.tabVentas.item(row, 2).setTextAlignment(QtCore.Qt.AlignCenter)
            var.precio = dato[1].replace('€', '')

        except Exception as error:
            print('error en procesoVenta en invoice', error)

    def totalLineaVenta(self = None):
        try:
            venta = []
            row = var.ui.tabVentas.currentRow()
            cantidad = float(var.txtCantidad.text())
            print(cantidad)
            total_linea = round(float(var.precio) * float(cantidad), 2)
            var.ui.tabVentas.setItem(row, 4, QtWidgets.QTableWidgetItem(str(total_linea) + '€'))
            var.ui.tabVentas.item(row, 4).setTextAlignment(QtCore.Qt.AlignRight)
            codfac = var.ui.lblnumFac.text()
            venta.append(int(codfac))
            venta.append(int(var.codpro))
            venta.append(float(var.precio))
            venta.append(float(cantidad))

            print(venta)
            conexion.Conexion.cargarVenta(venta)
        except Exception as error:
            print('error en totalLineaVenta en invoice', error)
