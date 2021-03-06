import traceback

import conexion, var
from window import *

class Clientes():
    dnivalido = False

    def validarDNI():
        """
        Método que valida el DNI del cliente
        :rtype: object
        """
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
            print('Error en módulo validarDNI',error, traceback.format_exc())

    def cargarFecha(qDate):
        """

        Método que carga la fecha en el panel de clientes

        """
        try:
            data = (str(qDate.day()).zfill(2)+'/'+str(qDate.month()).zfill(2)+'/'+str(qDate.year()))

            if var.ui.tabPrograma.currentIndex()==0:
               var.ui.txtFechAlta.setText(data)
            elif var.ui.tabPrograma.currentIndex()==1:
               var.ui.txtFechaFac.setText(data)
            # Oculta la ventana
            var.dlgcalendar.hide()

        except Exception as error:
            print('Error cargar fecha en txtFecha',error, traceback.format_exc())

    def letracapital():
        """

        Método que se llama para poner letra capital en el nombre y apellidos del cliente

        """
        try:
            apel = var.ui.txtApel.text()
            var.ui.txtApel.setText(apel.title())
            nome = var.ui.txtNome.text();
            var.ui.txtNome.setText(nome.title())
            dir = var.ui.txtDir.text()
            var.ui.txtDir.setText(dir.title())
        except Exception as error:
            print('Error en modulo mayusculas',error, traceback.format_exc())

    def guardaCli(self):
        """

        Método que recupera los datos del cliente del panel de clientes y lo prepara para la insercion en la bd

        """
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
            print('Error en modulo guardar clientes',error, traceback.format_exc())


    def limpiarFormCli(self):
        """

        Método que limpia el formulario del panel clientes

        """
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
            print('Error en modulo limpiar formulario clientes, ',error, traceback.format_exc())

    def cargaCli(self):
        """

        Método que se llama cuando se selecciona un cliente en el panel clientes, carga sus datos en el formulario

        """
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
            var.ui.txtDNIFac.setText(str(row[0]))
            var.ui.lblCliente.setText(row[1]+', '+row[2])
            var.ui.txtDir.setText(str(registro[0]))
            var.ui.cmbProv.setCurrentText(str(registro[1]))
            var.ui.cmbMun.setCurrentText(str(registro[2]))
            if str(registro[3]) == 'Hombre':
                var.ui.rbtHom.setChecked(True)
            if str(registro[3]) == 'Mujer':
                var.ui.rbtFem.setChecked(True)
            if registro[4]:
                var.ui.spinEnvio.setValue(registro[4])

        except Exception as error:
            print('Error en cargar datos de un cliente',error, traceback.format_exc())

    def modifCli(self):
        """

        Método que obtiene datos del formulario de clientes, y los guarda en un "cliente" auxiliar, para la modificacion. Este cliente se lo pasa al método  modificar cliente de conexion

        """
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
        """

        Método que recoje el dni de un cliente y se lo pasa al métod correspondiente de conexion para darlo de baja

        """
        try:
            dni = var.ui.txtDni.text()
            conexion.Conexion.bajaCli(dni)
            conexion.Conexion.cargarTabCli(self)
        except Exception as error:
            print('error en modulo baja cli de clientes',error, traceback.format_exc())

    def cargaProv():
        """

        Método que limpia el combobox de provincias y carga las provincias en el combobox del panel clientes

        """
        try:
            var.ui.cmbProv.clear()
            prov = conexion.Conexion.cargarProv()
            # print(prov)
            #for i in prov:
             #   var.ui.cmbProv.addItem(i)
        except Exception as error:
            print('Error en módulo cargar provincias',error, traceback.format_exc())

    def cargaMun(self):
        """

         Método que limpia el combobox de municipios y carga los municipios en el combobox del panel clientes

        """
        try:
            var.ui.cmbMun.clear()
            mun = conexion.Conexion.cargarMun(self)
        except Exception as error:
            print('Error en el módulo cargar municipio, ',error, traceback.format_exc())

    def envio(self):
        """

        Método que dependiendo del valor del spin de envio, le indica al usuario el método de envio escogido

        """
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
            print('Error en el módulo envio en clients, ',error, traceback.format_exc())