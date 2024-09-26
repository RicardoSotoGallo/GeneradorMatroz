import pygame
import os

pygame.init()
print("comentado")
ventana = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
abierto = True

rosa = pygame.image.load("./Dibujos/Rosa.png")
azul = pygame.image.load("./Dibujos/Azul.png")
verde = pygame.image.load("./Dibujos/Verde.png")
matriz = [
    [0,1,2,1,2,0],
    [2,1,0,0,1,2],
    [1,2,0,1,2,1],
    [0,1,2,2,0,1],
    [2,1,0,2,0,1],
    [1,2,0,0,2,1]
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
        for j in range(len(matriz[0])):
            if matriz[i][j] == 0:
                listImagnes.append(rosa)
                rosaAux = rosa.get_rect()
                rosaAux.move_ip(i*dx+mx,j*dy+my)
                listCosas.append(rosaAux)
            elif matriz[i][j] == 1:
                listImagnes.append(azul)
                azulAux = azul.get_rect()
                azulAux.move_ip(i*dx+mx,j*dy+my)
                listCosas.append(azulAux)
            elif matriz[i][j] == 2:
                listImagnes.append(verde)
                verdeAux = verde.get_rect()
                verdeAux.move_ip(i*dx+mx,j*dy+my)
                listCosas.append(verdeAux)

    #dibujar
    for i in range(len(listImagnes)):
        ventana.blit(listImagnes[i],listCosas[i])
    pygame.display.flip()

pygame.quit()