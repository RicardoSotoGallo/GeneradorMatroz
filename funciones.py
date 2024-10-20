import pygame
import numpy as np
from leerNumpy import devolverMapas

def get_mapaSprit(map:"{str,str}"):
    MapaSprit = {}
    for i in map:
        MapaSprit[i] = pygame.image.load(map[i])
    return MapaSprit

def dibujar_fondo(matriz,dx,dy,mx,my,MapaScript,MapaEscala,ventana):
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