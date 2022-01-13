import datetime

import xlwt as xlwt
from PyQt5 import QtSql, QtWidgets, Qt, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from datetime import *
import locale

locale.setlocale(locale.LC_ALL, '')
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

    def cargarTabPro(self):
        try:
            index = 0
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, nombre, precio from articulos order by codigo')
            if query.exec_():
                while query.next():
                    codigo = query.value(0)
                    producto = query.value(1)
                    precio = query.value(2)
                    var.ui.tabArticulos.setRowCount(index + 1)  # creamos la fila y luego cargamos datos
                    var.ui.tabArticulos.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codigo)))
                    var.ui.tabArticulos.setItem(index, 1, QtWidgets.QTableWidgetItem(producto))
                    var.ui.tabArticulos.setItem(index, 2, QtWidgets.QTableWidgetItem(precio))
                    var.ui.tabArticulos.item(index, 2).setTextAlignment(QtCore.Qt.AlignCenter)
                    var.ui.tabArticulos.item(index, 0).setTextAlignment(QtCore.Qt.AlignCenter)
                    index += 1
            header = var.ui.tabArticulos.horizontalHeader()
            for i in range(3):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
                if i == 0 or i == 2:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

        except Exception as error:
            print('Problemas mostrar tabla productos', error)

    def oneArt(codigo):
        try:
            print(codigo)
            record = []
            query = QtSql.QSqlQuery()
            query.prepare('select nombre, precio'
                          ' from articulos where codigo = :codigo')
            query.bindValue(':codigo', codigo)
            if query.exec_():
                while query.next():
                    for i in range(2):
                        record.append(query.value(i))
            print(record)
            return record

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
                    print(codigo, nombre, precio)
                    print(codigo, nombre, precio)
                    var.ui.tabArticulos.setRowCount(index + 1)
                    var.ui.tabArticulos.setItem(index, 0, QTableWidgetItem(type=int(codigo)))
                    var.ui.tabArticulos.setItem(index, 1, QTableWidgetItem(nombre))
                    var.ui.tabArticulos.setItem(index, 2, QTableWidgetItem(precio))
                    print(var.ui.tabArticulos.takeItem(index, 0).text())
                    index += 1
        except Exception as error:
            print('Error en buscar articulo,', error)

    def modifPro(modpro):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('update articulos set nombre =:producto, precio = :precio where codigo = :cod')
            query.bindValue(':cod', int(modpro[0]))
            query.bindValue(':producto', str(modpro[1]))
            modpro[2] = modpro[2].replace('€', '')
            modpro[2] = modpro[2].replace(',', '.')
            modpro[2] = float(modpro[2])
            modpro[2] = round(modpro[2], 2)
            modpro[2] = str(modpro[2])
            modpro[2] = locale.currency(float(modpro[2]))
            query.bindValue(':precio', str(modpro[2]))

            if query.exec_():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Datos modificados de Producto')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(query.lastError().text())
                msg.exec()
        except Exception as error:
            print('Error modificar producto en conexion: ', error)

    def bajaPro(codigo):
        try:
            print(codigo)
            query = QtSql.QSqlQuery()
            query.prepare('delete from articulos where codigo=:codigo')
            query.bindValue(':codigo', codigo)
            msg = QtWidgets.QMessageBox()
            if query.exec_():

                msg.setText('Articulo con codigo ' + codigo + ' dado de baja correctamente')
                msg.setWindowTitle('Eliminacion Correcta')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.exec()
            else:
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(query.lastError().text())
                msg.exec()
        except Exception as error:
            print('error en baja art, en conexion', error)

    '''
    Gestion Facturacion
    '''

    def buscaCliFac(dni):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare('select apellidos,nombre from clientes where dni=:dni')
            query.bindValue(':dni', dni)
            if query.exec_():
                while query.next():
                    registro.append(query.value(0))
                    registro.append(query.value(1))

            return registro
        except Exception as error:
            print('Error en buscar cliente en conexion', error)

    def altaFac(registro):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('insert into facturas (fechafac,dnifac)values(:fechafac,:dni)')
            query.bindValue(':fechafac', str(registro[1]))
            query.bindValue(':dni', str(registro[0]))
            msg = QtWidgets.QMessageBox()
            if query.exec_():

                msg.setText('Factura dada de alta')
                msg.setWindowTitle('Insercion Correcta')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.exec()
            else:
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(query.lastError().text())
                msg.exec()
        except Exception as error:
            print('Error en altaFac en conexion', error)

    def cargarTabFacturas(self):

        try:
            index = 0
            query = QtSql.QSqlQuery()
            query.prepare('select codfac, fechafac from facturas order by fechafac DESC')
            if query.exec_():
                while query.next():
                    codigo = query.value(0)
                    fechafac = query.value(1)
                    var.btnfacdel = QtWidgets.QPushButton()
                    icopapelera = QtGui.QPixmap("img/papelera.png")
                    var.btnfacdel.setFixedSize(28, 28)
                    var.btnfacdel.setIcon(QtGui.QIcon(icopapelera))
                    var.ui.tabFacturas.setRowCount(index + 1)  # creamos la fila y luego cargamos datos
                    var.ui.tabFacturas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codigo)))
                    var.ui.tabFacturas.setItem(index, 1, QtWidgets.QTableWidgetItem(fechafac))
                    cell_widget = QtWidgets.QWidget()
                    lay_out = QtWidgets.QHBoxLayout(cell_widget)
                    lay_out.setContentsMargins(0, 0, 0, 0)
                    lay_out.addWidget(var.btnfacdel)

                    var.btnfacdel.clicked.connect(Conexion.bajaFac)
                    var.ui.tabFacturas.setCellWidget(index, 2, cell_widget)
                    var.ui.tabFacturas.item(index, 0).setTextAlignment(QtCore.Qt.AlignCenter)
                    var.ui.tabFacturas.item(index, 1).setTextAlignment(QtCore.Qt.AlignCenter)
                    index = index + 1

        except Exception as error:
            print('Error en cargar Tab Facturas', error)

    def buscaDNIFac(numfac):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select dnifac from facturas where codfac = :numfac')
            query.bindValue(':numfac', int(numfac))
            if query.exec_():
                while query.next():
                    dni = query.value(0)
                    print(dni)
            return dni
        except Exception as error:
            print('Fallo en buscaDNIFac en conexion')

    def bajaFac(self):
        try:
            confirma = QtWidgets.QMessageBox.accept

            numfac = var.ui.lblnumFac.text()
            con = str('Desea eliminar la factura '+ numfac+ '?')
            #confirma.setText(con)
            #confirma.setWindowTitle('Eliminar')
            confirma.setStandardButtons(QMessageBox.Ok,QMessageBox.Cancel)
            if confirma.exec():
                query = QtSql.QSqlQuery()
                query.prepare('delete from facturas where codfac = :numfac')
                query.bindValue(':numfac', numfac)
                msg = QtWidgets.QMessageBox()
                if query.exec_():

                    msg.setText('Factura eliminada correctamente')
                    msg.setWindowTitle('Eliminacion Correcta')
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.exec()
                    Conexion.cargarTabFacturas(self)
                else:
                    msg.setWindowTitle('Aviso')
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.setText(query.lastError().text())
                    msg.exec()
        except Exception as error:
            print('Fallo en bajaFac en conexion', error)
