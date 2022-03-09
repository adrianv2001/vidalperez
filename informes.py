import os, var
import traceback

import conexion
from PyQt5 import QtSql
from datetime import datetime
from reportlab.pdfgen import canvas


class Informes():
    def listadoProductos(self):
        """

        Método que genera un pdf con el listado de los productos

        """
        try:
            # se crea el lienzo
            var.cv = canvas.Canvas('informes/listadoproductos.pdf')
            var.cv.setTitle('Listado Productos')
            var.cv.setAuthor('Departamento de Administracion')
            Informes.cabecera(self)

            # Se guardan los cambios

            rootPath = '.\\informes'  # Aqui se van a guardar los PDF
            var.cv.setFont('Helvetica-Bold', size=9)
            textotitulo = 'LISTADO PRODUCTOS'
            Informes.pie(self, textotitulo)

            var.cv.drawString(255, 690, textotitulo)  # Dibuja el titulo
            var.cv.line(40, 685, 530, 685)  # Dibuja linea por debajo del titulo

            items = ['Código', 'Articulo', 'Precio']
            var.cv.drawString(70, 675, items[0])
            var.cv.drawString(200, 675, items[1])
            var.cv.drawString(350, 675, items[2])
            var.cv.line(40, 670, 530, 670)
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, nombre, precio from articulos order by codigo')

            var.cv.setFont('Helvetica', size=8)
            if query.exec_():
                i = 50
                j = 655
                while query.next():
                    if j <= 80:
                        var.cv.showPage()
                        # Informes.cabecera()
                        Informes.pie(textotitulo)
                        var.cv.setFont('Helvetica-Bold', size=9)
                        var.cv.drawString(255, 690, textotitulo)  # Dibuja el titulo
                        var.cv.line(40, 685, 530, 685)
                        var.cv.drawString(70, 675, items[0])
                        var.cv.drawString(200, 675, items[1])
                        var.cv.drawString(350, 675, items[2])
                        var.cv.line(40, 670, 530, 670)
                        i = 50
                        j = 655
                        var.cv.setFont('Helvetica', size=8)
                    var.cv.drawString(i, j, str(query.value(0)))
                    var.cv.drawString(i + 140, j, str(query.value(1)))
                    var.cv.drawString(i + 300, j, str(query.value(2)))
                    j = j - 20

            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('listadoproductos.pdf'):
                    os.startfile('%s/%s' % (rootPath, file))
                cont = cont + 1

            var.cv.save()
        except Exception as error:
            print('Error en listar clientes, en informes', error, traceback.format_exc())

    # Se va a crear un listado en pdf de todos los clientes
    def listadoClientes(self):
        """

        Método que genera un pdf con el listado de los clientes

        """
        try:

            # se crea el lienzo
            var.cv = canvas.Canvas('informes/listadoclientes.pdf')
            var.cv.setTitle('Listado Clientes')
            var.cv.setAuthor('Departamento de Administracion')
            Informes.cabecera(self)

            # Se guardan los cambios

            rootPath = '.\\informes'  # Aqui se van a guardar los PDF
            var.cv.setFont('Helvetica-Bold', size=9)
            textotitulo = 'LISTADO CLIENTES'
            # Informes.pie(self,textotitulo)

            var.cv.drawString(255, 690, textotitulo)  # Dibuja el titulo
            var.cv.line(40, 685, 530, 685)  # Dibuja linea por debajo del titulo

            items = ['DNI', 'Nombre', 'Formas de Pago']
            var.cv.drawString(70, 675, items[0])
            var.cv.drawString(200, 675, items[1])
            var.cv.drawString(350, 675, items[2])
            var.cv.line(40, 670, 530, 670)
            query = QtSql.QSqlQuery()
            query.prepare('select dni, apellidos, nombre, pago from clientes order by apellidos, nombre')

            var.cv.setFont('Helvetica', size=8)
            if query.exec_():
                i = 50
                j = 655
                while query.next():
                    if j <= 80:
                        # var.cv.drawString(440,30,'Página Siguiente...')
                        var.cv.showPage()
                        Informes.cabecera(self)
                        Informes.pie(self, textotitulo)
                        var.cv.setFont('Helvetica-Bold', size=9)
                        var.cv.drawString(255, 690, textotitulo)  # Dibuja el titulo
                        var.cv.line(40, 685, 530, 685)
                        var.cv.drawString(75, 675, items[0])
                        var.cv.drawString(200, 675, items[1])
                        var.cv.drawString(350, 675, items[2])
                        var.cv.line(40, 670, 530, 670)
                        i = 50
                        j = 655
                    var.cv.setFont('Helvetica', size=8)
                    var.cv.drawString(i, j, str(query.value(0)))
                    var.cv.drawString(i + 140, j, str(query.value(1) + ', ' + query.value(2)))
                    var.cv.drawString(i + 300, j, str(query.value(3)))
                    j = j - 20

            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('listadoclientes.pdf'):
                    os.startfile('%s/%s' % (rootPath, file))
                cont = cont + 1

            var.cv.save()
        except Exception as error:
            print('Error en listar clientes, en informes', error, traceback.format_exc())

    def cabecera(self):
        """

       Método que genera la cabecera de los informes

        """
        try:
            logo = '.\\img\logo.png'
            var.cv.drawImage(logo, 425, 722)
            var.cv.line(40, 800, 530, 800)
            var.cv.setFont('Helvetica-Bold', 14)
            var.cv.drawString(50, 785, 'Import-Export Vigo')

            var.cv.setFont('Helvetica', 11)
            var.cv.drawString(50, 770, 'CIF: A0000000H')
            var.cv.drawString(50, 755, 'Dirección: Av. Galicia, 101')
            var.cv.drawString(50, 740, 'Vigo - 36216 - Spain')
            var.cv.drawString(50, 725, 'import_export_vigo@email.com')

            var.cv.line(40, 710, 530, 710)
        except Exception as error:
            print('Error en cabecera informe clientes, en informes', error, traceback.format_exc())

    def pie(self, texto):
        """

        Método que genera el pie de los informes

        """
        try:

            var.cv.line(50, 50, 530, 50)
            fecha = datetime.today()
            fecha = fecha.strftime('%d.%m.%Y %H.%M.%S')
            var.cv.setFont('Helvetica', 6)
            var.cv.drawString(70, 40, str(fecha))
            var.cv.drawString(255, 40, str(texto))
            var.cv.drawString(500, 40, str('Página %s ' % var.cv.getPageNumber()))
        except Exception as error:
            print('error creacion de pie informe', error, traceback.format_exc())

    def factura(self):
        """

        Método que genera en pdf, una factura

        """
        try:
            var.cv = canvas.Canvas('informes/factura.pdf')
            var.cv.setTitle('Factura')
            var.cv.setAuthor('Departamento de Administración')
            rootPath = '.\\informes'
            var.cv.setFont('Helvetica-Bold', size=12)
            textotitulo = 'FACTURA'
            # Informes.cabecera(self)
            Informes.pie(self, textotitulo)
            Informes.cabeceraFactura()

            codfac = var.ui.lblnumFac.text()
            # var.cv.drawString(260, 694, textotitulo + ': ' + (str(codfac)))
            # var.cv.line(40, 685, 530, 685)
            # var.cv.setFont('Helvetica-Bold', size=9)
            # var.cv.drawString(270, 785, 'Datos Cliente: ')
            # query1 = QtSql.QSqlQuery()
            # query1.prepare('select direccion,municipio,provincia from clientes where dni = :dni')
            # query1.bindValue(':dni', str(var.ui.txtDNIFac.text()))
            # dir = []
            # if query1.exec_():
            #     while query1.next():
            #         dir.append(query1.value(0))
            #         dir.append(query1.value(1))
            #         dir.append(query1.value(2))
            #
            # var.cv.drawString(250, 760, 'CIF:' + var.ui.txtDni.text())
            # var.cv.drawString(250, 745, 'Cliente:' + var.ui.txtNome.text())
            # var.cv.drawString(250, 730, 'Direccion:' + str(dir[0]))
            # var.cv.drawString(250, 715, 'Localidad:' + str(dir[1]) + ' (' + str(dir[2]) + ')')
            items = ['Venta', 'Articulo', 'Precio', 'Cantidad', 'Total']
            var.cv.drawString(65, 673, items[0])
            var.cv.drawString(165, 673, items[1])
            var.cv.drawString(270, 673, items[2])
            var.cv.drawString(380, 673, items[3])
            var.cv.drawString(490, 673, items[4])
            suma = 0.0

            try:
                query2 = QtSql.QSqlQuery()
                query2.prepare('select codventa, precio, cantidad, codpro from ventas where codfac = :codfac')
                query2.bindValue(':codfac', codfac)
                i = 50
                j = 655

                if query2.exec_():
                    while query2.next():
                        codventa = query2.value(0)
                        precio = query2.value(1)
                        cantidad = query2.value(2)
                        nombre = conexion.Conexion.oneArt(int(query2.value(3)))
                        total = round(precio * cantidad, 2)
                        suma += total
                        var.cv.setFont('Helvetica', size=9)
                        var.cv.drawString(i + 20, j, str(query2.value(0)))
                        var.cv.drawString(i + 100, j, str(nombre[0]))
                        var.cv.drawString(i + 219, j, str(precio) + '€/kg')
                        var.cv.drawString(i + 340, j, str(cantidad))
                        var.cv.drawString(i + 442, j, str(total))
                        j = j - 20
            except Exception as error:
                print(error)
            var.cv.save()
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('factura.pdf'):
                    os.startfile('%s/%s' % (rootPath, file))
                cont = cont + 1

        except Exception as error:
            print('Error creación informe facturas', error, traceback.format_exc())

    def cabeceraFactura(self=None):
        """
        Método que dibuja la cabecera con los datos del cliente de específicos que se añaden en el caso de una factura.
        """
        try:

            logo = '.\\img\logo.png'
            var.cv.drawImage(logo, 425, 730)
            var.cv.line(40, 800, 530, 800)
            var.cv.setFont('Helvetica-Bold', 14)
            var.cv.drawString(50, 785, 'Import-Export Vigo')
            var.cv.setFont('Helvetica-Bold', 10)
            var.cv.drawString(220, 785, 'DATOS CLIENTE:')
            var.cv.setFont('Helvetica', 10)
            var.cv.drawString(50, 770, 'CIF: A0000000H')
            var.cv.drawString(50, 755, 'Dirección: Av. Galicia, 101')
            var.cv.drawString(50, 740, 'Vigo - 36216 - Spain')
            var.cv.drawString(50, 725, 'import_export_vigo@email.com')
            query = QtSql.QSqlQuery()
            dni = var.ui.txtDNIFac.text()
            query.prepare('select apellidos,nombre, direccion, envio from clientes where dni = :dni')
            query.bindValue(':dni', dni)
            if query.exec_():
                while query.next():
                    apellidos = query.value(0)
                    nombre = query.value(1)
                    direccion = query.value(2)
                    cliente = str(apellidos + ', ' + nombre)

            fecha = var.ui.txtFechaFac.text()
            fecha = str('Fecha: ' + fecha)
            dni = str('DNI: ' + dni)
            direccion = str('Dirección: ' + direccion)
            cliente = str('Cliente: ' + cliente)
            codfac = var.ui.lblnumFac.text()
            var.cv.drawString(220, 770, dni)
            var.cv.drawString(220, 755, cliente)
            var.cv.drawString(220, 740, direccion)
            var.cv.line(40, 718, 530, 718)

            var.cv.setFont('Helvetica', 8)
            var.cv.setFont('Helvetica-Bold', 10)
            var.cv.drawString(40, 700, 'Factura Nº: ' + str(codfac))
            var.cv.drawString(170, 700, fecha)
        except Exception as error:
            print('Error en cabecera informe ', error, traceback.format_exc())
