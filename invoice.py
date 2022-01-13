'''
Gestion Facturación
'''
from PyQt5 import QtSql, QtWidgets, QtCore

import conexion
import window,var


class Facturas():
    def buscaCli(self):
        try:
            dni = var.ui.txtDNIFac.text().upper()

            var.ui.txtDNIFac.setText(dni)
            registro = conexion.Conexion.buscaCliFac(dni)
            if registro:
                nombre = registro[0]+', '+registro[1]
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

        except Exception as error:
            print('Error en altaFac en invoice', error)

    def cargaFac(self):
        try:
            fila = var.ui.tabFacturas.selectedItems()
            datos = [var.ui.lblnumFac, var.ui.txtFechaFac]
            if fila:
                row = [dato.text() for dato in fila]
            for i,dato in enumerate(datos):
                dato.setText(row[i])
            dni = conexion.Conexion.buscaDNIFac(row[0])
            registro = conexion.Conexion.buscaCliFac(dni)
            if registro:
                nombre = registro[0] + ', ' + registro[1]
                var.ui.lblCliente.setText(nombre)
            var.ui.txtDNIFac.setText(str(dni))
            Facturas.cargaVenta1(self)
        except Exception as error:
            print('error en cargarFac',error)

    def cargarLineaVenta(self):
        try:
            index = 0
            var.cmbProducto = QtWidgets.QComboBox()
            var.txtCantidad = QtWidgets.QLineEdit()
            var.cmbProducto.setFixedSize(180,25)
            var.txtCantidad.setFixedSize(60,25)
            var.txtCantidad.setAlignment(QtCore.Qt.AlignCenter)
            var.ui.tabVentas.setRowCount(index+1)
            var.ui.tabVentas.setCellWidget(index,1, var.cmbProducto)
            var.ui.tabVentas.setCellWidget(index,3, var.txtCantidad)

        except Exception as error:
            print('error en cargarLineaVenta', error)
