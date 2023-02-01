from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi
from Classes import FotoBase

class CargarImagenBase(QMainWindow):
    def __init__(self):
        super(CargarImagenBase, self).__init__()
        loadUi("UI\Cargar_imagen_base.ui", self)
        
        self.lblNombreImagenBase.setText("...")
        self.rutaImagenBase = ""
        self.btnExaminarBase.clicked.connect(self.buscarImagenBase)
        self.imagenBase = 0
    
    def buscarImagenBase(self):
        fileName = QFileDialog.getOpenFileName(self, 'Open file', "C:/Users/User/Desktop/PRUEBA/BASE", "Image files (*.jpg *.jpeg)")
        lblNombre = fileName[0].split("/")
        self.rutaImagenBase = fileName[0]
        sizelblNombre = len(lblNombre)
        self.lblNombreImagenBase.setText(lblNombre[sizelblNombre-1])
        self.lblImagenBase.setPixmap(QtGui.QPixmap(fileName[0]))
        self.lblImagenBase.setScaledContents(True)
        self.lblNombreImagenBase = QtWidgets.QLabel(self.centralwidget)
        self.lblNombreImagenBase.setGeometry(QtCore.QRect(390, 190, 300, 13))

        if fileName[0] != "":
            self.imagenBase = FotoBase.FotoBase(fileName[0])
            self.btnContinuar1.setEnabled(True)




        