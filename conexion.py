from PyQt5 import QtSql, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

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

    def altaCli(newCli):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('insert into clientes (dni,alta,apellidos,nombre,direccion,provincia,municipio,sexo,pago)'
                          'VALUES(:dni,:alta,:apellidos,:nombre,:direccion,:provincia,:municipio,:sexo,:pago)')
            query.bindValue(':dni', str(newCli[0]))
            query.bindValue(':alta', str(newCli[1]))
            query.bindValue(':apellidos', str(newCli[2]))
            query.bindValue(':nombre', str(newCli[3]))
            query.bindValue(':direccion', str(newCli[4]))
            query.bindValue(':provincia', str(newCli[5]))
            query.bindValue(':municipio', str(newCli[6]))
            query.bindValue(':sexo', str(newCli[7]))
            query.bindValue(':pago', str(newCli[8]))
            msg = QtWidgets.QMessageBox()
            if query.exec_():
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
            index = 0
            query = QtSql.QSqlQuery()
            query.prepare('select dni, apellidos, nombre,alta, pago from clientes')
            if query.exec_():
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
        except Exception as e:
            print("error cargarTabCli", e)

    def oneCli(dni):
        try:
            record = []
            query = QtSql.QSqlQuery()
            query.prepare('select direccion,provincia,municipio,sexo'
                          ' from clientes where dni = :dni')
            query.bindValue(':dni', dni)
            if query.exec_():
                while query.next():
                    for i in range(4):
                        record.append(query.value(i))
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

                msg.setText('Cliente con dni ', dni, ' dado de baja correctamente')
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
                    while query.next():

                        nombre = query.value(1)
                        var.ui.cmbProv.addItem(nombre)

                    # print(id,nombre)


            except Exception as error:
                print('Error en modulo cargar provincias, ', error)

    def cargarMun(self):
        try:
            prov = var.ui.cmbProv.currentText()

            query = QtSql.QSqlQuery()
            query.prepare('select id from provincias where provincia=:prov')
            query.bindValue(':prov', prov)
            if query.exec_():
                while query.next():
                    id = query.value(0)

            query1 = QtSql.QSqlQuery()
            query1.prepare('select municipio from municipios where provincia_id=:id')
            query1.bindValue(':id', id)
            if query1.exec_():
                while query1.next():

                    nombre = query1.value(1)
                    var.ui.cmbMun.addItem(nombre)

                # print(id,nombre)



        except Exception as error:
            print('Error en modulo cargar provincias, ', error)
