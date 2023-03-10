import sys
from .ui import *
from app.utils.translator import Translator


class App:
    def __init__(self):
        Translator('configurator')

    @staticmethod
    def run():
        app = QtWidgets.QApplication(sys.argv)
        window = Configurator()
        window.show()
        app.exec_()
