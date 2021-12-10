'''
Gestion Facturación
'''
import conexion
import window,var

class Facturas():
    def buscaCli(self):
        try:
            dni = var.ui.txtDNIFac.text().upper()

            var.ui.txtDNIFac.setText(dni)
            registro = conexion.Conexion.buscaCliFac(dni)
            nombre = registro[0]+', '+registro[1]
            var.ui.lblCliente.setText(nombre)
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
        except Exception as error:
            print('error en cargarFac',error)
