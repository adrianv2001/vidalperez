'''

Funciones gestión clientes

'''
import var
from window import *
class Clientes():
    def validarDNI():
        try:
            dni = var.ui.txtDni.text()
            var.ui.txtDni.setText(dni.upper())
            tabla = 'TRWAGMYFPDXBNJZSQVHLCKE' #letras dni
            dig_ext = 'XYZ' #digito
            reemp_dig_ext = {'X':0,'Y':1,'Z':2}
            numeros = '1234567890'
            dni = dni.upper() #convertir la letra en mayusculas
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                   dni = dni.replace[0], reemp_dig_ext[dni[0]]
                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:
                    var.ui.lblValidoDNI.setStyleSheet('QLabel {color: green;}')
                    var.ui.lblValidoDNI.setText('V')

                else:
                    var.ui.lblValidoDNI.setStyleSheet('QLabel {color: red;}')
                    var.ui.lblValidoDNI.setText('X')
                    var.ui.txtDni.setStyleSheet('QLineEdit {background-color: red;}')
            else:
                var.ui.lblValidoDNI.setStyleSheet('QLabel {color: red;}')
                var.ui.txtDni.setStyleSheet('QLineEdit {background-color: red;}')
                var.ui.lblValidoDNI.setText('X')



        except Exception as error:
            print('Error en módulo validarDNI', error)

    def selSexo(self):
        try:
            if var.ui.rbtFem.isChecked():
                print('marcado femenino')
            if var.ui.rbtHom.isChecked():
                print('marcado masculino')
        except Exception as error:
            print('Error en modulo seleccionar sexo, ',error)

    def selPago(self):
        try:
            if var.ui.chkEfectivo.isChecked():
                print('Has seleccionado efectivo')

            if var.ui.chkTarjeta.isChecked():
                print('Has seleccionado Tarjeta')

            if var.ui.chkCargoCuenta.isChecked():
                print('Has seleccionado Cargo en Cuenta')

            if var.ui.chkTransfer.isChecked():
                print('Has seleccionado Transferencia Bancaria')
        except Exception as error:
            print('Error en modulo seleccionar Pago, ', error)

    def cargaProv_(self):
        try:
            var.ui.cmbProv.clear()
            prov = ['','A Coruña','Lugo','Pontevedra','Ourense']
            for i in prov:
                var.ui.cmbProv.addItem(i)
        except Exception as error:
            print('Error en módulo cargar provincias',error)
    def selProv(prov):
        try:

            print('Has seleccionado la provincia de ', prov)
            return prov
        except Exception as error:
            print('Error en seleccion de provincia', error)

    def cargaMun_(self):
        try:
            var.ui.cmbMun.clear()
            mun = ['','Salvaterra de Miño','As Neves','Ponteareas','Salceda de Caselas']
            for i in mun:
                var.ui.cmbMun.addItem(i)
        except Exception as error:
            print('Error en módulo cargar municipios',error)
    def selMun(mun):
        try:

            print('Has seleccionado el municipio de ', mun)
            return mun
        except Exception as error:
            print('Error en seleccion de municipio', error)

    def cargarFecha(qDate):
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(),qDate.month(),qDate.year()))
            var.ui.txtFechAlta.setText(str(data))
            #Oculta la ventana
            var.dlgcalendar.hide()

        except Exception as error:
            print('Error cargar fecha en txtFecha', error)

    def letracapital():
        try:
            apel = var.ui.txtApel.text()
            var.ui.txtApel.setText(apel.title())
            nome = var.ui.txtNome.text();
            var.ui.txtNome.setText(nome.title())
            dir = var.ui.txtDir.text()
            var.ui.txtDir.setText(dir.title())
        except Exception as error:
            print('Error en modulo mayusculas', error)

    def guardaCli(self):
        try:
            #preparamos el registro
            newCli =[]
            client =[var.ui.txtApel, var.ui.txtNome, var.ui.txtFechAlta]
            for i in client:
                newCli.append(i.text())
            #cargamos en la tabla
            row = 0
            column = 0
            var.ui.tabClientes.insertRow(row)
            for campo in newCli:
                cell = QtWidgets.QTableWidgetItem(campo)
                var.ui.tabClientes.setItem(row,column,cell)
                column+=1
        except Exception as error:
            print('Error en modulo guardar clientes', error)

    def limpiarFormCli(self):
        try:
            var.ui.txtDni.setStyleSheet('QLineEdit {background-color: white;}')
            var.ui.lblValidoDNI.setStyleSheet('QLabel {color: white;}')
            var.ui.lblValidoDNI.setText('')
            cajas = [var.ui.txtDni,var.ui.txtApel,var.ui.txtNome,var.ui.txtFechAlta,var.ui.txtDir]
            for i in cajas:
               i.setText('')
            var.ui.rbtGroupSex.setExclusive(False)
            var.ui.rbtFem.setChecked(False)
            var.ui.rbtHom.setChecked(False)
            var.ui.rbtGroupSex.setExclusive(True)

            var.ui.chkTarjeta.setChecked(False)
            var.ui.chkEfectivo.setChecked(False)
            var.ui.chkTransfer.setChecked(False)
            var.ui.chkCargoCuenta.setChecked(False)

            var.ui.cmbProv.setCurrentIndex(0)
            var.ui.cmbMun.setCurrentIndex(0)
        except Exception as error:
            print('Error en modulo limpiar formulario clientes, ', error)