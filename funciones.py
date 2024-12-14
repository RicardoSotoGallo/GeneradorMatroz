import pygame
import numpy as np

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

def dibujarOtros(posiciones,Xrel,Yrel,xAbs,yAbs,dx,dy,MapaScript,MapaEscala,ventana,tVentanaX,tVentanaY):
    valor = '100'
    for i in posiciones:
        #print(i)
        vectorDiferencia = sumarVectores(i,[-xAbs,-yAbs])
        #posRel = sumarVectores(vectorDiferencia,[Xrel,Yrel])
        posRel = vectorDiferencia
        mx = posRel[0]
        my = posRel[1]
        #print(f"absoluta ({i[0]},{i[1]})")
        #print(f"diferencia ({mx},{my})")
        imagen = pygame.transform.scale(
                    MapaScript[valor],
                    (dx*MapaEscala[valor][0],dy*MapaEscala[valor][1])
                    )
        posicion = MapaScript[valor].get_rect()
        posicion.move_ip(mx*dx+tVentanaX*dx,my*dy+tVentanaY*dy)
        ventana.blit(imagen,posicion)

def sumarVectores(v1,v2):
    return [v1[0] + v2[0] , v1[1] + v2[1]]