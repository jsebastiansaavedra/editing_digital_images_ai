from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from Controlers import Cargar_imagen_base_controller, Cargar_imagenes_a_tratar_controller, Pantalla_de_carga_controller, Visualizacion_de_resultados_controller
import sys
from PyQt5.uic import loadUi
from Classes import Foto
import random


def window():
    # creating application
    app = QApplication(sys.argv)
    # creating widget for navigation throug windows
    widget = QtWidgets.QStackedWidget()
    # creating windows
    CargarImagenBaseWindow = Cargar_imagen_base_controller.CargarImagenBase()
    CargarImagenATratarWindow = Cargar_imagenes_a_tratar_controller.CargarImagenesATratar()
    PantallaDeCargaWindow = Pantalla_de_carga_controller.PantallaDeCarga()
    VisualizacionDeResultadosWindow = Visualizacion_de_resultados_controller.VisualizacionDeResultados()

    # adding windows to StackedWidget
    widget.addWidget(CargarImagenBaseWindow)
    widget.addWidget(CargarImagenATratarWindow)
    #widget.addWidget(PantallaDeCargaWindow)
    widget.addWidget(VisualizacionDeResultadosWindow)

    # setting size of the widget screen
    widget.setFixedHeight(720)
    widget.setFixedWidth(1080)

    # show window
    widget.show()

    def ejecutarAlgoritmo(self):

        widget.setCurrentIndex(widget.currentIndex()+1)
        imagenesFinales = []
        for i in range (len(CargarImagenATratarWindow.imagenesATratar)):
            PantallaDeCargaWindow.lblCargando.setText((str(i+1))+"/"+(str(len(CargarImagenATratarWindow.imagenesATratar))))
            imagenTratada = Foto.Foto(CargarImagenATratarWindow.imagenesATratar[i])
            print("----------------------------------------------------------------------")
            print(imagenTratada.rutaImagenInicial)
            rutaFinal = imagenTratada.EjecutarAlgoritmo(CargarImagenBaseWindow.imagenBase.abstraccionHSL)
            imagenesFinales.append(rutaFinal)

        # set imagen base results
        VisualizacionDeResultadosWindow.lblImagenBaseFinal.setPixmap(QtGui.QPixmap(CargarImagenBaseWindow.rutaImagenBase))
        VisualizacionDeResultadosWindow.lblImagenBaseFinal.setScaledContents(True)
        
        # set imagenes a tratar results
        fila = 0
        columna = 0
        for i in range (len(imagenesFinales)):
            fotoResultante = QtWidgets.QLabel()
            fotoResultante.setGeometry(QtCore.QRect(0, 0, 100, 100))
            fotoResultante.setPixmap(QtGui.QPixmap(imagenesFinales[i]))
            fotoResultante.setScaledContents(True)
            VisualizacionDeResultadosWindow.gridFinal.addWidget(fotoResultante, fila, columna)
            if columna == 2:
                columna = 0
                fila = fila+1
            else:
                columna = columna+1

        # delete last images
        CargarImagenATratarWindow.imagenesATratar = []

        
    # Methods for change window
    def nextScreen(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

    def mainScreen(self):
        widget.setCurrentIndex(widget.currentIndex()-2)
    
    # Connecting buttons
    CargarImagenBaseWindow.btnContinuar1.clicked.connect(nextScreen)
    CargarImagenATratarWindow.btnContinuar2.clicked.connect(ejecutarAlgoritmo)
    VisualizacionDeResultadosWindow.btnInicio4.clicked.connect(mainScreen)


    # click at X button and close
    sys.exit(app.exec_())
  
# calling method
window()

