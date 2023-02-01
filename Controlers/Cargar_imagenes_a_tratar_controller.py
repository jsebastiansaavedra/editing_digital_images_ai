from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi

class CargarImagenesATratar(QMainWindow):
    def __init__(self):
        super(CargarImagenesATratar, self).__init__()
        loadUi("UI/Cargar_imagenes_a_tratar.ui", self)

        self.imagenesATratar = []
        self.btnExaminarATratar.clicked.connect(self.buscarImagenesATratar)
    
    def buscarImagenesATratar(self):

        filesname = QFileDialog.getOpenFileNames(self, 'Open files', "C:/Users/User/Desktop/PRUEBA/TRATAR", "Image files (*.jpg *.jpeg)")

        if filesname[1] != "":
            self.btnContinuar2.setEnabled(True)

        
        fila = 0
        columna = 0
        for i in range(len(filesname[0])):
            self.imagenesATratar.append(filesname[0][i])
            imagen = QtWidgets.QLabel(self.centralwidget)
            imagen.setGeometry(QtCore.QRect(0, 0, 100, 100))
            imagen.setPixmap(QtGui.QPixmap(filesname[0][i]))
            imagen.setScaledContents(True)
            self.gridFotosTratar.addWidget(imagen, fila, columna)
            if columna == 2:
                columna = 0
                fila = fila+1
            else:
                columna = columna+1
        


