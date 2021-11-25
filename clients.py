'''

Funciones gestión clientes

'''
import locale

import conexion
import var
from window import *


class Clientes():
    dnivalido = False

    def validarDNI():
        try:
            dni = var.ui.txtDni.text()
            var.ui.txtDni.setText(dni.upper())
            tabla = 'TRWAGMYFPDXBNJZSQVHLCKE'  # letras dni
            dig_ext = 'XYZ'  # digito
            reemp_dig_ext = {'X': 0, 'Y': 1, 'Z': 2}
            numeros = '1234567890'
            dni = dni.upper()  # convertir la letra en mayusculas
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace[0], reemp_dig_ext[dni[0]]
                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:
                    var.ui.lblValidoDNI.setStyleSheet('QLabel {color: green;}')
                    var.ui.txtDni.setStyleSheet('QLineEdit {background-color: white ;}')
                    var.ui.lblValidoDNI.setText('V')
                    Clientes.dnivalido = True
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

    def cargarFecha(qDate):
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.txtFechAlta.setText(str(data))
            # Oculta la ventana
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
            if Clientes.dnivalido:  # es lo mismo que Clientes.dnivalido == True
                # preparamos el registro
                newCli = []
                cliente = [var.ui.txtDni, var.ui.txtFechAlta, var.ui.txtApel, var.ui.txtNome, var.ui.txtDir]
                tabCli = []  # para tablewidget
                client = [var.ui.txtDni, var.ui.txtApel, var.ui.txtNome, var.ui.txtFechAlta]
                # codigo para cargar la tabla
                for i in cliente:
                    newCli.append(i.text())

                for i in client:
                    tabCli.append(i.text())

                newCli.append(var.ui.cmbProv.currentText())

                newCli.append(var.ui.cmbMun.currentText())
                if var.ui.rbtHom.isChecked():
                    newCli.append('Hombre')
                elif var.ui.rbtFem.isChecked():
                    newCli.append('Mujer')


                pagos = []

                if var.ui.chkCargoCuenta.isChecked():
                    pagos.append('Cargo Cuenta')

                if var.ui.chkEfectivo.isChecked():
                    pagos.append('Efectivo')

                if var.ui.chkTarjeta.isChecked():
                    pagos.append('Tarjeta')

                if var.ui.chkTransfer.isChecked():
                    pagos.append('Transferencia')

                pagos = set(pagos)
                newCli.append('; '.join(pagos))
                print(newCli)
                tabCli.append('; '.join(pagos))

                envio = var.ui.spinEnvio.value()
                newCli.append(envio)
                print(newCli)
            # codigo para grabar en Base de Datos
            if Clientes.dnivalido:
                conexion.Conexion.altaCli(newCli)  # graba en la Base de datos
                conexion.Conexion.cargarTabCli(self)  # recarga la tabla

            else:
                print('DNI no valido')
                msg = QtWidgets.QMessageBox()
                msg.setText('DNI no valido')
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.exec()
        except Exception as error:
            print('Error en modulo guardar clientes', error)

    def limpiarFormCli(self):
        try:
            var.ui.txtDni.setStyleSheet('QLineEdit {background-color: white;}')
            var.ui.lblValidoDNI.setStyleSheet('QLabel {color: white;}')
            var.ui.lblValidoDNI.setText('')
            cajas = [var.ui.txtDni, var.ui.txtApel, var.ui.txtNome, var.ui.txtFechAlta, var.ui.txtDir]
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
            #+var.ui.spinEnvio.setValue(0)
        except Exception as error:
            print('Error en modulo limpiar formulario clientes, ', error)

    def cargaCli(self):
        try:
            # carga los datos del cliente al seleccionar en tabla
            Clientes.limpiarFormCli(self)
            fila = var.ui.tabClientes.selectedItems()  # seleccionamos la fila
            datos = [var.ui.txtDni, var.ui.txtApel, var.ui.txtNome, var.ui.txtFechAlta]

            if fila:
                row = [dato.text() for dato in fila]
            # print(row)
            for i, dato in enumerate(datos):
                dato.setText(row[i])  # cargamos en las cajas de texto los datos

            # ahora cargamos los metodos de pago que estan en la posicion 5 de row
            if 'Efectivo' in row[4]:
                var.ui.chkEfectivo.setChecked(True)

            if 'Transferencia' in row[4]:
                var.ui.chkTransfer.setChecked(True)

            if 'Tarjeta' in row[4]:
                var.ui.chkTarjeta.setChecked(True)

            if 'Cargo' in row[4]:
                var.ui.chkCargoCuenta.setChecked(True)
            registro = conexion.Conexion.oneCli(row[0])
            print(registro)# row0 es dni
            var.ui.txtDir.setText(str(registro[0]))
            var.ui.cmbProv.setCurrentText(str(registro[1]))
            var.ui.cmbMun.setCurrentText(str(registro[2]))
            if str(registro[3]) == 'Hombre':
                var.ui.rbtHom.setChecked(True)
            if str(registro[3]) == 'Mujer':
                var.ui.rbtFem.setChecked(True)
            var.ui.spinEnvio.setValue(registro[4])

        except Exception as error:
            print('Error en cargar datos de un cliente', error)

    def modifCli(self):
        try:
            modcliente = []

            cliente = [var.ui.txtDni, var.ui.txtFechAlta, var.ui.txtApel, var.ui.txtNome, var.ui.txtDir]
            # codigo para cargar la tabla
            for i in cliente:
                modcliente.append(i.text())
            modcliente.append(var.ui.cmbProv.currentText())
            modcliente.append(var.ui.cmbMun.currentText())
            if var.ui.rbtHom.isChecked():
                modcliente.append('Hombre')
            elif var.ui.rbtFem.isChecked():
                modcliente.append('Mujer')
            else:
                modcliente.append(' ')
            pagos = []
            if var.ui.chkCargoCuenta.isChecked():
                pagos.append('Cargo Cuenta')

            if var.ui.chkEfectivo.isChecked():
                pagos.append('Efectivo')

            if var.ui.chkTarjeta.isChecked():
                pagos.append('Tarjeta')

            if var.ui.chkTransfer.isChecked():
                pagos.append('Transferencia')

            pagos = set(pagos)
            modcliente.append('; '.join(pagos))
            conexion.Conexion.modificarCli(modcliente)
            conexion.Conexion.cargarTabCli(self)

        except Exception as e:
            print("error modificando cliente" + e)

    def bajaCli(self):
        try:
            dni = var.ui.txtDni.text()
            conexion.Conexion.bajaCli(dni)
            conexion.Conexion.cargarTabCli(self)
        except Exception as error:
            print('error en modulo baja cli de clientes')

    def cargaProv():
        try:
            var.ui.cmbProv.clear()
            prov = conexion.Conexion.cargarProv()
            # print(prov)
            #for i in prov:
             #   var.ui.cmbProv.addItem(i)
        except Exception as error:
            print('Error en módulo cargar provincias', error)

    def cargaMun(self):
        try:
            var.ui.cmbMun.clear()
            mun = conexion.Conexion.cargarMun(self)
        except Exception as error:
            print('Error en el módulo cargar municipio, ', error)

    def envio(self):
        try:
            op = var.ui.spinEnvio.value()
            if op == 0:
                var.ui.lblEnvio.setText("Recogida Cliente")
            if op == 1:
                var.ui.lblEnvio.setText("Envío Nacional Paquetería Express Urgente")
            if op == 2:
                var.ui.lblEnvio.setText("Envío Nacional Paquetería Normal")
            if op == 3:
                var.ui.lblEnvio.setText("Envío Interncional")
        except Exception as error:
            print('Error en el módulo envio en clients, ', error)