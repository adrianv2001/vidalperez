# This is a sample Python script.
import sys, var

import invoice
import informes
import articulos
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
        #var.ui.btnSalir.clicked.connect(events.Eventos.Salir)
        var.ui.btnCalendar.clicked.connect(events.Eventos.abrircal)
        var.ui.btnGrabaCli.clicked.connect(clients.Clientes.guardaCli)
        var.ui.btnLimpiaCli.clicked.connect(clients.Clientes.limpiarFormCli)
        var.ui.btnBajaCli.clicked.connect(clients.Clientes.bajaCli)
        var.ui.btnModifCli.clicked.connect(clients.Clientes.modifCli)


        #Examen
        var.ui.btnLimpiaArt.clicked.connect(articulos.Productos.limpiarFormPro)
        var.ui.btnGrabaArt.clicked.connect(articulos.Productos.altaPro)
        var.ui.btnBuscar.clicked.connect(conexion.Conexion.buscarArt)
        var.ui.btnModifArt.clicked.connect(articulos.Productos.modifProducto)
        var.ui.btnBajaArt.clicked.connect(articulos.Productos.bajaArt)

        var.ui.btnBuscaCliFac.clicked.connect(invoice.Facturas.buscaCli)
        var.ui.btnFechaFac.clicked.connect(events.Eventos.abrircal)
        var.ui.btnFacturar.clicked.connect(invoice.Facturas.altaFac)

        var.ui.btnPDFCli.clicked.connect(informes.Informes.listadoClientes) #boton report cli
        var.ui.btnReprPro.clicked.connect(informes.Informes.listadoProductos)

        var.ui.btnImprimirFactura.clicked.connect(informes.Informes.factura)
        '''
        Eventos de la barra de menus y de herramientas
        '''
        var.ui.actionSalir.triggered.connect(events.Eventos.Salir)
        var.ui.actionAbrir.triggered.connect(events.Eventos.Abrir)
        var.ui.actionCrear_Backup.triggered.connect(events.Eventos.crearBackup)
        var.ui.actionRestaurar_BBDD.triggered.connect(events.Eventos.restaurarBackup)
        var.ui.actionImportar_Datos.triggered.connect(events.Eventos.ImportarExcel)
        var.ui.actionExportar_Datos.triggered.connect(events.Eventos.ExportarDatos)
        var.ui.actionListado_Clientes.triggered.connect(informes.Informes.listadoClientes)

        '''
        Eventos caja de texto
        '''
        var.ui.txtDni.editingFinished.connect(clients.Clientes.validarDNI)

        var.ui.txtApel.editingFinished.connect(clients.Clientes.letracapital)
        var.ui.txtNome.editingFinished.connect(clients.Clientes.letracapital)
        var.ui.txtDir.editingFinished.connect(clients.Clientes.letracapital)
        var.txtCantidad = QtWidgets.QLineEdit()
        # var.txtCantidad.editingFinished.connect(invoice.Facturas.totalLineaVenta)

        '''
        Eventos QTabWidget
        '''
        events.Eventos.resizeTablaCli(self)
        events.Eventos.resizeTablaArt(self)
        events.Eventos.resizeTablaFac(self)
        events.Eventos.resizeTablaVen(self)
        var.ui.tabClientes.clicked.connect(clients.Clientes.cargaCli)
        var.ui.tabClientes.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        #Examen
        var.ui.tabArticulos.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tabArticulos.clicked.connect(articulos.Productos.cargaArt)

        var.ui.tabFacturas.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tabVentas.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tabFacturas.clicked.connect(conexion.Conexion.cargaFac)
        #invoice.Facturas.cargarLineaVenta(0)
        '''
        Base de Datos
        '''
        conexion.Conexion.db_connect(var.filedb)
        conexion.Conexion.cargarTabCli(self)
        #Examen
        conexion.Conexion.cargarTabPro(self)
        conexion.Conexion.cargarTabFacturas(self)

        '''
        Eventos de ComboBox
        '''

        conexion.Conexion.cargarProv(self)
        var.ui.cmbProv.currentIndexChanged.connect(clients.Clientes.cargaMun)
        conexion.Conexion.cargarCmbProducto(self)
        #var.cmbProducto.currentIndexChanged.connect(invoice.Facturas.procesoVenta)

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

        '''
        Eventos de spinBox
        '''
        var.ui.spinEnvio.valueChanged.connect(clients.Clientes.envio)



if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    var.dlgaviso = DialogAviso()
    var.dlgcalendar = DialogCalendar()
    var.dlgabrir = FileDialogAbrir()
    window.show()
    sys.exit(app.exec())
