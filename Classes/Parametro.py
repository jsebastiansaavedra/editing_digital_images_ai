

class Parametro():
    def __init__(self, exposicion, contraste, iluminaciones, sombras, blancos, negros):
        super(Parametro, self).__init__

        self.exposicion = exposicion
        self.contraste = contraste
        self.iluminaciones = iluminaciones
        self.sombras = sombras
        self.blancos = blancos
        self.negros = negros
        self.calificacion = 0.0
        self.distanciasFinales = []
        self.porcentajesDeSimilitud = []

    
    def CalcularDistancia(self, abstraccionImagenBaseHSL, abstraccionImagenATratarHSL):
        alto = len(abstraccionImagenBaseHSL)
        ancho = len(abstraccionImagenBaseHSL[0])

        for i in range (alto):
            for j in range (ancho):
                distancias = []
                for k in range (alto):
                    for n in range (ancho):
                        if abstraccionImagenATratarHSL[k][n][1] < 20 or abstraccionImagenATratarHSL[k][n][1] > 80:
                            distancias.append((abs(abstraccionImagenBaseHSL[i][j][1]-abstraccionImagenATratarHSL[k][n][1]))/100)
                        elif abs(abstraccionImagenBaseHSL[i][j][0]-abstraccionImagenATratarHSL[k][n][0]) > 5:
                            distancias.append(0.6)
                        elif abs(abstraccionImagenBaseHSL[i][j][1]-abstraccionImagenATratarHSL[k][n][1]) > 5:
                            distancias.append(0.6)
                        else:
                            distancias.append((abs(abstraccionImagenBaseHSL[i][j][0]-abstraccionImagenATratarHSL[k][n][0])+abs(abstraccionImagenBaseHSL[i][j][1]-abstraccionImagenATratarHSL[k][n][1]))/100)
                self.distanciasFinales.append(min(distancias))
        

    def CalificarSimilitud(self):
        for i in range (len(self.distanciasFinales)):
            if self.distanciasFinales[i] > 0.16:
                self.porcentajesDeSimilitud.append(0.5)
            else:
                self.porcentajesDeSimilitud.append(1-(self.distanciasFinales[i]/2))
        for i in range (len(self.porcentajesDeSimilitud)):
            if self.porcentajesDeSimilitud[i] < 0.8:
                self.calificacion += 0
            else:
                self.calificacion += self.porcentajesDeSimilitud[i]
        self.calificacion = self.calificacion/len(self.porcentajesDeSimilitud)
        

    def Procesar(self, abstraccionImagenBaseHSL, abstraccionImagenATratarHSL):
        self.CalcularDistancia(abstraccionImagenBaseHSL, abstraccionImagenATratarHSL)
        self.CalificarSimilitud()