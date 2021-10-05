'''
Fichero de eventos generales
'''
import sys

import var


class Eventos():
    def Salir(self):
        try:
           sys.exit()
        except Exception as error:
            print('Error en módulo salir ',error)