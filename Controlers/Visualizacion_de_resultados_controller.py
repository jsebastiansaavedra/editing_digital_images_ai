from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

class VisualizacionDeResultados(QMainWindow):
    def __init__(self):
        super(VisualizacionDeResultados, self).__init__()
        loadUi("UI/Visualizacion_de_resultados.ui", self)