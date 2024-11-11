import pygame
import numpy as np
from leerNumpy import devolverMapas

def get_mapaSprit(map:"{str,str}"):
    MapaSprit = {}
    for i in map:
        MapaSprit[i] = pygame.image.load(map[i])
    return MapaSprit

def dibujar_fondo_Antiguo(matriz,dx,dy,mx,my,MapaScript,MapaEscala,ventana):
    tamanox = matriz.shape[0]
    tamanoy = matriz.shape[1]
    #Programar
    for i in range(tamanox):
        for j in range(tamanoy):
            valor = str(int( matriz[i,j]))
            imagen = pygame.transform.scale(
                    MapaScript[valor],
                    (dx*MapaEscala[valor][0],dy*MapaEscala[valor][1])
                    )
            posicion = MapaScript[valor].get_rect()
            posicion.move_ip(j*dx+mx,i*dy+my)
            ventana.blit(imagen,posicion)

def dibujar_fondo(matrizDibujar,MapaSprite,MapaEscala,ventana,X,Y,tamVentanaX,tamVentanaY,dx,dy):
    rangoX = range(
        X - tamVentanaX - 5 if X - tamVentanaX - 5 > 0 else 0,
        X + tamVentanaX + 5 if X + tamVentanaX  + 5 < matrizDibujar.shape[0] else matrizDibujar.shape[0]
    )
    rangeY = range( 
        Y - tamVentanaY - 5 if Y - tamVentanaY - 5 > 0 else 0,
        Y + tamVentanaY + 5 if Y + tamVentanaY + 5 < matrizDibujar.shape[1] else  matrizDibujar.shape[1]
    )
    #print(f"rango -> {rangoX} : {rangeY}")
    
    for i in rangoX:
        for j in rangeY:
            valor = str(int( matrizDibujar[i,j]))
            imagen = pygame.transform.scale(
                    MapaSprite[valor],
                    (dx*MapaEscala[valor][0],dy*MapaEscala[valor][1])
                    )
            posicion = MapaSprite[valor].get_rect()
            posicion.move_ip((i - rangoX.start - 5) * dx + tamVentanaX , (j - rangeY.start - 5) * dy + tamVentanaY)
            ventana.blit(imagen,posicion)

def dibujarSer(ser,ventana,escalaX,escalaY,posicionX,posicionY):
    imagen = pygame.transform.scale(
                    ser.spriteActual,
                    (escalaX*ser.escalaActual[0],escalaY*ser.escalaActual[1])
                    )
    
    posicion = ser.spriteActual.get_rect()
    posicion.move_ip(posicionX*escalaX,posicionY*escalaY)
    ventana.blit(imagen,posicion)

def anadirMatriz(matrizOriginal,direccion,posicionX,posicionY,accion):
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
    nuevo = [np.load(i) for i in direccion]
    if accion == "arriba" or accion == "abajo":
        anadir = nuevo[0]
        for i in nuevo[1:]:
            anadir = np.concatenate((anadir,i),axis=1)
        tamanoorigen = matrizOriginal.shape[1]
        tamanoDire = sum( map(lambda x : x.shape[1], nuevo))
        """print("================================")
        print(matrizOriginal.shape)
        print("================================")
        print(anadir.shape)
        print("================================")
        print(matrizOriginal)
        print("================================")
        print(anadir)
        print("================================")"""
        if ( tamanoDire == tamanoorigen):
            print("Correcto")
            if accion == "arriba":
                matrizOriginal = np.concatenate((anadir,matrizOriginal),axis=0)
            elif accion == "abajo":
                matrizOriginal = np.concatenate((matrizOriginal,anadir),axis=0)
        else:
            print("Tamaño incorrecto")
    
    if accion == "derecha" or accion == "izquierda":
        anadir = nuevo[0]
        for i in nuevo[1:]:
            anadir = np.concatenate((anadir,i),axis=0)
        tamanoorigen = matrizOriginal.shape[0]
        tamanoDire = sum( map(lambda x : x.shape[0], nuevo))
        """print("================================")
        print(tamanoorigen)
        print("================================")
        print(tamanoDire)
        print("================================")
        print(matrizOriginal)
        print("================================")
        print(anadir)
        print("================================")"""
        if ( tamanoDire == tamanoorigen):
            print("Correcto")
            if accion == "derecha":
                matrizOriginal = np.concatenate((matrizOriginal,anadir),axis=1)
            elif accion == "izquierda":
                matrizOriginal = np.concatenate((anadir,matrizOriginal),axis=1)
        else:
            print("Tamaño incorrecto")
    return matrizOriginal
        

    
def iniciarMapa():
    posiciones = [(1,0),
                (1,-1),
                (1,1),
                (2,-1),(2,0),(2,1),
                (-1,-1),(-1,0),(-1,1)]
    matriz = np.load(f"entrda\plano{posiciones[0][0]}_{posiciones[0][1]}.npy")
    matriz = anadirMatriz(matriz,
                [f"entrda\plano{posiciones[1][0]}_{posiciones[1][1]}.npy"],
                0,0,
                "arriba")
    matriz = anadirMatriz(matriz,
                [f"entrda\plano{posiciones[2][0]}_{posiciones[2][1]}.npy"],
                0,0,
                "abajo")
    print([f"entrda\plano{posiciones[i][0]}_{posiciones[i][1]}.npy" for i in range(3,6)])
    matriz = anadirMatriz(matriz,
                [f"entrda\plano{posiciones[i][0]}_{posiciones[i][1]}.npy" for i in range(3,6)],
                0,0,
                "derecha")
    print([f"entrda\plano{posiciones[i][0]}_{posiciones[i][1]}.npy" for i in range(6,9)])
    matriz = anadirMatriz(matriz,
                [f"entrda\plano{posiciones[i][0]}_{posiciones[i][1]}.npy" for i in range(6,9)],
                0,0,
                "izquierda")
    return matriz

