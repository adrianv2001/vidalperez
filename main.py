# This is a sample Python script.
import sys,var

import clients
import events
from window import *
# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from windowaviso import *


class DialogAviso(QtWidgets.QDialog):
    def __init__(self):
        super(DialogAviso, self).__init__()
        var.dlgaviso = Ui_Aviso()
        var.dlgaviso.setupUi(self)


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_MainWindow()
        var.ui.setupUi(self)
        '''
        Eventos de boton
        '''
        var.ui.btnSalir.clicked.connect(events.Eventos.Salir)
        '''
        Eventos de la barra de menus
        '''
        var.ui.actionSalir.triggered.connect(events.Eventos.Salir)

        '''
        Eventos caja de texto
        '''
        var.ui.txtDni.editingFinished.connect(clients.Clientes.validarDNI)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    var.dlgaviso = DialogAviso()
    window.show()
    sys.exit(app.exec())



