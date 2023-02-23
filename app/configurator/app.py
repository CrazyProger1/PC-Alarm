import sys
from .ui import *


class App:
    @staticmethod
    def run():
        app = QtWidgets.QApplication(sys.argv)
        window = Configurator()
        window.show()
        app.exec_()
