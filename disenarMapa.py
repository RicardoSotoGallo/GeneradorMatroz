import numpy as np
from leerNumpy import devolverMapas
class matrizMapa():
    def __init__(self):
        self.sizeUnChunk = []
        self.iniciarMapa()
        self.sizeX = [0 , self.matriz.shape[0]]
        self.sizeY = [0 , self.matriz.shape[1]]
        self.chunkX = [-1 , 1]
        self.chunkY = [-1 , 1]
        self.rangoCambiar = 40
        self.posicionRelativa = [0,0]
        

    def anadirMatriz(self,direccion,accion):
        """
        arriba -> Colocar la nueva matriz encima
        abajo -> Colocar la nueva matriz abajo
        derecha -> Colocar la nueva matriz a la derecha
        izquierda -> coloca la nueva matriz izquierda
        las direcciones tiene que ser una lista de direcciones
        """

        """
        Primero vamos a comprobar la operacion si se puede hacer
        """
        nuevo = [np.load(i).T for i in direccion]
        if accion == "arriba" or accion == "abajo":
            anadir = nuevo[0]
            for i in nuevo[1:]:
                anadir = np.concatenate((anadir,i),axis=0)
            tamanoorigen = self.matriz.shape[0]
            tamanoDire = sum( map(lambda x : x.shape[0], nuevo))
            """print("================================")
            print(self.matriz.shape)
            print("================================")
            print(anadir.shape)
            print("================================")
            print(self.matriz)
            print("================================")
            print(anadir)
            print("================================")"""
            if ( tamanoDire == tamanoorigen):
                #print("Correcto")
                if accion == "arriba":
                    self.matriz = np.concatenate((self.matriz,anadir),axis=1)
                elif accion == "abajo":
                    self.matriz = np.concatenate((anadir,self.matriz),axis=1)
            else:
                print("Tamaño incorrecto")
        
        if accion == "derecha" or accion == "izquierda":
            anadir = nuevo[0]
            for i in nuevo[1:]:
                anadir = np.concatenate((anadir,i),axis=1)
            tamanoorigen = self.matriz.shape[1]
            tamanoDire = sum( map(lambda x : x.shape[1], nuevo))
            """print("================================")
            print(tamanoorigen)
            print("================================")
            print(tamanoDire)
            print("================================")
            print(self.matriz)
            print("================================")
            print(anadir)
            print("================================")"""
            if ( tamanoDire == tamanoorigen):
                #print("Correcto")
                if accion == "derecha":
                    self.matriz = np.concatenate((self.matriz,anadir),axis=0)
                elif accion == "izquierda":
                    self.matriz = np.concatenate((anadir,self.matriz),axis=0)
            else:
                print("Tamaño incorrecto")

    def iniciarMapa(self):
        """
        Crea una nueva matriz 
        """
        posiciones = [(0,0),
                    (0,1),
                    (0,-1),
                    (1,-1),(1,0),(1,1),
                    (-1,-1),(-1,0),(-1,1)]
        self.matriz = np.load(f"entrda\plano{posiciones[0][0]}_{posiciones[0][1]}.npy").T
        self.sizeUnChunk = [self.matriz.shape[0] ,self.matriz.shape[1]]
        self.anadirMatriz(
                    [f"entrda\plano{posiciones[1][0]}_{posiciones[1][1]}.npy"],
                    "arriba")
        
        self.anadirMatriz(
                    [f"entrda\plano{posiciones[2][0]}_{posiciones[2][1]}.npy"],
                    "abajo")
        #print([f"entrda\plano{posiciones[i][0]}_{posiciones[i][1]}.npy" for i in range(3,6)])
        self.anadirMatriz(
                    [f"entrda\plano{posiciones[i][0]}_{posiciones[i][1]}.npy" for i in range(3,6)],
                    "derecha")
        #print([f"entrda\plano{posiciones[i][0]}_{posiciones[i][1]}.npy" for i in range(6,9)])
        self.anadirMatriz(
                    [f"entrda\plano{posiciones[i][0]}_{posiciones[i][1]}.npy" for i in range(6,9)],
                    "izquierda")

    def comprobarCambio(self,posX,posY):
        #Sobrepasamos margen Izquierda
        if( (posX - self.sizeX[0]) <= self.rangoCambiar ):
            self.sizeX = [self.sizeX[0] - self.sizeUnChunk[0] ,
                          self.sizeX[1] - self.sizeUnChunk[0]]
            self.chunkX = [self.chunkX[0] -1 , self.chunkX[1] -1]
            self.matriz = self.matriz[:2*self.sizeUnChunk[0],:]
            self.anadirMatriz(
                [f"entrda\plano{self.chunkX[0]}_{i}.npy" for i in range(self.chunkY[0],self.chunkY[1]+1)],
                "izquierda"
            )
            self.posicionRelativa[0] = self.posicionRelativa[0] + self.sizeUnChunk[0]
        
        #Sobrepasamos margen Derecha
        elif( (self.sizeX[1] - posX) <= self.rangoCambiar ):
            self.sizeX = [self.sizeX[0] + self.sizeUnChunk[0] ,
                          self.sizeX[1] + self.sizeUnChunk[0]]
            self.chunkX = [self.chunkX[0] +1 , self.chunkX[1] +1]
            self.matriz = self.matriz[self.sizeUnChunk[0]:,:]
            self.anadirMatriz(
                [f"entrda\plano{self.chunkX[1]}_{i}.npy" for i in range(self.chunkY[0],self.chunkY[1]+1)],
                "derecha"
            )
            self.posicionRelativa[0] = self.posicionRelativa[0] - self.sizeUnChunk[0]
        
        #Sobre pasa margen Arriba
        elif( (posY - self.sizeY[0]) <= self.rangoCambiar ):
            self.sizeY = [self.sizeY[0] - self.sizeUnChunk[1] ,
                          self.sizeY[1] - self.sizeUnChunk[1]]
            self.chunkY = [self.chunkY[0] -1 , self.chunkY[1] -1]
            #self.matriz = self.matriz[:,self.sizeUnChunk[1]:]
            self.matriz = self.matriz[:,:2*self.sizeUnChunk[1]]
            self.anadirMatriz(
                [f"entrda\plano{i}_{self.chunkY[0]}.npy" for i in range(self.chunkX[0],self.chunkX[1]+1)],
                "abajo"
            )
            self.posicionRelativa[1] = self.posicionRelativa[1] + self.sizeUnChunk[1]
            
        #Sobre pasa margen Abajo
        elif( (self.sizeY[1] - posY) <= self.rangoCambiar ):
            self.sizeY = [self.sizeY[0] + self.sizeUnChunk[0] ,
                          self.sizeY[1] + self.sizeUnChunk[0]]
            self.chunkY = [self.chunkY[0] +1 , self.chunkY[1] +1]
            #self.matriz = self.matriz[:,:2*self.sizeUnChunk[1]]
            self.matriz = self.matriz[:,self.sizeUnChunk[1]:]
            self.anadirMatriz(
                [f"entrda\plano{i}_{self.chunkY[1]}.npy" for i in range(self.chunkX[0],self.chunkX[1]+1)],
                "arriba"
            )
            self.posicionRelativa[1] = self.posicionRelativa[1] - self.sizeUnChunk[1]