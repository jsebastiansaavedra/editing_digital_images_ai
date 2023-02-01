from PIL import Image, ImageEnhance
from Classes import Parametro
import random
import numpy as np
import os
import errno

class Foto():
    def __init__(self, pathImagen):
        super(Foto, self).__init__

        self.imagen = Image.open(pathImagen)
        self.imagenRGB = self.ObtenerColoresRGB(self.imagen)
        self.imagenHSL = self.RGBtoHSL(self.imagenRGB)
        self.abstraccion = self.AbstraerImagen()
        self.abstraccionRGB = self.ObtenerColoresRGB(self.abstraccion)
        self.abstraccionHSL = self.RGBtoHSL(self.abstraccionRGB)
        self.parametros = []
        self.parametros.append(Parametro.Parametro(0.0,0.0,0.0,0.0,0.0,0.0))
        self.mejorParametro = ""
        self.rutaImagenInicial = pathImagen
        self.rutaImagenFinal = self.CrearRutaFinal()
        self.calificacionMayorActual = Parametro.Parametro(0.0,0.0,0.0,0.0,0.0,0.0)
        self.calificacionMayorActual.calificacion = 0.8

    def AbstraerImagen(self):
        return self.imagen.resize((10,10))

    def ObtenerColoresRGB(self, item):
        return np.asarray(item)

    def RGBtoHSL(self, item):
        hsl = []

        alto = len(item)
        ancho = len(item[0])

        for i in range(alto):
            aux = []
            for j in range(ancho):
                mayor = max(item[i][j], key=int)/255
                menor = min(item[i][j], key=int)/255

                l = (mayor+menor)/2

                if l < 0.5:
                    if (mayor+menor) != 0:
                        s = (mayor-menor)/(mayor+menor)
                    else:
                        s = 0
                else:
                    if (2-mayor-menor) != 0:
                        s = (mayor-menor)/(2-mayor-menor)
                    else:
                        s = 0

                aux.append((round(s*100), round(l*100)))
            hsl.append(aux)
        
        hsl = np.array(hsl)

        return hsl

    def GenerarParametrosAleatorios(self, cantidad):
        for i in range (cantidad):
            self.parametros.append(Parametro.Parametro(random.randrange(-20,20)*0.05, random.randrange(-20,20)*0.05, random.randrange(-20,20)*0.05, random.randrange(-20,20)*0.05, random.randrange(-20,20)*0.05, random.randrange(-20,20)*0.05))

    def SeleccionarMejoresParametros(self):
        parametrosABorrar = []
        for i in range (len(self.parametros)):
            if self.parametros[i].calificacion < self.calificacionMayorActual.calificacion:
                parametrosABorrar.append(self.parametros[i])
        
        for j in range (len(parametrosABorrar)):
            self.parametros.remove(parametrosABorrar[j])

    def EvolucionarParametros(self):
        parametrosEvolucionados = []
        for i in range (len(self.parametros)):
            if self.parametros[i].exposicion > -1.0 and self.parametros[i].exposicion < 1.0:
                parametrosEvolucionados.append(Parametro.Parametro(self.parametros[i].exposicion+0.05, self.parametros[i].contraste, self.parametros[i].iluminaciones, self.parametros[i].sombras, self.parametros[i].blancos, self.parametros[i].negros))
                parametrosEvolucionados.append(Parametro.Parametro(self.parametros[i].exposicion-0.05, self.parametros[i].contraste, self.parametros[i].iluminaciones, self.parametros[i].sombras, self.parametros[i].blancos, self.parametros[i].negros))

            if self.parametros[i].contraste > -1.0 and self.parametros[i].contraste < 1.0:
                parametrosEvolucionados.append(Parametro.Parametro(self.parametros[i].exposicion, self.parametros[i].contraste+0.05, self.parametros[i].iluminaciones, self.parametros[i].sombras, self.parametros[i].blancos, self.parametros[i].negros))
                parametrosEvolucionados.append(Parametro.Parametro(self.parametros[i].exposicion, self.parametros[i].contraste-0.05, self.parametros[i].iluminaciones, self.parametros[i].sombras, self.parametros[i].blancos, self.parametros[i].negros))

            if self.parametros[i].iluminaciones > -1.0 and self.parametros[i].iluminaciones < 1.0:
                parametrosEvolucionados.append(Parametro.Parametro(self.parametros[i].exposicion, self.parametros[i].contraste, self.parametros[i].iluminaciones+0.05, self.parametros[i].sombras, self.parametros[i].blancos, self.parametros[i].negros))
                parametrosEvolucionados.append(Parametro.Parametro(self.parametros[i].exposicion, self.parametros[i].contraste, self.parametros[i].iluminaciones-0.05, self.parametros[i].sombras, self.parametros[i].blancos, self.parametros[i].negros))

            if self.parametros[i].sombras > -1.0 and self.parametros[i].sombras < 1.0:
                parametrosEvolucionados.append(Parametro.Parametro(self.parametros[i].exposicion, self.parametros[i].contraste, self.parametros[i].iluminaciones, self.parametros[i].sombras+0.05, self.parametros[i].blancos, self.parametros[i].negros))
                parametrosEvolucionados.append(Parametro.Parametro(self.parametros[i].exposicion, self.parametros[i].contraste, self.parametros[i].iluminaciones, self.parametros[i].sombras-0.05, self.parametros[i].blancos, self.parametros[i].negros))

            if self.parametros[i].blancos > -1.0 and self.parametros[i].blancos < 1.0:
                parametrosEvolucionados.append(Parametro.Parametro(self.parametros[i].exposicion, self.parametros[i].contraste, self.parametros[i].iluminaciones, self.parametros[i].sombras, self.parametros[i].blancos+0.05, self.parametros[i].negros))
                parametrosEvolucionados.append(Parametro.Parametro(self.parametros[i].exposicion, self.parametros[i].contraste, self.parametros[i].iluminaciones, self.parametros[i].sombras, self.parametros[i].blancos-0.05, self.parametros[i].negros))

            if self.parametros[i].negros > -1.0 and self.parametros[i].negros < 1.0:
                parametrosEvolucionados.append(Parametro.Parametro(self.parametros[i].exposicion, self.parametros[i].contraste, self.parametros[i].iluminaciones, self.parametros[i].sombras, self.parametros[i].blancos, self.parametros[i].negros+0.05))
                parametrosEvolucionados.append(Parametro.Parametro(self.parametros[i].exposicion, self.parametros[i].contraste, self.parametros[i].iluminaciones, self.parametros[i].sombras, self.parametros[i].blancos, self.parametros[i].negros-0.05))
        self.parametros = parametrosEvolucionados
        print("Hay "+str(len(self.parametros))+" parámetros")

    def CrearRutaFinal(self):
        arrayRuta = self.rutaImagenInicial.split("/")
        self.rutaImagenFinal = ""
        for i in range (len(arrayRuta)-1):
            self.rutaImagenFinal = self.rutaImagenFinal + arrayRuta[i] + "/"
        try:
            os.mkdir(self.rutaImagenFinal+"Resultado")
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        self.rutaImagenFinal = self.rutaImagenFinal+"Resultado/"+arrayRuta[len(arrayRuta)-1]
        return self.rutaImagenFinal

    def RetornarImagen(self, resultado):
        imagenResultante = Image.fromarray(np.uint8(resultado))
        imagenResultante.save(self.rutaImagenFinal)

    def Exposicion(self, valorExposicion, imagenAEditar):
        exposicion = Image.fromarray(np.uint8(imagenAEditar))
        exposicion = ImageEnhance.Brightness(exposicion)
        multiplicador = 0.6*valorExposicion
        nuevaImagen = np.asarray(exposicion.enhance(1+multiplicador))
        return nuevaImagen

    def Contraste(self, valorContraste, imagenAEditar):
        contraste = Image.fromarray(np.uint8(imagenAEditar))
        contraste = ImageEnhance.Contrast(contraste)
        multiplicador = 0.6*valorContraste
        nuevaImagen = np.asarray(contraste.enhance(1+multiplicador))
        return nuevaImagen

    def Negros(self, valorNegros, imagenAEditar, imagenAEditarHSL):
        nuevaImagen = []

        alto = len(imagenAEditarHSL)
        ancho = len(imagenAEditarHSL[0])


        for i in range (alto):
            aux = []
            for j in range(ancho):
                valorDeAumento = 0
                valorDeDisminucion = 0

                if imagenAEditarHSL[i][j][1] <= 25 :
                    valorDeAumento = 25
                    valorDeDisminucion = 60
                elif imagenAEditarHSL[i][j][1] <= 60 and imagenAEditarHSL[i][j][1] > 25:
                    valorDeDisminucion = 40

            
                diferenciaFinal = 0

                if valorNegros>0:
                    diferenciaFinal = round(valorNegros*valorDeAumento)
                if valorNegros<0:
                    diferenciaFinal = round(valorNegros*valorDeDisminucion)

                #print(diferenciaFinal)

                r = imagenAEditar[i][j][0]+diferenciaFinal
                g = imagenAEditar[i][j][1]+diferenciaFinal
                b = imagenAEditar[i][j][2]+diferenciaFinal

                if r>255:
                    r=255
                if g>255:
                    g=255
                if b>255:
                    b=255
                
                if r<0:
                    r=0
                if g<0:
                    g=0
                if b<0:
                    b=0

                aux.append((r,g,b))

            nuevaImagen.append(aux)
        
        nuevaImagen = np.asarray(nuevaImagen)

        edicionAdicional = Image.fromarray(np.uint8(nuevaImagen))
        edicionAdicional = ImageEnhance.Color(edicionAdicional)
        multiplicador = 0
        if valorNegros<0:
            multiplicador = -0.15*valorNegros
            nuevaImagen = np.asarray(edicionAdicional.enhance(1+multiplicador))

        return nuevaImagen

    def Blancos(self, valorBlancos, imagenAEditar, imagenAEditarHSL):
        nuevaImagen = []

        alto = len(imagenAEditarHSL)
        ancho = len(imagenAEditarHSL[0])


        for i in range (alto):
            aux = []
            for j in range(ancho):
                valorDeAumento = 0
                valorDeDisminucion = 0

                if imagenAEditarHSL[i][j][1] >= 75 :
                    valorDeAumento = 60
                    valorDeDisminucion = 25
                elif imagenAEditarHSL[i][j][1] >= 40 and imagenAEditarHSL[i][j][1] < 75:
                    valorDeAumento = 40

            
                diferenciaFinal = 0

                if valorBlancos>0:
                    diferenciaFinal = round(valorBlancos*valorDeAumento)
                if valorBlancos<0:
                    diferenciaFinal = round(valorBlancos*valorDeDisminucion)

                #print(diferenciaFinal)

                r = imagenAEditar[i][j][0]+diferenciaFinal
                g = imagenAEditar[i][j][1]+diferenciaFinal
                b = imagenAEditar[i][j][2]+diferenciaFinal

                if r>255:
                    r=255
                if g>255:
                    g=255
                if b>255:
                    b=255
                
                if r<0:
                    r=0
                if g<0:
                    g=0
                if b<0:
                    b=0

                aux.append((r,g,b))

            nuevaImagen.append(aux)
        
        nuevaImagen = np.asarray(nuevaImagen)

        edicionAdicional = Image.fromarray(np.uint8(nuevaImagen))
        edicionAdicional = ImageEnhance.Color(edicionAdicional)
        multiplicador = 0
        if valorBlancos>0:
            multiplicador = 0.2*valorBlancos
            nuevaImagen = np.asarray(edicionAdicional.enhance(1+multiplicador))

        return nuevaImagen
    
    def Iluminaciones(self, valorIluminaciones, imagenAEditar, imagenAEditarHSL):
        nuevaImagen = []

        alto = len(imagenAEditarHSL)
        ancho = len(imagenAEditarHSL[0])


        for i in range (alto):
            aux = []
            for j in range(ancho):
                valorDeAumento = 0
                valorDeDisminucion = 0

                if imagenAEditarHSL[i][j][1] > 65 :
                    valorDeAumento = (100-imagenAEditarHSL[i][j][1])/5
                    valorDeDisminucion = valorDeAumento*2.5-1
                elif imagenAEditarHSL[i][j][1] <= 65 and imagenAEditarHSL[i][j][1] > 30:
                    valorDeDisminucion = (100-imagenAEditarHSL[i][j][1]-30)/5
                    valorDeAumento = valorDeDisminucion*2.5-1
                
            
                diferenciaFinal = 0

                if valorIluminaciones>0:
                    diferenciaFinal = round(valorIluminaciones*valorDeAumento)
                if valorIluminaciones<0:
                    diferenciaFinal = round(valorIluminaciones*valorDeDisminucion)


                r = imagenAEditar[i][j][0]+diferenciaFinal
                g = imagenAEditar[i][j][1]+diferenciaFinal
                b = imagenAEditar[i][j][2]+diferenciaFinal

                if r>255:
                    r=255
                if g>255:
                    g=255
                if b>255:
                    b=255
                
                if r<0:
                    r=0
                if g<0:
                    g=0
                if b<0:
                    b=0

                aux.append((r,g,b))

            nuevaImagen.append(aux)
        
        nuevaImagen = np.asarray(nuevaImagen)

        exposicion = Image.fromarray(np.uint8(nuevaImagen))
        exposicion = ImageEnhance.Brightness(exposicion)
        multiplicador = 0
        multiplicador = 0.23*valorIluminaciones
        nuevaImagen = np.asarray(exposicion.enhance(1+multiplicador))

        return nuevaImagen

    def Sombras(self, valorSombras, imagenAEditar, imagenAEditarHSL):
        nuevaImagen = []

        alto = len(imagenAEditarHSL)
        ancho = len(imagenAEditarHSL[0])


        for i in range (alto):
            aux = []
            for j in range(ancho):
                valorDeAumento = 0
                valorDeDisminucion = 0

                if imagenAEditarHSL[i][j][1] > 35 and imagenAEditarHSL[i][j][1] < 70:
                    valorDeAumento = (imagenAEditarHSL[i][j][1]-35)/5
                    valorDeDisminucion = valorDeAumento*2.5-1
                elif imagenAEditarHSL[i][j][1] <= 35 and imagenAEditarHSL[i][j][1] >= 0:
                    valorDeDisminucion = (imagenAEditarHSL[i][j][1])/3
                    valorDeAumento = valorDeDisminucion*2.5-1
            
                diferenciaFinal = 0

                if valorSombras>0:
                    diferenciaFinal = round(valorSombras*valorDeAumento)
                if valorSombras<0:
                    diferenciaFinal = round(valorSombras*valorDeDisminucion)

                #print(diferenciaFinal)

                r = imagenAEditar[i][j][0]+diferenciaFinal
                g = imagenAEditar[i][j][1]+diferenciaFinal
                b = imagenAEditar[i][j][2]+diferenciaFinal

                if r>255:
                    r=255
                if g>255:
                    g=255
                if b>255:
                    b=255
                
                if r<0:
                    r=0
                if g<0:
                    g=0
                if b<0:
                    b=0

                aux.append((r,g,b))

            nuevaImagen.append(aux)
        
        nuevaImagen = np.asarray(nuevaImagen)
   
        if valorSombras>0:
            edicionAdicional = Image.fromarray(np.uint8(nuevaImagen))
            edicionAdicional = ImageEnhance.Contrast(edicionAdicional)
            multiplicador = -0.05*valorSombras
            nuevaImagen = np.asarray(edicionAdicional.enhance(1+multiplicador))
            edicionAdicional = Image.fromarray(np.uint8(nuevaImagen))
            edicionAdicional = ImageEnhance.Brightness(edicionAdicional)
            multiplicador = 0.25*valorSombras
            nuevaImagen = np.asarray(edicionAdicional.enhance(1+multiplicador))
        elif valorSombras<0:
            nuevaImagenHSL = self.RGBtoHSL(nuevaImagen)
            multiplicador = 0.5*valorSombras
            nuevaImagen = self.Negros(multiplicador, nuevaImagen, nuevaImagenHSL)
            edicionAdicional = Image.fromarray(np.uint8(nuevaImagen))
            edicionAdicional = ImageEnhance.Color(edicionAdicional)
            multiplicador = 0.2*valorSombras
            nuevaImagen = np.asarray(edicionAdicional.enhance(1+multiplicador))

        return nuevaImagen

    def EditarImagen(self, imagenAEditar, parametros):
        imagenFinal = imagenAEditar
        imagenFinalHSL = self.RGBtoHSL(imagenFinal)
        imagenFinal = self.Exposicion(parametros.exposicion, imagenFinal)
        imagenFinal = self.Contraste(parametros.contraste, imagenFinal)
        imagenFinal = self.Iluminaciones(parametros.iluminaciones, imagenFinal, imagenFinalHSL)
        imagenFinal = self.Sombras(parametros.sombras, imagenFinal, imagenFinalHSL)
        imagenFinal = self.Blancos(parametros.blancos, imagenFinal, imagenFinalHSL)
        imagenFinal = self.Negros(parametros.negros, imagenFinal, imagenFinalHSL)
        return imagenFinal
        
    def EjecutarAlgoritmo(self, imagenBaseHSL):
        self.GenerarParametrosAleatorios(100)
        contador = 0
        contadorBucle = 0
        mejorAnterior = 0
        mejorNueva = 0
        while self.mejorParametro == "":
            for i in range (len(self.parametros)):
                imagenATratarHSL = self.RGBtoHSL(self.EditarImagen(self.abstraccionRGB, self.parametros[i]))
                self.parametros[i].Procesar(imagenBaseHSL, imagenATratarHSL)
                if self.parametros[i].calificacion > self.calificacionMayorActual.calificacion:
                    self.calificacionMayorActual = self.parametros[i]
                    contadorBucle = 0
                if self.parametros[i].calificacion > 0.95:
                    self.mejorParametro = self.parametros[i]
                    break
                if contadorBucle>=5:
                    if self.calificacionMayorActual.calificacion != 0.8:
                        self.mejorParametro = self.calificacionMayorActual
                        break
                    elif contadorBucle == 20:
                        self.mejorParametro = self.calificacionMayorActual
                        break
            mejorAnterior = mejorNueva
            mejorNueva = self.calificacionMayorActual.calificacion
            if self.mejorParametro == "": 
                self.SeleccionarMejoresParametros()
                self.EvolucionarParametros()
                if len(self.parametros) < 50:
                    self.GenerarParametrosAleatorios(100)
                else:
                    self.GenerarParametrosAleatorios(50)
            contador = contador +1
            if mejorAnterior == mejorNueva:
                contadorBucle = contadorBucle+1
            else:
                contadorBucle = 0
            print("Procesando "+str(contador)+".   La calificación mayor actual es: "+str(self.calificacionMayorActual.calificacion))
        imagenFinal = self.EditarImagen(self.imagenRGB, self.mejorParametro)
        print("Exposicion: "+str(self.mejorParametro.exposicion))
        print("Contraste: "+str(self.mejorParametro.contraste))
        print("Iluminaciones: "+str(self.mejorParametro.iluminaciones))
        print("Sombras: "+str(self.mejorParametro.sombras))
        print("Blancos: "+str(self.mejorParametro.blancos))
        print("Negros: "+str(self.mejorParametro.negros))
        print("----------------------------------------------------------------------")
        self.RetornarImagen(imagenFinal)
        return self.rutaImagenFinal