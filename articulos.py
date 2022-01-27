import conexion
import var
import locale
locale.setlocale( locale.LC_ALL, '' )


class Productos():




    def altaPro(self):
        try:
            registro = []
            producto = var.ui.txtNombreArt.text()
            producto = producto.title()
            registro.append(producto)
            precio = var.ui.txtPrecioArt.text()
            precio = precio.replace(',', '.') #necesita estar con punto como en américa
            precio = locale.currency(float(precio))
            registro.append(precio)
            conexion.Conexion.altaArt(registro)
            conexion.Conexion.cargarTabPro(self)

        except Exception as error:
            print('Error en alta productos: ', error)


    def limpiarFormPro(self):
        try:
            var.ui.txtNombreArt.setText('')
            var.ui.txtPrecioArt.setText('')
        except Exception as error:
            print('Error en Limpiar Tabla Articulos',error)


    def cargaArt(self):
        try:

            Productos.limpiarFormPro(self)
            fila = var.ui.tabArticulos.selectedItems()  # seleccionamos la fila
            datos = [var.ui.lblCodigo,var.ui.txtNombreArt, var.ui.txtPrecioArt]

            if fila:
                row = [dato.text() for dato in fila]
            print(row)

            for i, dato in enumerate(datos):
                dato.setText(row[i])

        except Exception as error:
            print('En Articulos, Error en cargar datos de un articulo', error)

    def modifProducto(self):
        try:
            modart = []
            tab = var.ui.tabArticulos
            h = tab.takeItem(0,1).text()

            art = [var.ui.lblCodigo,var.ui.txtNombreArt,var.ui.txtPrecioArt]

            for i in art:
                modart.append(i.text())
            print('modart = ',modart)
            conexion.Conexion.modifPro(modart)
            conexion.Conexion.cargarTabPro(self)

        except Exception as e:
            print("error modificando articulo" + e)

    def bajaArt(row):
        try:
            codigo = var.ui.lblCodigo.text()
            conexion.Conexion.bajaArt(codigo)
            conexion.Conexion.cargarTabPro
        except Exception as error:
            print('error en modulo baja art de articulos', error)
