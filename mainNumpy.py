import pygame
import numpy as np
import os
from leerNumpy import devolverMapas

def get_mapaSprit(map:"{str,str}"):
    MapaSprit = {}
    for i in map:
        MapaSprit[i] = pygame.image.load(map[i])
    return MapaSprit

pygame.init()
ventana = pygame.display.set_mode((1480,720))
clock = pygame.time.Clock()
abierto = True

MapaNombre,MapaEscala = devolverMapas()
MapaScript = get_mapaSprit(MapaNombre)
print(MapaScript)
rosa = pygame.image.load("./Dibujos/Rosa.png")
azul = pygame.image.load("./Dibujos/Azul.png")
verde = pygame.image.load("./Dibujos/Verde.png")
matriz = np.load("entrda\plano3_3.npy")
mx = 10
my = 10
dx = 10
dy = 10
sx= 10
sy = 10
cont = 0
tamanox = matriz.shape[0]
tamanoy = matriz.shape[1]
while abierto:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            abierto = False
    clock.tick(60)  
    ventana.fill("black")
    #Programar
    listCosas = []
    listImagnes = []
    cont += 1
    for i in range(tamanox):
        for j in range(tamanoy):
            valor = str(int( matriz[i,j]))
            listImagnes.append(pygame.transform.scale(
                    MapaScript[valor],
                    (dx*MapaEscala[valor][0],dy*MapaEscala[valor][1])
                    )
                )
            rectAux = MapaScript[valor].get_rect()
            rectAux.move_ip(j*dx+mx,i*dy+my)
            listCosas.append(rectAux)

    #dibujar
    for i in range(len(listImagnes)):
        ventana.blit(listImagnes[i],listCosas[i])
    pygame.display.flip()

pygame.quit()
