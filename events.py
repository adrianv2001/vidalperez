'''
Fichero de eventos generales
'''
import os.path
import shutil
import sys
import zipfile

import conexion
from window import *
from datetime import date, datetime
from zipfile import ZipFile
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
            print('Error en módulo salir ',error)

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
            var.copia = (str(fecha)+'_backup.zip')
            option = QtWidgets.QFileDialog.Options()
            directorio,filename = var.dlgabrir.getSaveFileName(None, 'Guardar Copia',var.copia,'.zip',options = option)
            if var.dlgabrir.Accepted and filename !='':
                fichzip = zipfile.ZipFile(var.copia,'w')
                fichzip.write(var.filedb, os.path.basename(var.filedb),zipfile.ZIP_DEFLATED)
                fichzip.close()
                shutil.move(str(var.copia),str(directorio))
        except Exception as error:
            print('Error crear backup', error)


    def restaurarBackup(self):
       try:
           dirpro = os.getcwd()
           dirpro.join('\\')
           option = QtWidgets.QFileDialog.Options()
           filename = var.dlgabrir.getOpenFileName(None, 'Restaurar Copia','', '*.zip', options = option)
           if var.dlgabrir.Accepted and filename !='':
               file = filename[0]
               with zipfile.ZipFile(str(file), 'r') as bbdd:
                   bbdd.extractall()
                   bbdd.close()
           conexion.Conexion.cargarTabCli(self)

           #codigo drive

       except Exception as error:
            print('Error Restaurar backup', error)
