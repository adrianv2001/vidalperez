# This is a sample Python script.
import sys, var
import clients
import conexion
import events
from window import *
from windowaviso import *
from windowcal import *
from datetime import *


class DialogAviso(QtWidgets.QDialog):
    def __init__(self):
        super(DialogAviso, self).__init__()
        var.dlgaviso = Ui_Aviso()
        var.dlgaviso.setupUi(self)


class DialogCalendar(QtWidgets.QDialog):
    def __init__(self):
        super(DialogCalendar, self).__init__()
        var.dlgcalendar = Ui_windowcal()
        var.dlgcalendar.setupUi(self)
        diaactual = datetime.now().day
        mesactual = datetime.now().month
        anoactual = datetime.now().year
        var.dlgcalendar.calendar.setSelectedDate((QtCore.QDate(anoactual, mesactual, diaactual)))
        var.dlgcalendar.calendar.clicked.connect(clients.Clientes.cargarFecha)


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_MainWindow()
        var.ui.setupUi(self)
        '''
        Eventos de boton
        '''
        var.ui.btnSalir.clicked.connect(events.Eventos.Salir)

        var.ui.btnCalendar.clicked.connect(events.Eventos.abrircal)

        var.ui.btnGrabaCli.clicked.connect(clients.Clientes.guardaCli)

        var.ui.btnLimpiaCli.clicked.connect(clients.Clientes.limpiarFormCli)

        var.ui.btnBajaCli.clicked.connect(clients.Clientes.bajaCli)
        '''
        Eventos de la barra de menus
        '''
        var.ui.actionSalir.triggered.connect(events.Eventos.Salir)

        '''
        Eventos caja de texto
        '''
        var.ui.txtDni.editingFinished.connect(clients.Clientes.validarDNI)
        #var.ui.rbtGroupSex.buttonClicked.connect(clients.Clientes.selSexo)
        #var.ui.chkGroupPago.buttonClicked.connect(clients.Clientes.selPago)
        var.ui.txtApel.editingFinished.connect(clients.Clientes.letracapital)
        var.ui.txtNome.editingFinished.connect(clients.Clientes.letracapital)
        var.ui.txtDir.editingFinished.connect(clients.Clientes.letracapital)




        '''
        Eventos QTabWidget
        '''
        events.Eventos.resizeTablaCli(self)
        var.ui.tabClientes.clicked.connect(clients.Clientes.cargaCli)
        var.ui.tabClientes.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)

        '''
        Base de Datos
        '''
        conexion.Conexion.db_connect(var.filedb)
        conexion.Conexion.cargarTabCli(self)

        '''
        Eventos de ComboBox
        '''
        #clients.Clientes.cargaProv_(self)
        #provincia = var.ui.cmbProv.activated[str].connect(clients.Clientes.selProv)
        #clients.Clientes.cargaMun_(provincia)
        conexion.Conexion.cargarProv(self)
        conexion.Conexion.cargarMun(self)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    var.dlgaviso = DialogAviso()
    var.dlgcalendar = DialogCalendar()
    window.show()
    sys.exit(app.exec())
