import conexion
import var
from PyQt5 import QtWidgets


class articulos():

    def limpiarFormArt(self):
        try:
            var.ui.txtNombreArt.setText('')
            var.ui.txtPrecioArt.setText('')
        except Exception as error:
            print('Error en Limpiar Tabla Articulos',error)

    def guardarArt(self):
        try:
            newArt = []
            nombreArt = var.ui.txtNombreArt.text()
            precioArt = var.ui.txtPrecioArt.text()

            print(nombreArt)
            print(precioArt)

            newArt.append(nombreArt)
            newArt.append(precioArt)
            print(newArt)
            conexion.Conexion.altaArt(newArt)
            conexion.Conexion.cargaTabArt(self)


        except Exception as error:
            print('Error en guardar articulo',error)

    def cargaArt(self):
        try:

            articulos.limpiarFormArt(self)
            fila = var.ui.tabArticulos.selectedItems()  # seleccionamos la fila
            datos = [var.ui.txtNombreArt, var.ui.txtPrecioArt]

            if fila:
                row = [dato.text() for dato in fila]

            for i, dato in enumerate(datos):
                dato.setText(row[i])

            registro = conexion.Conexion.oneArt(row[0])
            var.ui.txtNombreArt.setText(str(registro[0]))
            var.ui.txtPrecioArt.setCurrentText(str(registro[1]))

        except Exception as error:
            print('En Articulos, Error en cargar datos de un articulo', error)

    def modifArt(self):
        try:
            modart = []
            tab = var.ui.tabArticulos
            h = tab.takeItem(0,1).text()
            print(h)

            art = [var.ui.txtNombreArt,var.ui.txtPrecioArt]


            for i in art:
                modart.append(i.text())


            conexion.Conexion.modificarArt(modart)
            conexion.Conexion.cargarTabCli(self)

        except Exception as e:
            print("error modificando articulo" + e)

    def bajaArt(row):
        try:
            #codigo = var.ui.tabArticulos.text().
            h = var.ui.tabArticulos.selectedItems()[1]
            print(h)
            #var.ui.tabArticulos.setItem(index, 0, QTableWidgetItem(codigo))
            #conexion.Conexion.bajaArt(codigo)
            #conexion.Conexion.cargarTabCli(self)
        except Exception as error:
            print('error en modulo baja art de articulos', error)