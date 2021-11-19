'''
Fichero de eventos generales
'''
import os.path
import shutil
import sys
import zipfile

import xlrd as xlrd
from PyQt5.QtWidgets import QMessageBox

import conexion
from window import *
from datetime import date, datetime
from zipfile import ZipFile
from PyQt5 import QtPrintSupport
import var


class Eventos():
    SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

    def Salir(self):
        try:
            var.dlgaviso.show()
            if var.dlgaviso.exec():
                sys.exit()
            else:
                var.dlgaviso.hide()
        except Exception as error:
            print('Error en módulo salir ', error)

    def abrircal(self):
        try:
            var.dlgcalendar.show()
        except Exception as error:
            print('Error en modulo abrirCal, ', error)

    def resizeTablaCli(self):
        try:
            header = var.ui.tabClientes.horizontalHeader()
            for i in range(5):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
                if i == 0 or i == 3:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        except Exception as error:
            print("Error en modulo resizeTablaCLi", error)

    def Abrir(self):
        try:
            var.dlgabrir.show()
        except Exception as error:
            print("Error en modulo abrir", error)

    def crearBackup(self):
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%YY.%m.%d.%H.%M.%S')
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
            print('Error crear backup', error)

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
                    bbdd.close()
            conexion.Conexion.cargarTabCli(self)

            # codigo drive

        except Exception as error:
            print('Error Restaurar backup', error)

    def Imprimir(self):
        try:
            #hay que pasarle un algo para imprimir
            printDialog = QtPrintSupport.QPrintDialog()
            if printDialog.exec():
                printDialog.show()
        except Exception as error:
            print('Error Imprimir ', error)

    def ImportarExcel(self):
        try:
            newcli = []
            contador = 0
            option = QtWidgets.QFileDialog.Options()
            ruta_excel = var.dlgabrir.getOpenFileName(None, 'Importar Excel', '', '*.xls', options=option)
            fichero = ''
            if var.dlgabrir.Accepted and ruta_excel != '':
                fichero = ruta_excel[0]
            workbook = xlrd.open_workbook(fichero)
            hoja = workbook.sheet_by_index(0)
            while contador < hoja.nrows:
                for i in range(10):
                    newcli.append(hoja.cell_value(contador + 1, i))

                b = conexion.Conexion.altaCli2(newcli)
                print(newcli)
                conexion.Conexion.cargarTabCli(newcli)
                newcli.clear()
                contador = contador + 1
            if b:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Cliente dado de alta')
                msg.exec()
        except Exception as error:
            print('Error al importar ', error)

    def ExportarDatos(self):
        try:
            conexion.Conexion.exportExcel(self)
            try:
                msgBox = QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Information)
                msgBox.setText("Datos exportados con éxito.")
                msgBox.setWindowTitle("Operación completada")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()
            except Exception as error:
                print('Error en mensaje generado exportar datos ', error)
        except Exception as error:
            print('Error en evento exportar datos ', error)
