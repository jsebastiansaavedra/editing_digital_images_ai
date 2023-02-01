from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from Classes import Foto

class PantallaDeCarga(QMainWindow):
    def __init__(self):
        super(PantallaDeCarga, self).__init__()
        loadUi("UI/Pantalla_de_carga.ui", self)


        
