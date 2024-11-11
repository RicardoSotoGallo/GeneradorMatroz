import pygame
import numpy as np
import os
from leerNumpy import devolverMapas
from funciones import *
from seres import *

pygame.init()
ventanax= 1000
ventanay = 800
ventana = pygame.display.set_mode((ventanax,ventanay))
clock = pygame.time.Clock()
abierto = True
contarFrame = 0
frameMaximo = 30

MapaNombre,MapaEscala = devolverMapas()
MapaScript = get_mapaSprit(MapaNombre)
matriz = iniciarMapa()
actualX = int(matriz.shape[0]/2)
actualY = int(matriz.shape[0]/2)
dx = 20
dy = 20
botonesValidos = [pygame.K_a,pygame.K_s,pygame.K_d,pygame.K_w]
teclaPulsadaLista = []
prota = protagonista(nombreImagenes=MapaScript,escalaImagenes=MapaEscala,frameMaxmimo=frameMaximo,botonesValidos=botonesValidos)




while abierto:
    contarFrame += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            abierto = False
        #teclado
        if event.type == pygame.KEYDOWN:
            if event.key in botonesValidos:
                teclaPulsadaLista.append(event.key)
        elif event.type == pygame.KEYUP and event.key in teclaPulsadaLista:
            teclaPulsadaLista.remove(event.key)
    if teclaPulsadaLista != []:
        if teclaPulsadaLista[0] == pygame.K_a:
            #las variables del tamaño se van a ir modificando cuando hagamos el procedural
            actualX = max([0, actualX - 1])
        if teclaPulsadaLista[0] == pygame.K_d:
            actualX = min([ matriz.shape[0], actualX + 1])
        if teclaPulsadaLista[0] == pygame.K_s:
            actualY = min([ matriz.shape[1], actualY + 1 ]) 
        if teclaPulsadaLista[0] == pygame.K_w:
            actualY = max([ 0 , actualY - 1])
    clock.tick(frameMaximo)
    ventana.fill("black")
    dibujar_fondo(  matriz,
                  MapaScript,
                  MapaEscala,
                  ventana,
                  actualX,actualY,
                  #10,10,
                  int( ventanax/(dx*2)) ,int( ventanay/(dy*2)),
                  dx,dy)
    
    prota.actualizar(teclaPulsadaLista,contarFrame)
    dibujarSer(
        prota,
        ventana,
        dx,dy
        ,int( ventanax/(dx*2)) , int( ventanay/(dy*2))
    )


    pygame.display.flip()
    
    if contarFrame == frameMaximo: contarFrame = -1
pygame.quit()