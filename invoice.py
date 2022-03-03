'''
Gestion Facturación
'''
import traceback

from PyQt5 import QtSql, QtWidgets, QtCore
import conexion,window, var


class Facturas():

    def buscaCli(self):
        """
        Modulo que se ejecuta con el boton busqueda del cliente. Devuelve datos del cliente para el panel facturación

        """
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
            print('Error buscar cliente en invoice',error, traceback.format_exc())

    def altaFac(self):
        """
        Modulo que a partir del dni da de alta una factura con su numero,fecha. Recarga la tabla facturas y muestra en el label el numero de la factura general
        """
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
            print('Error en altaFac en invoice',error, traceback.format_exc())


    def cargarLineaVenta(self):
        """
        Módulo que carga una linea de venta en la fila de la tabla indicada por index correspondiente a una factura
        :param index:
        :type index:int
        """
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
            var.txtCantidad.editingFinished.connect(conexion.Conexion.cargarLineasVenta)


        except Exception as error:
            print('error en cargarLineaVenta',error, traceback.format_exc())

    def procesoVenta(self):
        """

        Módulo que carga el precio del articulo al seleccionarlo en el combo de articulos

        """
        try:
            row = var.ui.tabVentas.currentRow()
            articulo = var.cmbProducto.currentText()
            dato = conexion.Conexion.obtenerCodPrecio(articulo)
            var.ui.tabVentas.setItem(row, 2, QtWidgets.QTableWidgetItem(str(dato[1])))
            var.ui.tabVentas.item(row, 2).setTextAlignment(QtCore.Qt.AlignCenter)
            var.precio = dato[1].replace('€', '')


        except Exception as error:
            print('error en procesoVenta en invoice',error, traceback.format_exc())

    def totalLineaVenta():
        """

        Módulo que al anotar la cantidad de producto, indica el total del precio de la venta realizada.
        Al mismo tiempo recarga la tabla de lineas de venta incluyendo las anteriores y la realizada

        """
        try:
            row = var.ui.tabVentas.currentRow()
            cantidad = round(float(var.txtCantidad.text().replace(',', '.')), 2)
            total_linea = round(float(var.precio) * float(cantidad), 2)
            var.ui.tabVentas.setItem(row, 4, QtWidgets.QTableWidgetItem(str('{:.2f}'.format(total_linea)) + '€'))
            var.ui.tabVentas.item(row, 4).setTextAlignment(QtCore.Qt.AlignRight)
            venta = []
            codfac = var.ui.lblnumFac.text()
            venta.append(int(codfac))
            venta.append(int(var.codpro))
            venta.append(float(var.precio))
            venta.append(float(cantidad))
            print(venta)
            conexion.Conexion.cargarVenta(venta)
        except Exception as error:
            print('error en totalLineaVenta en invoice',error, traceback.format_exc())

    def vaciarTabVentas(self=None):
        """
        Método que vacía la tabla y los campos referentes a las lineas de venta en la interfaz para futuras operaciones.
        """
        try:
            var.ui.tabVentas.clearContents()
            var.cmbProducto = QtWidgets.QComboBox()
            var.txtCantidad = QtWidgets.QLineEdit()
            #var.txtCantidad.editingFinished.connect(Facturas.totalLineaVenta)
            var.cmbProducto.currentIndexChanged.connect(Facturas.procesoVenta)
            Facturas.cargarLineaVenta(self)
            var.ui.lblSubtotal.setText('')
            var.ui.lblIva.setText('')
            var.ui.lblTotal.setText('')
        except Exception as error:
            print('Error en vaciarTabVentas: ',error, traceback.format_exc())
