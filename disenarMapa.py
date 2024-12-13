import numpy as np
from leerNumpy import devolverMapas
import os
import llamadaServer
import threading

class matrizMapa():
        
    def iniciar(self):
        self.sizeUnChunk = []
        self.espera = True #estamos esperando a que venga
        #self.vacio = False
        self.iniciarMapa()
        # while self.espera:
        #     #print("Conectando ... ")
        #     pass
        self.sizeX = [0 , self.matriz.shape[0]]
        self.sizeY = [0 , self.matriz.shape[1]]
        self.chunkX = [-1 , 1]
        self.chunkY = [-1 , 1]
        self.rangoCambiar = 40
        self.posicionRelativa = [0,0]
        self.pendiente = []
        self.direPendite = ""
        #self.vacio = True #La lista esta vacia

        
    def insertarArboles(self,mapa,arboles):
        mapi = mapa
        mapa = np.where((arboles == 0) | (mapa == 0) | (mapa == 1) | (mapa == 2) | (mapa == 5),mapa,200)
        return mapa

    def solicitarChunks(self,posiciones):
        #async with websockets.connect(web) as websocket:
        print("Conexión establecida con el servidor.")
        buscamos =list (map(lambda x : f"entrda\plano{x[0]}_{x[1]}.npy",posiciones))
        for i,j in zip (buscamos,posiciones):
            if not(os.path.isfile(i)):
                print(f"Cargado el -> {j}")
                llamadaServer.siguientePedido(j[0],j[1])
                llamadaServer.pedir_bioma()
                llamadaServer.pedir_objeto()
            else:
                print(f"Estan cargado {i}")

    def solicitarChunksHilo(self,xPos,yPos):
        #async with websockets.connect(web) as websocket:

        buscamos = f"entrda\plano{xPos}_{yPos}.npy"
        if not(os.path.isfile(buscamos)):
            print(f"Cargado el -> ({xPos} , {yPos})")
            llamadaServer.siguientePedido(xPos,yPos)
            hiloBioma =  threading.Thread( target= llamadaServer.pedir_bioma )
            hiloObjeto = threading.Thread( target= llamadaServer.pedir_objeto)
            hiloBioma.start()
            hiloObjeto.start()
        else:
            print(f"Estan cargado ({xPos} , {yPos})")
    
    def comprobarCarga(self,posiciones):
        buscamos =list (map(lambda x : f"entrda\plano{x[0]}_{x[1]}.npy",posiciones))
        comprobar = True
        while(comprobar):
            comprobar = False
            #print("Cargando del server")
            for i in buscamos:
                if not(os.path.isfile(i)):
                    comprobar = True

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
        arbol = [np.load(i.replace("entrda","arboles").replace("plano","arbol")) for i in direccion]
        if accion == "arriba" or accion == "abajo":
            anadir = nuevo[0]
            anadir = self.insertarArboles(anadir,arbol[0])
            for i,j in zip( nuevo[1:],arbol[1:]):
                e = self.insertarArboles(i,j)
                #e = i
                anadir = np.concatenate((anadir,e),axis=0)
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
            anadir = self.insertarArboles(anadir,arbol[0])
            for i,j in zip(nuevo[1:],arbol[1:]):
                e = self.insertarArboles(i,j)
                #e = i
                anadir = np.concatenate((anadir,e),axis=1)
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
        
        self.solicitarChunks(posiciones)

        self.comprobarCarga(posiciones)

        self.matriz = np.load(f"entrda\plano{posiciones[0][0]}_{posiciones[0][1]}.npy",allow_pickle=True).T
        arbol = np.load(f"arboles/arbol{posiciones[0][0]}_{posiciones[0][1]}.npy",allow_pickle=True)
        self.matriz = self.insertarArboles(self.matriz,arbol)
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
        self.espera = False

    def comprobarCambio(self,posX,posY):
        if not( self.espera):
            
            #Sobrepasamos margen Izquierda
            if( (posX - self.sizeX[0]) <= self.rangoCambiar ):
                self.enCamino = False
                # self.sizeX = [self.sizeX[0] - self.sizeUnChunk[0] ,
                #               self.sizeX[1] - self.sizeUnChunk[0]]
                # self.chunkX = [self.chunkX[0] -1 , self.chunkX[1] -1]
                #self.matriz = self.matriz[:2*self.sizeUnChunk[0],:]
                #Posiciones a cargar
                self.pendiente = [f"entrda\plano{self.chunkX[0]-1}_{i}.npy" for i in range(self.chunkY[0],self.chunkY[1]+1)]
                self.objetoPendiente = [f"arboles/arbol{self.chunkX[0]-1}_{i}.npy" for i in range(self.chunkY[0],self.chunkY[1]+1)]
                #Acciones pedida
                self.direPendite = "izquierda"
                #indice que indica chunk estamos cargando
                self.posicionEspera = 0
                #Posiciones a cargar
                listaPosi = []
                for i in range(self.chunkY[0],self.chunkY[1]+1):
                    listaPosi.append((self.chunkX[0]-1,i))
                
                self.coordenadaPendiente = listaPosi

                #iniciamos la espera
                self.espera = True
            #Sobrepasamos margen Derecha
            elif( (self.sizeX[1] - posX) <= self.rangoCambiar ):
                self.enCamino = False
                # self.sizeX = [self.sizeX[0] + self.sizeUnChunk[0] ,
                #             self.sizeX[1] + self.sizeUnChunk[0]]
                # self.chunkX = [self.chunkX[0] +1 , self.chunkX[1] +1]
                # self.matriz = self.matriz[self.sizeUnChunk[0]:,:]
                #Posiciones a cargar
                self.pendiente = [f"entrda\plano{self.chunkX[1]+1}_{i}.npy" for i in range(self.chunkY[0],self.chunkY[1]+1)]
                self.objetoPendiente = [f"arboles/arbol{self.chunkX[1]+1}_{i}.npy" for i in range(self.chunkY[0],self.chunkY[1]+1)]
                #Acciones pedida
                self.direPendite = "derecha"
                #indice que indica chunk estamos cargando
                self.posicionEspera = 0
                #creamos lista de posiciones
                listaPosi = []
                for i in range(self.chunkY[0],self.chunkY[1]+1):
                    listaPosi.append((self.chunkX[1]+1,i))
                
                self.coordenadaPendiente = listaPosi
                
                #inciamos espera
                self.espera = True

                #self.solicitarChunksHilo(xPos=listaPosi[0][0],yPos=listaPosi[0][1])
                #await self.solicitarChunks(listaPosi,self.url)
                # self.anadirMatriz(
                #     [f"entrda\plano{self.chunkX[1]}_{i}.npy" for i in range(self.chunkY[0],self.chunkY[1]+1)],
                #     "derecha"
                # )
                # self.posicionRelativa[0] = self.posicionRelativa[0] - self.sizeUnChunk[0]
            
            #Sobre pasa margen Arriba
            elif( (posY - self.sizeY[0]) <= self.rangoCambiar ):
                self.enCamino = False
                # self.sizeY = [self.sizeY[0] - self.sizeUnChunk[1] ,
                #             self.sizeY[1] - self.sizeUnChunk[1]]
                # self.chunkY = [self.chunkY[0] -1 , self.chunkY[1] -1]
                # #self.matriz = self.matriz[:,self.sizeUnChunk[1]:]
                # self.matriz = self.matriz[:,:2*self.sizeUnChunk[1]]
                #Posiciones a cargar
                self.pendiente = [f"entrda\plano{i}_{self.chunkY[0] -1}.npy" for i in range(self.chunkX[0],self.chunkX[1]+1)]
                self.objetoPendiente = [f"arboles/arbol{i}_{self.chunkY[0] -1}.npy" for i in range(self.chunkX[0],self.chunkX[1]+1)]
                #Acciones pedida
                self.direPendite = "abajo"
                #indice que indica chunk estamos cargando
                self.posicionEspera = 0
               #Posiciones a cargar
                listaPosi = []
                for i in range(self.chunkX[0],self.chunkX[1]+1):
                    listaPosi.append((i,self.chunkY[0] -1))
                self.coordenadaPendiente = listaPosi
                
                #self.solicitarChunksHilo(xPos=listaPosi[0][0],yPos=listaPosi[0][1])
                #iniciamos espera
                self.espera = True
                #await self.solicitarChunks(listaPosi,self.url)

                # self.anadirMatriz(
                #     [f"entrda\plano{i}_{self.chunkY[0]}.npy" for i in range(self.chunkX[0],self.chunkX[1]+1)],
                #     "abajo"
                # )
                # self.posicionRelativa[1] = self.posicionRelativa[1] + self.sizeUnChunk[1]
                
            #Sobre pasa margen Abajo
            elif( (self.sizeY[1] - posY) <= self.rangoCambiar ):
                self.enCamino = False
                # self.sizeY = [self.sizeY[0] + self.sizeUnChunk[0] ,
                #             self.sizeY[1] + self.sizeUnChunk[0]]
                # self.chunkY = [self.chunkY[0] +1 , self.chunkY[1] +1]
                # #self.matriz = self.matriz[:,:2*self.sizeUnChunk[1]]
                # self.matriz = self.matriz[:,self.sizeUnChunk[1]:]

                #Posiciones a cargar
                self.pendiente = [f"entrda\plano{i}_{self.chunkY[1] +1}.npy" for i in range(self.chunkX[0],self.chunkX[1]+1)]
                self.objetoPendiente = [f"arboles/arbol{i}_{self.chunkY[1] +1}.npy" for i in range(self.chunkX[0],self.chunkX[1]+1)]
                #Acciones pedida
                self.direPendite = "arriba"
                #indice que indica chunk estamos cargando
                self.posicionEspera = 0
                #Posicion cargada                
                listaPosi = []
                for i in range(self.chunkX[0],self.chunkX[1]+1):
                    listaPosi.append((i,self.chunkY[1] +1))
                
                self.coordenadaPendiente = listaPosi
                # self.solicitarChunksHilo(xPos=listaPosi[0][0],yPos=listaPosi[0][1])
                # self.direccionPendiente = self.pendiente
                
                #iniciamos espera
                self.espera = True
                #self.solicitarChunks(listaPosi)

                # self.anadirMatriz(
                #     [f"entrda\plano{i}_{self.chunkY[1]}.npy" for i in range(self.chunkX[0],self.chunkX[1]+1)],
                #     "arriba"
                # )
                # self.posicionRelativa[1] = self.posicionRelativa[1] - self.sizeUnChunk[1]
                
                
                #self.solicitarChunksHilo(xPos=listaPosi[0][0],yPos=listaPosi[0][1])
                # self.anadirMatriz(
                #     [f"entrda\plano{self.chunkX[0]}_{i}.npy" for i in range(self.chunkY[0],self.chunkY[1]+1)],
                #     "izquierda"
                # )
                # self.posicionRelativa[0] = self.posicionRelativa[0] + self.sizeUnChunk[0]
        elif self.espera and self.posicionEspera < 3:
            #os.system("cls")
            print(f"posicionesBuscadas -> ({self.coordenadaPendiente[self.posicionEspera][0]},{self.coordenadaPendiente[self.posicionEspera][1]})")
            print(f"posicion espera {self.pendiente[self.posicionEspera]} ===== {self.objetoPendiente[self.posicionEspera]}")
            print(f"chun cargado -> {os.path.isfile(self.pendiente[self.posicionEspera])}")
            print(f"objetos cargados -> {os.path.isfile(self.objetoPendiente[self.posicionEspera])}")
            if os.path.isfile(self.pendiente[self.posicionEspera]) and os.path.isfile(self.objetoPendiente[self.posicionEspera]):
                self.posicionEspera += 1
                self.enCamino = False
            else:
                if not (self.enCamino):
                    print(f"Solicitando -> ({self.coordenadaPendiente[self.posicionEspera][0]}, {self.coordenadaPendiente[self.posicionEspera][1]})")
                    self.solicitarChunksHilo(xPos= self.coordenadaPendiente[self.posicionEspera][0]
                                            ,yPos= self.coordenadaPendiente[self.posicionEspera][1])
                    self.enCamino = True
        else:
            self.posicionEspera = 0
            self.espera = False
            self.anadirMatriz(
                    self.pendiente,
                    self.direPendite
                )
            
            if self.direPendite == "izquierda":
                #Actualizamos posicion relativa
                self.posicionRelativa[0] = self.posicionRelativa[0] + self.sizeUnChunk[0]
                #tamaño de x
                self.sizeX = [self.sizeX[0] - self.sizeUnChunk[0] ,
                              self.sizeX[1] - self.sizeUnChunk[0]]
                #actualizamos los chunk escogidos
                self.chunkX = [self.chunkX[0] -1 , self.chunkX[1] -1]
                #luego tamaño
                self.matriz = self.matriz[:3*self.sizeUnChunk[0],:]
                
            elif self.direPendite == "derecha":
                self.posicionRelativa[0] = self.posicionRelativa[0] - self.sizeUnChunk[0]
                self.sizeX = [self.sizeX[0] + self.sizeUnChunk[0] ,
                              self.sizeX[1] + self.sizeUnChunk[0]]
                self.chunkX = [self.chunkX[0] +1 , self.chunkX[1] +1]
                self.matriz = self.matriz[self.sizeUnChunk[0]:,:]
                
            elif self.direPendite == "abajo":
                self.posicionRelativa[1] = self.posicionRelativa[1] + self.sizeUnChunk[1]
                self.sizeY = [self.sizeY[0] - self.sizeUnChunk[1] ,
                              self.sizeY[1] - self.sizeUnChunk[1]]
                self.chunkY = [self.chunkY[0] -1 , self.chunkY[1] -1]
                #self.matriz = self.matriz[:,self.sizeUnChunk[1]:]
                self.matriz = self.matriz[:,:3*self.sizeUnChunk[1]]
                
            elif self.direPendite == "arriba":
                self.posicionRelativa[1] = self.posicionRelativa[1] - self.sizeUnChunk[1]
                self.sizeY = [self.sizeY[0] + self.sizeUnChunk[0] ,
                            self.sizeY[1] + self.sizeUnChunk[0]]
                self.chunkY = [self.chunkY[0] +1 , self.chunkY[1] +1]
                #self.matriz = self.matriz[:,:2*self.sizeUnChunk[1]]
                self.matriz = self.matriz[:,self.sizeUnChunk[1]:]

        
                


        # if self.vacio and not (self.espera):
        #     #Sobrepasamos margen Izquierda
        #     if( (posX - self.sizeX[0]) <= self.rangoCambiar ):
        #         self.sizeX = [self.sizeX[0] - self.sizeUnChunk[0] ,
        #                     self.sizeX[1] - self.sizeUnChunk[0]]
        #         self.chunkX = [self.chunkX[0] -1 , self.chunkX[1] -1]
        #         self.matriz = self.matriz[:2*self.sizeUnChunk[0],:]
        #         self.pendiente = [f"entrda\plano{self.chunkX[0]}_{i}.npy" for i in range(self.chunkY[0],self.chunkY[1]+1)]
        #         self.direPendite = "izquierda"
        #         self.vacio = False
        #         self.espera = True
        #         listaPosi = []
        #         for i in range(self.chunkY[0],self.chunkY[1]+1):
        #             listaPosi.append((self.chunkX[0],i))
                
        #         self.coordenadaPendiente = listaPosi
        #         self.solicitarChunksHilo(xPos=listaPosi[0][0],yPos=listaPosi[0][1])
        #         self.direccionPendiente = self.pendiente
        #         # self.anadirMatriz(
        #         #     [f"entrda\plano{self.chunkX[0]}_{i}.npy" for i in range(self.chunkY[0],self.chunkY[1]+1)],
        #         #     "izquierda"
        #         # )
        #         # self.posicionRelativa[0] = self.posicionRelativa[0] + self.sizeUnChunk[0]
            
        #     #Sobrepasamos margen Derecha
        #     elif( (self.sizeX[1] - posX) <= self.rangoCambiar ):
        #         self.sizeX = [self.sizeX[0] + self.sizeUnChunk[0] ,
        #                     self.sizeX[1] + self.sizeUnChunk[0]]
        #         self.chunkX = [self.chunkX[0] +1 , self.chunkX[1] +1]
        #         self.matriz = self.matriz[self.sizeUnChunk[0]:,:]
        #         self.pendiente = [f"entrda\plano{self.chunkX[1]}_{i}.npy" for i in range(self.chunkY[0],self.chunkY[1]+1)]
        #         self.direPendite = "derecha"
        #         self.vacio = False
        #         self.espera = True
        #         listaPosi = []
        #         for i in range(self.chunkY[0],self.chunkY[1]+1):
        #             listaPosi.append((self.chunkX[1],i))
                
        #         self.coordenadaPendiente = listaPosi
        #         self.solicitarChunksHilo(xPos=listaPosi[0][0],yPos=listaPosi[0][1])
        #         self.direccionPendiente = self.pendiente
        #         #await self.solicitarChunks(listaPosi,self.url)
        #         # self.anadirMatriz(
        #         #     [f"entrda\plano{self.chunkX[1]}_{i}.npy" for i in range(self.chunkY[0],self.chunkY[1]+1)],
        #         #     "derecha"
        #         # )
        #         # self.posicionRelativa[0] = self.posicionRelativa[0] - self.sizeUnChunk[0]
            
        #     #Sobre pasa margen Arriba
        #     elif( (posY - self.sizeY[0]) <= self.rangoCambiar ):
        #         self.sizeY = [self.sizeY[0] - self.sizeUnChunk[1] ,
        #                     self.sizeY[1] - self.sizeUnChunk[1]]
        #         self.chunkY = [self.chunkY[0] -1 , self.chunkY[1] -1]
        #         #self.matriz = self.matriz[:,self.sizeUnChunk[1]:]
        #         self.matriz = self.matriz[:,:2*self.sizeUnChunk[1]]

        #         self.pendiente = [f"entrda\plano{i}_{self.chunkY[0]}.npy" for i in range(self.chunkX[0],self.chunkX[1]+1)]
        #         self.direPendite = "abajo"
        #         self.vacio = False
        #         self.espera = True
        #         listaPosi = []
        #         for i in range(self.chunkX[0],self.chunkX[1]+1):
        #             listaPosi.append((i,self.chunkY[0]))
                
        #         self.coordenadaPendiente = listaPosi
        #         self.solicitarChunksHilo(xPos=listaPosi[0][0],yPos=listaPosi[0][1])
        #         self.direccionPendiente = self.pendiente
        #         #await self.solicitarChunks(listaPosi,self.url)

        #         # self.anadirMatriz(
        #         #     [f"entrda\plano{i}_{self.chunkY[0]}.npy" for i in range(self.chunkX[0],self.chunkX[1]+1)],
        #         #     "abajo"
        #         # )
        #         # self.posicionRelativa[1] = self.posicionRelativa[1] + self.sizeUnChunk[1]
                
        #     #Sobre pasa margen Abajo
        #     elif( (self.sizeY[1] - posY) <= self.rangoCambiar ):
        #         self.sizeY = [self.sizeY[0] + self.sizeUnChunk[0] ,
        #                     self.sizeY[1] + self.sizeUnChunk[0]]
        #         self.chunkY = [self.chunkY[0] +1 , self.chunkY[1] +1]
        #         #self.matriz = self.matriz[:,:2*self.sizeUnChunk[1]]
        #         self.matriz = self.matriz[:,self.sizeUnChunk[1]:]

        #         self.pendiente = [f"entrda\plano{i}_{self.chunkY[1]}.npy" for i in range(self.chunkX[0],self.chunkX[1]+1)]
        #         self.direPendite = "arriba"
        #         self.vacio = False
        #         self.espera = True
        #         listaPosi = []
        #         for i in range(self.chunkX[0],self.chunkX[1]+1):
        #             listaPosi.append((i,self.chunkY[1]))
                
        #         self.coordenadaPendiente = listaPosi
        #         self.solicitarChunksHilo(xPos=listaPosi[0][0],yPos=listaPosi[0][1])
        #         self.direccionPendiente = self.pendiente
        #         #self.solicitarChunks(listaPosi)

        #         # self.anadirMatriz(
        #         #     [f"entrda\plano{i}_{self.chunkY[1]}.npy" for i in range(self.chunkX[0],self.chunkX[1]+1)],
        #         #     "arriba"
        #         # )
        #         # self.posicionRelativa[1] = self.posicionRelativa[1] - self.sizeUnChunk[1]
        # elif not self.vacio:
        #     self.vacio = True
        #     for nombre,posi in zip(self.direccionPendiente,self.coordenadaPendiente):
        #         if not(os.path.isfile(nombre)):
        #             self.vacio = False
        #         else:
        #             self.direccionPendiente.remove(nombre)
        #             self.coordenadaPendiente.remove(posi)
        #             if len(self.pendiente) > 0:
        #                 self.solicitarChunksHilo(self.coordenadaPendiente[0][0],self.coordenadaPendiente[0][1])
        # else:
        #     self.anadirMatriz(
        #             self.pendiente,
        #             self.direPendite
        #         )
        #     self.espera = False
        #     if self.direPendite == "izquierda":
        #         self.posicionRelativa[0] = self.posicionRelativa[0] + self.sizeUnChunk[0]
        #     elif self.direPendite == "derecha":
        #         self.posicionRelativa[0] = self.posicionRelativa[0] - self.sizeUnChunk[0]
        #     elif self.direPendite == "abajo":
        #         self.posicionRelativa[1] = self.posicionRelativa[1] + self.sizeUnChunk[1]
        #     elif self.direPendite == "arriba":
        #         self.posicionRelativa[1] = self.posicionRelativa[1] - self.sizeUnChunk[1]
        
