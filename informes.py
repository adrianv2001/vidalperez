import os, var
import conexion
from PyQt5 import QtSql
from datetime import datetime
from reportlab.pdfgen import canvas


class Informes():
    def listadoProductos(self):
        try:
            # se crea el lienzo
            var.cv = canvas.Canvas('informes/listadoproductos.pdf')
            var.cv.setTitle('Listado Productos')
            var.cv.setAuthor('Departamento de Administracion')
            Informes.cabecera()

            # Se guardan los cambios

            rootPath = '.\\informes'  # Aqui se van a guardar los PDF
            var.cv.setFont('Helvetica-Bold', size=9)
            textotitulo = 'LISTADO PRODUCTOS'
            Informes.pie(textotitulo)

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
                        #var.cv.drawString(440,30,'Página Siguiente...')
                        var.cv.showPage()
                        Informes.cabecera()
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
                if file.endswith('.pdf'):
                    os.startfile('%s/%s' % (rootPath, file))
                cont = cont + 1

            var.cv.save()
        except Exception as error:
            print('Error en listar clientes, en informes', error)
    # Se va a crear un listado en pdf de todos los clientes
    def listadoClientes(self):
        try:

            # se crea el lienzo
            var.cv = canvas.Canvas('informes/listadoclientes.pdf')
            var.cv.setTitle('Listado Clientes')
            var.cv.setAuthor('Departamento de Administracion')
            Informes.cabecera()

            # Se guardan los cambios

            rootPath = '.\\informes'  # Aqui se van a guardar los PDF
            var.cv.setFont('Helvetica-Bold', size=9)
            textotitulo = 'LISTADO CLIENTES'
            Informes.pie(textotitulo)

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
                        #var.cv.drawString(440,30,'Página Siguiente...')
                        var.cv.showPage()
                        Informes.cabecera()
                        Informes.pie(textotitulo)
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
                if file.endswith('.pdf'):
                    os.startfile('%s/%s' % (rootPath, file))
                cont = cont + 1

            var.cv.save()
        except Exception as error:
            print('Error en listar clientes, en informes', error)

    def cabecera():
        try:
            logo = '.\\img\\logo.png'
            var.cv.line(40, 800, 530, 800)
            var.cv.setFont('Helvetica-Bold', 14)
            var.cv.drawString(50, 785, 'Import-Export Vigo')

            var.cv.setFont('Helvetica', 11)
            var.cv.drawString(50, 770, 'CIF:A0000000H')

            var.cv.drawString(50, 755, 'Direccion: Avenida Galicia,101')
            var.cv.drawString(50, 740, 'Vigo - 36216 - Spain')
            var.cv.drawString(50, 725, 'micorreo@email.com')

            var.cv.drawImage(logo, 425, 750)
            var.cv.line(40, 710, 530, 710)
        except Exception as error:
            print('Error en cabecera informe clientes, en informes', error)

    def pie(texto):
        try:

            var.cv.line(50, 50, 530, 50)
            fecha = datetime.today()
            fecha = fecha.strftime('%d.%m%.Y %H.%M.%S')
            var.cv.setFont('Helvetica', size=6)

            var.cv.drawString(70, 40, str(fecha))
            var.cv.drawString(255, 40, str(texto))
            var.cv.drawString(500, 40, str('Pagina %s' % var.cv.getPageNumber()))
        except Exception as error:
            print('error creacion de pie informe', error)
