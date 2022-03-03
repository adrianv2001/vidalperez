import os.path, shutil, sys, zipfile, xlrd, conexion, var
import traceback

from PyQt5.QtWidgets import QMessageBox
from window import *
from datetime import date, datetime
from PyQt5 import QtPrintSupport


class Eventos():

    def salir(self):
        try:
            var.dlgaviso.show()
            if var.dlgaviso.exec():
                sys.exit()
            else:
                var.dlgaviso.hide()
        except Exception as error:
            print('Error en módulo salir ',error, traceback.format_exc())

    def abrircal(self):
        try:
            var.dlgcalendar.show()
        except Exception as error:
            print('Error en modulo abrirCal, ',error, traceback.format_exc())

    def Abrir(self):
        try:
            var.dlgabrir.show()
        except Exception as error:
            print("Error en modulo abrir",error, traceback.format_exc())

    def crearBackup(self):
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y.%m.%d.%H.%M.%S')
            var.copia = (str(fecha) + '_backup.zip')
            option = QtWidgets.QFileDialog.Options()
            directorio, filename = var.dlgabrir.getSaveFileName(None, 'Guardar Copia', var.copia, '.zip',
                                                                options=option)
            if var.dlgabrir.Accepted and filename != '':
                fichzip = zipfile.ZipFile(var.copia, 'w')
                fichzip.write(var.filedb, os.path.basename(var.filedb), zipfile.ZIP_DEFLATED)
                fichzip.close()
                shutil.move(str(var.copia), str(directorio))
        except Exception as error:
            print('Error crear backup',error, traceback.format_exc())

    def restaurarBackup(self):
        try:
            dirpro = os.getcwd()
            dirpro.join('\\')
            option = QtWidgets.QFileDialog.Options()
            filename = var.dlgabrir.getOpenFileName(None, 'Restaurar Copia', '', '*.zip', options=option)
            if var.dlgabrir.Accepted and filename != '':
                file = filename[0]
                with zipfile.ZipFile(str(file), 'r') as bbdd:
                    bbdd.extractall()
                    #bbdd.close()
            conexion.Conexion.db_connect(var.filedb)
            conexion.Conexion.cargarTabCli(self)

        except Exception as error:
            print('Error Restaurar backup',error, traceback.format_exc())

    def Imprimir(self):
        try:
            # hay que pasarle un algo para imprimir
            printDialog = QtPrintSupport.QPrintDialog()
            if printDialog.exec():
                printDialog.show()
        except Exception as error:
            print('Error Imprimir ',error, traceback.format_exc())

    def ImportarExcel(self):

        try:
            option = QtWidgets.QFileDialog.Options()
            filename = var.dlgabrir.getOpenFileName(None, 'Importar archivo .xls', '', '*.xls;;All Files',
                                                    options=option)
            if var.dlgabrir.Accepted and filename != '':
                wb = xlrd.open_workbook(filename[0])
                sheet = wb.sheet_by_index(0)
                COL_FECHA_ALTA = 1
                COL_MUNICIPIO = 5
                for row in range(1, sheet.nrows):
                    cliente = []
                    for col in range(sheet.ncols):
                        # mantener el orden en la base de datos, en la hoja de cálculo no están estas columnas...
                        if col == COL_FECHA_ALTA or col == COL_MUNICIPIO:
                            cliente.append('')
                        cliente.append(sheet.cell_value(row, col))
                    cliente.append('')
                    cliente.append('')
                    print(cliente)# para pago
                    conexion.Conexion.altaCli(cliente,False)
                conexion.Conexion.cargarTabCli(self)

        except Exception as error:
            print('Error importExcel ',error, traceback.format_exc())

    def ExportarDatos(self):
        try:
            conexion.Conexion.exportExcel(self)
            msgBox = QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Information)
            msgBox.setText("Datos exportados con éxito.")
            msgBox.setWindowTitle("Operación completada")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

        except Exception as error:
            print('Error en evento exportar datos ',error, traceback.format_exc())

    def resizeTablaCli(self):
        try:
            header = var.ui.tabClientes.horizontalHeader()
            for i in range(5):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
                if i == 0 or i == 3:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        except Exception as error:
            print("Error en modulo resizeTablaCLi",error, traceback.format_exc())

    def resizeTablaArt(self):
        try:
            header = var.ui.tabArticulos.horizontalHeader()
            for i in range(3):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        except Exception as error:
            print("Error en modulo resizeTablaArt",error, traceback.format_exc())

    def resizeTablaFac(self):
        try:
            header = var.ui.tabFacturas.horizontalHeader()
            for i in range(3):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

        except Exception as error:
            print("Error en modulo resizeTablaFac",error, traceback.format_exc())

    def resizeTablaVen(self):
        try:
            header = var.ui.tabVentas.horizontalHeader()
            for i in range(5):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
                if i == 1 or i == 3:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

        except Exception as error:
            print('Error al redimensionar tabla clientes',error, traceback.format_exc())
