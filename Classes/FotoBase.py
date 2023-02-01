from PIL import Image
import numpy as np

class FotoBase():
    def __init__(self, pathImagen):
        super(FotoBase, self).__init__

        self.imagen = Image.open(pathImagen)
        self.abstraccion = self.AbstraerImagen()
        self.abstraccionRGB = self.ObtenerColoresRGB()
        self.abstraccionHSL = self.RGBtoHSL()

    def AbstraerImagen(self):
        return self.imagen.resize((10,10))
    
    def ObtenerColoresRGB(self):
        return np.asarray(self.abstraccion)
    
    def RGBtoHSL(self):
        hsl = []

        for i in range(10):
            aux = []
            for j in range(10):
                mayor = max(self.abstraccionRGB[i][j], key=int)/255
                menor = min(self.abstraccionRGB[i][j], key=int)/255

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
