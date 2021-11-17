# This is a sample Python script.
import sys, var
import clients
import conexion
import events
from window import *
from windowaviso import *
from windowcal import *
from datetime import *
import locale
locale.setlocale(locale.LC_ALL,'es-ES')

class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        '''Ventana abrir explorador windows'''
        super(FileDialogAbrir,self).__init__()

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
        var.ui.btnModifCli.clicked.connect(clients.Clientes.modifCli)
        '''
        Eventos de la barra de menus y de herramientas
        '''
        var.ui.actionSalir.triggered.connect(events.Eventos.Salir)
        var.ui.actionAbrir.triggered.connect(events.Eventos.Abrir)
        var.ui.actionCrear_Backup.triggered.connect(events.Eventos.crearBackup)
        var.ui.actionRestaurar_BBDD.triggered.connect(events.Eventos.restaurarBackup)
        var.ui.actionImportar_Datos.triggered.connect(events.Eventos.importarDatos)

        '''
        Eventos caja de texto
        '''
        var.ui.txtDni.editingFinished.connect(clients.Clientes.validarDNI)

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

        conexion.Conexion.cargarProv(self)
        var.ui.cmbProv.currentIndexChanged.connect(clients.Clientes.cargaMun)


        '''
        Barra de estado
        '''
        var.ui.statusbar.addPermanentWidget(var.ui.lblFecha, 1)

        day = datetime.now()
        fe = day.strftime('%A, %d de %B de %Y')

        var.ui.lblFecha.setText(fe.capitalize())

        '''
        Eventos menu herramientas'''
        var.ui.actionactbarSalir.triggered.connect(events.Eventos.Salir)
        var.ui.actionbarAbrirCarpeta.triggered.connect(events.Eventos.Abrir)
        var.ui.actionCrear_Backup_2.triggered.connect(events.Eventos.crearBackup)
        var.ui.actionRestaurar_Backup.triggered.connect(events.Eventos.restaurarBackup)
        var.ui.actionbarImprimir.triggered.connect(events.Eventos.Imprimir)
        var.ui.actionImprimir.triggered.connect(events.Eventos.Imprimir)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    var.dlgaviso = DialogAviso()
    var.dlgcalendar = DialogCalendar()
    var.dlgabrir = FileDialogAbrir()
    window.show()
    sys.exit(app.exec())
