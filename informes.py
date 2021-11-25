import os,var
from reportlab.pdfgen import canvas


class Informes():
    # Se va a crear un listado en pdf de todos los clientes
    def listadoClientes(self):
        try:
            # se crea el lienzo
            var.cv = canvas.Canvas('informes/listadoclientes.pdf')
            Informes.cabecera()

             # Se guardan los cambios

            rootPath = '.\\informes'  # Aqui se van a guardar los PDF
            var.cv.setFont('Helvetica',8)
            var.cv.setTitle('Listado Clientes')
            var.cv.setAuthor('Departamento de Administracion')
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
            var.cv.line(40,800,500,800)
            var.cv.setFont('Helvetica-Bold',14)
            var.cv.drawString(50,785,'Import-Export Vigo')

            var.cv.setFont('Helvetica',11)
            var.cv.drawString(50,770,'CIF:A0000000H')

            var.cv.drawString(50, 755, 'Direccion: Avenida Galicia,101')
            var.cv.drawString(50, 740, 'Vigo - 36216 - Spain')
            var.cv.drawString(50, 725, 'micorreo@email.com')

            var.cv.drawImage(logo,425,750)
            var.cv.line(40, 710, 500, 710)
        except Exception as error:
            print('Error en cabecera informe clientes, en informes', error)
