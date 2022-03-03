import datetime, xlwt, csv, sqlite3, var, os, shutil, clients, invoice
import traceback

from PyQt5 import QtSql, QtWidgets, Qt, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QDialog
from datetime import *
import locale

locale.setlocale(locale.LC_ALL, '')


class Conexion():
    def create_DB(filename):
        """

        Recibe el nombre de la BD
        Módulo que se ejecuta al inicio del programa
        Crea las tablas y carga municipios y provincias
        Crea los directorios necesarios
        :rtype: Object

        """
        try:
            con = sqlite3.connect(database=filename)
            cur = con.cursor()
            con.execute(
                'CREATE TABLE IF NOT EXISTS articulos(codigo INTEGER,nombre TEXT,precio NUMERIC, PRIMARY KEY(codigo AUTOINCREMENT))')
            con.commit()
            con.execute('CREATE TABLE IF NOT EXISTS clientes (dni TEXT NOT NULL, alta TEXT, apellidos TEXT NOT NULL,'
                        ' nombre TEXT, direccion TEXT, provincia TEXT, municipio TEXT, sexo TEXT, pago TEXT,'
                        ' envio INTEGER, PRIMARY KEY(dni))')
            con.commit()
            con.execute(
                'CREATE TABLE IF NOT EXISTS facturas (codfac INTEGER,dnifac TEXT,fechafac TEXT,PRIMARY KEY(codfac AUTOINCREMENT))')
            con.commit()
            con.execute('CREATE TABLE IF NOT EXISTS ventas (codventa INTEGER NOT NULL, codfac INTEGER NOT NULL,'
                        ' codpro INTEGER NOT NULL, precio REAL, cantidad REAL NOT NULL,'
                        ' PRIMARY KEY(codventa AUTOINCREMENT), FOREIGN KEY(codfac) REFERENCES facturas(codfac),'
                        ' FOREIGN KEY(codpro) REFERENCES articulos("codigo"))')
            con.commit()
            con.execute('CREATE TABLE IF NOT EXISTS provincias (id INTEGER, provincia	TEXT,PRIMARY KEY(id))')
            con.commit()

            con.execute('CREATE TABLE IF NOT EXISTS municipios (provincia_id INTEGER, municipio TEXT, id INTEGER)')
            con.commit()

            cur.execute('select count() from provincias')
            numero = cur.fetchone()[0]
            con.commit()
            if int(numero) == 0:
                with open('provincias.csv', 'r', encoding="utf-8") as fin:
                    dr = csv.DictReader(fin)
                    to_db = [(i['id'], i['provincia']) for i in dr]
                cur.executemany('insert into provincias (id,provincia) VALUES(?,?);', to_db)
                con.commit()
            con.close()

            '''Creacion de Directorios'''
            if not os.path.exists('.\\informes'):
                os.mkdir('.\\informes')

            if not os.path.exists('.\\img'):
                os.mkdir('.\\img')
                shutil.move('logo-empresa.jpg', '.\\img\logo-empresa.jpg')

            if not os.path.exists('C:\\copias'):
                os.mkdir('C:\\copias')

        except Exception as error:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Aviso')
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText(str(error))
            msg.exec_()

    def db_connect(filedb):
        """

        Módulo que realiza la conexion a la BD
        :return True si es correcto, False si hay error
        :rtype: Boolean

        """
        try:
            db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(filedb)
            if not db.open():
                QtWidgets.QMessageBox.critical(None, 'No se puede abrir la base de datos.\n Haz click para continuar',
                                               QtWidgets.QMessageBox.Cancel)
                return False
            else:
                return True
        except Exception as error:
            print('Problemas en conexion ',error, traceback.format_exc())

    def altaCli(newCli, nuevos=True):
        """

        Modulo que recibe datos de cliente y los inserta en la BD
        :param nuevos:
        :type nuevos:

        """
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
            query.bindValue(':pago', str(newCli[8]))
            query.bindValue(':envio', str(newCli[9]))

            msg = QtWidgets.QMessageBox()
            if query.exec_():
                if nuevos:
                    msg.setText('Cliente insertado en la BBDD correctamente')
                    msg.setWindowTitle('Inserción Correcta')
                    msg.setIcon(QtWidgets.QMessageBox.Ok)
                    msg.exec()
            else:
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(query.lastError().text())
                msg.exec()

        except Exception as error:
            print('Problemas en Alta Cliente BBDD ',error, traceback.format_exc())

    def cargarTabCli(self):
        """

        Módulo que toma datos de los cliente y los carga en la tabla Clientes de la Interfaz Gráfica

        """
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
        """

        Módulo que selecciona un cliente según su dni y lo devuelve a la funcion CargaCli del fichero clientes
        :return: Devuelve una lista
        :rtype: Object = Lista

        """
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
            print('Error en oneCli, ',error, traceback.format_exc())

    def bajaCli(dni):
        """

        Módulo que recibe dni cliente y lo elimina de la BD

        """
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
            print('error en baja cli',error, traceback.format_exc())

    def cargarProv(self):
        """

        Módulo que carga las provincias en su combo de la interfaz gráfica del panel clientes

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select * from provincias')

            if query.exec_():
                var.ui.cmbProv.addItem('')
                while query.next():
                    nombre = query.value(1)
                    var.ui.cmbProv.addItem(nombre)

        except Exception as error:
            print('Error en modulo cargar provincias, ',error, traceback.format_exc())

    def cargarMun(self):
        """

        Módulo que selecciona los municipios dada una provincia y los carga en su combo de la interfaz gráfica del panel clientes

        """
        try:
            # busco el código de la provincia
            id = 0
            prov = var.ui.cmbProv.currentText()
            query = QtSql.QSqlQuery()
            query.prepare('select id from provincias where provincia = :prov')
            query.bindValue(':prov', str(prov))
            if query.exec_():
                while query.next():
                    id = query.value(0)
                    print(id)
            # cargo los municipios con ese código

            query1 = QtSql.QSqlQuery()
            query1.prepare('select municipio from municipios where provincia_id = :id')
            query1.bindValue(':id', id)
            print(id)

            if query1.exec_():
                var.ui.cmbMun.addItem('')
                while query1.next():
                    var.ui.cmbMun.addItem(query1.value(0))


        except Exception as error:
            print('Error en la selección de municipio',error, traceback.format_exc())

    def modificarCli(modcliente):
        """

        Módulo que recibe los datos del cliente a modificar y los modifica en la BD

        """
        try:
            msg = QtWidgets.QMessageBox()
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
        """

        Módulo que carga los datos en una hoja excel

        """
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
            print('Error en conexion para exportar excel ',error, traceback.format_exc())

    # Examen

    def altaArt(newArt):
        """

        Modulo que recibe los datos del producto y los carga en la BD

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'insert into articulos (nombre, precio)'
                'values(:nombre,:precio)')
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
            print('Error en conexion, Alta Articulo ',error, traceback.format_exc())

    def cargarTabPro():
        """

        Modulo que carga la tabla de productos siempre que se dé de alta, baja o modificacion de un producto

        """
        try:
            index = 0
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, nombre, precio from articulos order by codigo')

            if query.exec_():
                while query.next():
                    codigo = query.value(0)
                    producto = query.value(1)
                    precio = query.value(2)
                    precio = str(precio).replace(',', '.')
                    precio = precio +' €'
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
            print('Problemas mostrar tabla productos',error, traceback.format_exc())

    def oneArt(codigo):
        """

        Selecciona un producto a tracves de su codigo
        :return: el producto
        :rtype: Object

        """
        try:
            record = []
            query = QtSql.QSqlQuery()
            query.prepare('select nombre, precio'
                          ' from articulos where codigo = :codigo')
            query.bindValue(':codigo', codigo)
            if query.exec_():
                while query.next():
                    for i in range(2):
                        record.append(query.value(i))
            return record

        except Exception as error:
            print('Error en conexion, Cargar un articulo ',error, traceback.format_exc())

    def buscarArt(self):
        """

        Módulo que dado el nombre del producto lo busca en la BD y lo devuelve al modulo de productos

        """
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
                    precio = query.value(1)+ '€'
                    print(codigo, nombre, precio)
                    print(codigo, nombre, precio)
                    var.ui.tabArticulos.setRowCount(index + 1)
                    var.ui.tabArticulos.setItem(index, 0, QTableWidgetItem(type=int(codigo)))
                    var.ui.tabArticulos.setItem(index, 1, QTableWidgetItem(nombre))
                    var.ui.tabArticulos.setItem(index, 2, QTableWidgetItem(precio))
                    print(var.ui.tabArticulos.takeItem(index, 0).text())
                    index += 1
        except Exception as error:
            print('Error en buscar articulo,',error, traceback.format_exc())

    def modifPro(modpro):
        """

        Módulo que recibe el registro de datos de un producto y los modifica en la BD

        """
        try:
            print(modpro)
            query = QtSql.QSqlQuery()
            query.prepare('update articulos set nombre =:producto, precio = :precio where codigo = :cod')
            query.bindValue(':cod', int(modpro[0]))
            query.bindValue(':producto', str(modpro[1]))
            modpro[2] = modpro[2].replace('€', '')
            modpro[2] = modpro[2].replace(',', '.')
            modpro[2] = float(modpro[2])
            modpro[2] = round(modpro[2], 2)
            modpro[2] = str(modpro[2])
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
            print('Error modificar producto en conexion: ',error, traceback.format_exc())

    def bajaPro(codigo):
        """

        Módulo que recibe el codigo de un producto y lo elimina de la BD

        """
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
            print('error en baja art, en conexion',error, traceback.format_exc())

    def buscaCliFac(dni):
        """

        Módulo que busca los datos del cliente a facturar a partir de su dni
        :return: Datos del cliente a facturar
        :rtype: Object = registro

        """
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
            print('Error en buscar cliente en conexion',error, traceback.format_exc())

    def altaFac(registro):
        """

        Dado el cliente a facturar, se da de alta una factura en la BD con el dni

        """
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
            print('Error en altaFac en conexion',error, traceback.format_exc())

    def cargarTabFacturas(self):
        """

        Modulo que se ejecuta cada vez que se da de alta, modifica o elimina una factura

        """
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
            print('Error en cargar Tab Facturas',error, traceback.format_exc())

    def buscaDNIFac(numfac):
        """

        Modulo que busca el dni de la tabla facturas en la BD
        :return: devuelve un dni
        :rtype: string

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select dnifac from facturas where codfac = :numfac')
            query.bindValue(':numfac', int(numfac))
            if query.exec_():
                while query.next():
                    dni = query.value(0)
            return dni
        except Exception as error:
            print('Fallo en buscaDNIFac en conexion')

    def bajaFac(self):
        """

        Módulo que dado el numero de factura la dá de baja, ademas llama al modulo borrar ventas, para que se eliminen las venta asociadas a esa factura

        """
        try:
            numfac = var.ui.lblnumFac.text()
            con = str('Desea eliminar la factura ' + numfac + '?')
            query = QtSql.QSqlQuery()
            query.prepare('delete from facturas where codfac = :numfac')
            query.bindValue(':numfac', numfac)
            msg = QtWidgets.QMessageBox()
            if query.exec_():
                msg.setText('Factura eliminada correctamente')
                msg.setWindowTitle('Eliminacion Correcta')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.exec()
                Conexion.delVentaFac(numfac)
                Conexion.cargarTabFacturas(self)
            else:
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(query.lastError().text())
                msg.exec()
        except Exception as error:
            print('Fallo en bajaFac en conexion', error, traceback.format_exc())

    def cargarCmbProducto(self):
        """

        Toma los nombres de los productos existentes de la BD y los carga en el panel de facturacion de la tabla ventas

        """
        try:
            var.cmbProducto.clear()
            query = QtSql.QSqlQuery()
            var.cmbProducto.addItem('')
            query.prepare('select nombre from articulos order by nombre')
            if query.exec_():
                while query.next():
                    var.cmbProducto.addItem(str(query.value(0)))
        except Exception as error:
            print('Fallo en cargarCmbProducto en conexion', error, traceback.format_exc())

    def obtenerCodPrecio(articulo):
        """

        Dado el nomre del produto, obtenemos su codigo y su precio para realizar los calculos necesarios en la venta
        :return: Devuelve el codigo y precio
        :rtype: Obejct= array

        """
        try:
            dato = []
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, precio from articulos where nombre = :nombre')
            query.bindValue(':nombre', articulo)
            if query.exec_():
                while query.next():
                    dato.append(int(query.value(0)))
                    dato.append(str(query.value(1)))
                    var.codpro = dato[0]
            return dato

        except Exception as error:
            print('Fallo en obtenerCodPrecio en conexion', error, traceback.format_exc())

    def cargarVenta(venta):
        """

        Carga el registro de una venta realizada en la tabla ventas

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('insert into ventas(codfac,codpro,precio,cantidad)values(:codfac,:codpro,:precio,:cantidad)')
            query.bindValue(':codfac', int(venta[0]))
            query.bindValue(':codpro', int(venta[1]))
            query.bindValue(':precio', venta[2])
            query.bindValue(':cantidad', venta[3])

            if query.exec_():
                var.ui.lblVenta.setText('Venta realizada')
                var.ui.lblVenta.setStyleSheet('QLabel {color:black;}')
            else:
                var.ui.lblVenta.setText('Error en Venta')
                var.ui.lblVenta.setStyleSheet('QLabel {color:red;}')
        except Exception as error:
            print('Fallo en cargarVenta en conexion', error, traceback.format_exc())

    def buscaCodFac(self):
        """

        Selecciona la ultima factura o el codigo mas alto de factuara
        :return:  num factura
        :rtype: entero

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select codigo from facturas order by codigo desc limit 1')
            dato = ''
            if query.exec_():
                while query.next():
                    dato = query.value(0)
            return dato
        except Exception as error:
            print('Fallo en buscaCodFac en conexion', error, traceback.format_exc())


    def cargaFac(self=None):
        """

        Módulo que al elegir una factura de la tabla facturas carga sus datos en el panel de facturacion.

        """
        try:
            fila = var.ui.tabFacturas.selectedItems()  # seleccionamos la fila
            datos = [var.ui.lblnumFac, var.ui.txtFechaFac]
            if fila:  # cargamos en row todos los datos de la fila
                row = [dato.text() for dato in fila]
            for i, dato in enumerate(datos):
                dato.setText(row[i])
            dni = Conexion.buscaDNIFac(row[0])
            var.ui.txtDNIFac.setText(dni)
            registro = Conexion.buscaCliFac(dni)
            if registro:
                nombre = registro[0] + ', ' + registro[1]
                var.ui.lblCliente.setText(nombre)
            invoice.Facturas.cargarLineaVenta(self)

            Conexion.cargarLineasVenta()

        except Exception as error:
            print('error cargaFac en conexion',error, traceback.format_exc())

    def cargarLineasVenta():
        """

        Modulo que carga todas las ventas asociadas a una factura en la tabla ventas
        ademas realiza los calculas para el subtotal, total e iva de la factuars
        se le llama cada ez que se realiza una venta

        """
        try:
            suma = 0.0
            sumaT = 0.0
            index = 1
            codfac = str(var.ui.lblnumFac.text())
            query = QtSql.QSqlQuery()
            query.prepare('select codventa,codpro,precio,cantidad from ventas where codfac = :codfac')
            query.bindValue(':codfac', codfac)
            if query.exec_():
                while query.next():
                    codventa = query.value(0)
                    codpro = query.value(1)
                    precio = query.value(2)
                    cantidad = query.value(3)
                    producto = Conexion.nombrePro(codpro)
                    suma = float(precio) * float(cantidad)
                    sumaT = sumaT + suma
                    suma = round(suma, 2)
                    var.ui.tabVentas.setRowCount(index + 1)
                    var.ui.tabVentas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codventa)))
                    var.ui.tabVentas.item(index, 0).setTextAlignment(QtCore.Qt.AlignCenter)
                    var.ui.tabVentas.setItem(index, 1, QtWidgets.QTableWidgetItem(producto))
                    var.ui.tabVentas.setItem(index, 2, QtWidgets.QTableWidgetItem(str(precio) + ' €'))
                    var.ui.tabVentas.setItem(index, 3, QtWidgets.QTableWidgetItem(str(cantidad)))
                    var.ui.tabVentas.setItem(index, 4, QtWidgets.QTableWidgetItem(str(suma) + ' €'))
                    index = index + 1
            var.ui.lblSub.setText((str(round(sumaT, 2)) + ' €'))
            iva = float(sumaT * 0.21)
            total = iva + sumaT
            var.ui.lblIVA.setText((str(round(iva, 2)) + ' €'))
            var.ui.lblTotal.setText((str(round(total, 2)) + ' €'))

        except Exception as error:
            print('error cargar las lines de factura',error, traceback.format_exc())

    def nombrePro(cod):
        """

        Busca un articulo a traves de su codigo
        :return: el nombre del producto
        :rtype: string

        """
        nombre = ''
        query = QtSql.QSqlQuery()
        query.prepare('select nombre from articulos where codigo=:codigo')
        query.bindValue(':codigo', cod)
        if query.exec_():
            while query.next():
                nombre = query.value(0)
        return nombre

    def borraVenta(self):
        """

        Elimina una venta de una factura

        """
        try:
            sel = var.ui.tabVentas.selectedItems()
            row = var.ui.tabVentas.currentRow()
            if sel:
                codventa = var.ui.tabVentas.item(row, 0).text()
            print(codventa)
            query = QtSql.QSqlQuery()
            query.prepare('delete from ventas where codventa = :codventa')
            query.bindValue(':codventa', int(codventa))
            if query.exec_():
                while (query.next()):
                    msg1 = QtWidgets.QMessageBox()
                    msg1.setWindowTitle('Aviso')
                    msg1.setIcon(QtWidgets.QMessageBox.Information)
                    msg1.text('Venta eliminada')
                    msg1.exec()
                    codfac = var.ui.lblnumFac.text()
            Conexion.cargarLineasVenta()
        except Exception as error:
            print('error en baja venta en conexion ',error, traceback.format_exc())

    def delVentaFac(numfac):

        """

        Modulo que se llama cuando se da de baja una factura en la BD, para que elimine todas las ventas asociadas a esa factura
        Recibe el numero de factura a borrar, selecciona todos los codigos de venta asociados a esa factura y los guarda en una lista
        A continuacion a medida que recorre  esa lista, da de baja las ventas. Finalmente recarga la tabla de ventas y limpia datos
        
        :param numfac valor de la factura
        :type numfac: int

        """
        try:
            ventas = []
            query = QtSql.QSqlQuery()
            query.prepare('select codventa from ventas where codfac=:numfac')
            query.bindValue(':numfac', numfac)
            if query.exec_():
                while query.next():
                    ventas.append(query.value(0))
            for dato in ventas:
                query1 = QtSql.QSqlQuery()
                query1.prepare('delete from ventas where codventa = :dato')
                query1.bindValue(':dato', int(dato))
                query1.exec_()

                var.ui.tabVentas.clearContents()
                var.ui.lblIVA.setText('')
                var.ui.lblSub.setText('')
                var.ui.lblTotal.setText('')
        except Exception as error:
            print('Error eliminando venta',error, traceback.format_exc())
