import pygame
import os
from leer import devolverMapas

def get_mapaSprit(map:"{str,str}"):
    MapaSprit = {}
    for i in map:
        MapaSprit[i] = pygame.image.load(map[i])
    return MapaSprit

pygame.init()
ventana = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
abierto = True

MapaNombre,MapaEscala = devolverMapas()
MapaScript = get_mapaSprit(MapaNombre)
print(MapaScript)
rosa = pygame.image.load("./Dibujos/Rosa.png")
azul = pygame.image.load("./Dibujos/Azul.png")
verde = pygame.image.load("./Dibujos/Verde.png")
matriz = [
    ["AgPro","AgPro","AgPro","Niev","Niev","AgPro","AgPro","AgPro","AgPro","AgPro"],
    ["AgPro","Ag","Ag","Niev","Niev","Ag","Ag","AgPro"],
    ["AgPro","Ag","Tie","A","A","Tie","Ag","AgPro"],
    ["AgPro","Ag","Tie","A","A","Tie","Ag","AgPro"],
    ["AgPro","Ag","Ag","Cam","Cam","Ag","Ag","AgPro"],
    ["AgPro","AgPro","AgPro","AgPro","AgPro","AgPro","AgPro","AgPro"]
]
mx = 100
my = 100
dx = 30
dy = 30
sx= 0
sy = 0
cont = 0
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
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            valor = matriz[i][j]
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
