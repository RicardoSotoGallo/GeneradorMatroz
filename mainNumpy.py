import pygame
import numpy as np
import os
from leerNumpy import devolverMapas
from funciones import *

pygame.init()
ventanax= 980
ventanay = 520
ventana = pygame.display.set_mode((ventanax,ventanay))
clock = pygame.time.Clock()
abierto = True

MapaNombre,MapaEscala = devolverMapas()
MapaScript = get_mapaSprit(MapaNombre)
print(MapaScript)
matriz = np.load("entrda\plano3_3.npy")
mx = 0
my = 0
dx = 20
dy = 20
sx= 10
sy = 10
tecla = False
borrarTecla = 0
teclaPulsada = None
while abierto:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            abierto = False
        #teclado
        if event.type == pygame.KEYDOWN:
            borrarTecla = 0
            teclaPulsada = event.key
            tecla = True
        elif event.type == pygame.KEYUP and tecla:
            if teclaPulsada == event.key:
                tecla = False
    if tecla:
        #print(f"{borrarTecla} -> teclado")
        borrarTecla -= 1
        if borrarTecla <= 0:
            borrarTecla = 0
            if teclaPulsada == pygame.K_a:
                #mx = max([-matriz.shape[0]*dx,mx + dx])
                mx = min([0, (mx + dx * 10)])
            if teclaPulsada == pygame.K_d:
                mx = max([-matriz.shape[0]*dx+ventanax, (mx - dx*10)])
            if teclaPulsada == pygame.K_w:
                my = min([0, (my + dy * 10)]) 
            if teclaPulsada == pygame.K_s:
                my = max([-matriz.shape[1]*dy+ventanay, (my - dy*10)])
    clock.tick(60)
    ventana.fill("black")
    #listImagnes,listCosas = 
    dibujar_fondo(matriz=matriz,dx=dx,dy=dy,mx=mx,my=my,MapaScript=MapaScript,MapaEscala=MapaEscala,ventana=ventana)
    pygame.display.flip()
    

pygame.quit()
