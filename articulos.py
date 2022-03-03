import traceback

import conexion, var, locale

locale.setlocale(locale.LC_ALL, '')


class Productos():

    def altaPro(self):
        try:
            registro = []
            producto = var.ui.txtNombreArt.text()
            producto = producto.title()
            registro.append(producto)
            precio = var.ui.txtPrecioArt.text()
            precio = precio.replace('€', '')
            precio = precio.replace(',', '.')
            # precio = float(precio)
            # necesita estar con punto como en américa

            precio = float(precio)
            precio = round(precio, 2)
            precio = str(precio)

            registro.append(precio)
            #print(registro)
            conexion.Conexion.altaArt(registro)
            conexion.Conexion.cargarTabPro()

        except Exception as error:
            print('Error en alta productos: ',error, traceback.format_exc())

    def limpiarFormPro(self):
        try:
            var.ui.txtNombreArt.setText('')
            var.ui.txtPrecioArt.setText('')
        except Exception as error:
            print('Error en Limpiar Tabla Articulos',error, traceback.format_exc())

    def cargaArt(self):
        try:
            Productos.limpiarFormPro(self)
            fila = var.ui.tabArticulos.selectedItems()  # seleccionamos la fila
            datos = [var.ui.lblCodigo, var.ui.txtNombreArt, var.ui.txtPrecioArt]
            if fila:
                row = [dato.text() for dato in fila]
            for i, dato in enumerate(datos):
                dato.setText(row[i])

        except Exception as error:
            print('En Productos, Error en cargaArt',error, traceback.format_exc())

    def modifProducto(self):
        try:
            modpro = []
            tab = var.ui.tabArticulos
            h = tab.takeItem(0, 1).text()
            art = [var.ui.lblCodigo, var.ui.txtNombreArt, var.ui.txtPrecioArt]

            for i in art:
                modpro.append(i.text())
            print('modart = ', modpro)
            conexion.Conexion.modifPro(modpro)
            conexion.Conexion.cargarTabPro()

        except Exception as e:
            print("error modificando articulo" + e)

    def bajaArt(row):
        try:
            codigo = var.ui.lblCodigo.text()
            conexion.Conexion.bajaPro(codigo)
            conexion.Conexion.cargarTabPro()
        except Exception as error:
            print('error en modulo baja art de articulos',error, traceback.format_exc())
