import datetime

import xlwt as xlwt
from PyQt5 import QtSql, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from datetime import *

import clients
import var


class Conexion():
    def db_connect(filedb):
        try:
            db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(filedb)
            if not db.open():
                QtWidgets.QMessageBox.critical(None, 'No se puede abrir la base de datos.\n Haz click para continuar',
                                               QtWidgets.QMessageBox.Cancel)
                return False
            else:
                print('conexion establecida')
                return True
        except Exception as error:
            print('Problemas en conexion ', error)

    '''
    Modulos gestion Base Datos cliente
    '''

    def altaCli(newCli, nuevos=True):
        try:

            query = QtSql.QSqlQuery()
            query.prepare(
                'insert into clientes (dni,alta,apellidos,nombre,direccion,provincia,municipio,sexo,pago,envio)'
                'VALUES(:dni,:alta,:apellidos,:nombre,:direccion,:provincia,:municipio,:sexo,:pago,:envio)')
            query.bindValue(':dni', str(newCli[0]))
            query.bindValue(':alta', str(newCli[1]))
            query.bindValue(':apellidos', str(newCli[2]))
            query.bindValue(':nombre', str(newCli[3]))
            query.bindValue(':direccion', str(newCli[4]))
            query.bindValue(':provincia', str(newCli[5]))
            query.bindValue(':municipio', str(newCli[6]))
            query.bindValue(':sexo', str(newCli[7]))

            query.bindValue(':envio', str(newCli[9]))
            query.bindValue(':pago', str(newCli[8]))
            msg = QtWidgets.QMessageBox()
            if query.exec_():
                if nuevos:
                    msg.setText('Cliente insertado en la BBDD correctamente')
                    msg.setWindowTitle('Inserción Correcta')
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.exec()
            else:
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(query.lastError().text())
                msg.exec()

            print(newCli)
        except Exception as error:
            print('Problemas en Alta Cliente BBDD ', error)

    def cargarTabCli(self):
        try:
            hay = False
            index = 0
            query = QtSql.QSqlQuery()
            query.prepare('select dni, apellidos, nombre, alta, pago from clientes')
            if query.exec_():
                hay = True
                while query.next():
                    dni = query.value(0)
                    apellidos = query.value(1)
                    nombre = query.value(2)
                    alta = query.value(3)
                    pago = query.value(4)
                    var.ui.tabClientes.setRowCount(index + 1)
                    var.ui.tabClientes.setItem(index, 0, QTableWidgetItem(dni))
                    var.ui.tabClientes.setItem(index, 1, QTableWidgetItem(apellidos))
                    var.ui.tabClientes.setItem(index, 2, QTableWidgetItem(nombre))
                    var.ui.tabClientes.setItem(index, 3, QTableWidgetItem(alta))
                    var.ui.tabClientes.setItem(index, 4, QTableWidgetItem(pago))
                    index += 1

            if not hay:
                var.ui.tabClientes.removeRow(0)
                clients.Clientes.limpiarFormCli(self)
        except Exception as e:
            print("error cargarTabCli", e)

    def oneCli(dni):
        try:
            record = []
            query = QtSql.QSqlQuery()
            query.prepare('select direccion,provincia,municipio,sexo,envio'
                          ' from clientes where dni = :dni')
            query.bindValue(':dni', dni)
            if query.exec_():
                while query.next():
                    for i in range(5):
                        record.append(query.value(i))
            return record
        except Exception as error:
            print('Error en oneCli, ', error)

    def bajaCli(dni):
        try:
            print(dni)
            query = QtSql.QSqlQuery()
            query.prepare('delete from clientes where dni=:dni')
            query.bindValue(':dni', dni)
            msg = QtWidgets.QMessageBox()
            if query.exec_():

                msg.setText('Cliente con dni ' + dni + ' dado de baja correctamente')
                msg.setWindowTitle('Eliminacion Correcta')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.exec()
            else:
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(query.lastError().text())
                msg.exec()
        except Exception as error:
            print('error en baja cli', error)

    def cargarProv(self):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select * from provincias')

            if query.exec_():
                var.ui.cmbProv.addItem('')
                while query.next():
                    nombre = query.value(1)
                    var.ui.cmbProv.addItem(nombre)

        except Exception as error:
            print('Error en modulo cargar provincias, ', error)

    def cargarMun(self):
        try:
            # busco el código de la provincia
            var.ui.cmbMun.clear()
            prov = var.ui.cmbProv.currentText()
            query = QtSql.QSqlQuery()
            query.prepare('select id from provincias where provincia = :prov')
            query.bindValue(':prov', str(prov))
            if query.exec_():
                while query.next():
                    id = query.value(0)
            # cargo los municipios con ese código
            query1 = QtSql.QSqlQuery()
            query1.prepare('select municipio from municipios where provincia_id = :id')
            query1.bindValue(':id', id)
            if query1.exec_():
                var.ui.cmbMun.addItem('')
                while query1.next():
                    var.ui.cmbMun.addItem(query1.value(0))
        except Exception as error:
            print('Error en la selección de municipio', error)

    def modificarCli(modcliente):
        try:
            msg = QtWidgets.QMessageBox()
            print(modcliente)
            dni = modcliente[0]
            if dni == "":
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText("No hay ningún cliente")
                msg.exec()
                return
            query = QtSql.QSqlQuery()
            query.prepare('update clientes set alta=:alta,apellidos=:apellidos,nombre=:nombre, '
                          'direccion=:direccion,provincia=:provincia,municipio=:municipio, '
                          'sexo=:sexo,pago=:pago where dni = :dni')
            # print(modcliente)
            query.bindValue(':alta', str(modcliente[1]))
            query.bindValue(':apellidos', str(modcliente[2]))
            query.bindValue(':nombre', str(modcliente[3]))
            query.bindValue(':direccion', str(modcliente[4]))
            query.bindValue(':provincia', str(modcliente[5]))
            query.bindValue(':municipio', str(modcliente[6]))
            query.bindValue(':sexo', str(modcliente[7]))
            query.bindValue(':pago', str(modcliente[8]))
            query.bindValue(':dni', str(modcliente[0]))
            msg = QtWidgets.QMessageBox()
            if query.exec_():
                msg.setText('Cliente modificado con dni ' + modcliente[0])
                msg.setWindowTitle('Modificacion Correcta')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.exec()
            else:
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(query.lastError().text())
                msg.exec()
        except Exception as e:
            print(e)

    def exportExcel(self):
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y.%m.%d.%H.%M.%S')
            var.copia = (str(fecha) + '_dataExport.xls')
            option = QtWidgets.QFileDialog.Options()
            directorio, filename = var.dlgabrir.getSaveFileName(None, 'Exportar datos', var.copia, '.xls',
                                                                options=option)
            wb = xlwt.Workbook()
            sheet1 = wb.add_sheet('Hoja 1')

            # Cabeceras
            sheet1.write(0, 0, 'DNI')
            sheet1.write(0, 1, 'ALTA')
            sheet1.write(0, 2, 'APELLIDOS')
            sheet1.write(0, 3, 'NOMBRE')
            sheet1.write(0, 4, 'DIRECCION')
            sheet1.write(0, 5, 'PROVINCIA')
            sheet1.write(0, 6, 'MUNICIPIO')
            sheet1.write(0, 7, 'SEXO')
            sheet1.write(0, 8, 'PAGO')
            sheet1.write(0, 9, 'ENVIO')
            f = 1
            query = QtSql.QSqlQuery()
            query.prepare('SELECT *  FROM clientes')
            if query.exec_():
                while query.next():
                    for c in range(9):
                        sheet1.write(f, c, query.value(c))
                    f += 1
            wb.save(directorio)

        except Exception as error:
            print('Error en conexion para exportar excel ', error)

    # Examen

    def altaArt(newArt):
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'insert into articulos (nombre, precio)'
                'VALUES(:nombre,:precio)')
            query.bindValue(':nombre', str(newArt[0]))
            query.bindValue(':precio', str(newArt[1]))

            msg = QtWidgets.QMessageBox()
            if query.exec_():
                msg.setText('Articulo insertado en la BBDD correctamente')
                msg.setWindowTitle('Inserción Correcta')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.exec()
            else:
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(query.lastError().text())
                msg.exec()

        except Exception as error:
            print('Error en conexion, Alta Articulo ', error)

    def cargaTabArt(self):
        try:
            # El codigo de articulo no lo carga, no sé porque, con lo que las operaciones que dependan del id del
            # articulo no pueden funcionar correctamente
            index = 0
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, nombre, precio from articulos')
            if query.exec_():
                while query.next():
                    codigo = str(query.value(0))
                    nombre = query.value(1)
                    precio = query.value(2) + '€'

                    print(codigo,nombre,precio)
                    #str(codigo)
                    var.ui.tabArticulos.setRowCount(index + 1)
                    var.ui.tabArticulos.setItem(index, 0, QTableWidgetItem(str(codigo)))
                    var.ui.tabArticulos.setItem(index, 1, QTableWidgetItem(nombre))
                    var.ui.tabArticulos.setItem(index, 2, QTableWidgetItem(precio))
                    print(var.ui.tabArticulos.takeItem(index, 0).text())
                    index += 1
        except Exception as error:
            print('Error en conexion,cargar Tabla Articulos ', error)

    def oneArt(codigo):
        try:
            print(codigo)
            record = []
            query = QtSql.QSqlQuery()
            query.prepare('select nombre, precio'
                          ' from clientes where codigo = :codigo')
            query.bindValue(':codigo', codigo)
            if query.exec_():
                while query.next():
                    for i in range(2):
                        record.append(query.value(i))

        except Exception as error:
            print('Error en conexion, Cargar un articulo ', error)

    def buscarArt(self):
        try:
            nombre = var.ui.txtNombreArt.text()
            print(nombre)
            var.ui.tabArticulos.clear()
            index = 0
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, precio'
                          ' from articulos where nombre = :nombre')
            query.bindValue(':nombre', nombre)

            if query.exec_():
                while query.next():
                    codigo = query.value(0)
                    precio = query.value(1) + '€'
                    print(codigo,nombre,precio)
                    print(codigo, nombre, precio)
                    var.ui.tabArticulos.setRowCount(index + 1)
                    var.ui.tabArticulos.setItem(index, 0, QTableWidgetItem(type=int(codigo)))
                    var.ui.tabArticulos.setItem(index, 1, QTableWidgetItem(nombre))
                    var.ui.tabArticulos.setItem(index, 2, QTableWidgetItem(precio))
                    print(var.ui.tabArticulos.takeItem(index, 0).text())
                    index += 1
        except Exception as error:
            print('Error en buscar articulo,', error)

    def modificarArt(modart):
        try:
            msg = QtWidgets.QMessageBox()


            query = QtSql.QSqlQuery()
            query.prepare('update clientes set nombre=:nombre,precio=:precio where codigo = :codigo')
            # print(modcliente)
            query.bindValue(':codigo', str(modart[0]))
            query.bindValue(':alta', str(modart[1]))
            query.bindValue(':apellidos', str(modart[2]))

            msg = QtWidgets.QMessageBox()
            if query.exec_():
                msg.setText('articulo modificado' + modart[0])
                msg.setWindowTitle('Modificacion Correcta')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.exec()
            else:
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(query.lastError().text())
                msg.exec()
        except Exception as e:
            print(e)
