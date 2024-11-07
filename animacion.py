import pygame
import numpy as np
from leerNumpy import devolverMapas
from funciones import *


class protagonista():
    """
    Las animaciones de movimiento estan entre 
    100 , 101 , 102 abajo
    103 , 104 , 105 derecha
    106 , 107 , 108 izquierda
    109 , 110 , 111 arriba
    """
    def __init__(self,nombreImagenes,escalaImagenes,frameMaxmimo,botonesValidos):
        self.frameMaximo = frameMaxmimo

        self.frameSiguiente = -10
        self.siguienteSprite = 0

        self.controles = botonesValidos

        self.spriteArriba = [nombreImagenes['100'],nombreImagenes['101'],nombreImagenes['102']]
        self.escalaArriba = [escalaImagenes['100'],escalaImagenes['101'],escalaImagenes['102']]
        self.spriteAbajo = [nombreImagenes['109'],nombreImagenes['110'],nombreImagenes['111']]
        self.escalaAbajo = [escalaImagenes['109'],escalaImagenes['110'],escalaImagenes['111']]
        self.spriteDerecha = [nombreImagenes['103'],nombreImagenes['104'],nombreImagenes['105']]
        self.escalaDerecha = [escalaImagenes['103'],escalaImagenes['104'],escalaImagenes['105']]
        self.spriteIzquierda = [nombreImagenes['106'],nombreImagenes['107'],nombreImagenes['108']]
        self.escalaIzquierda = [escalaImagenes['106'],escalaImagenes['107'],escalaImagenes['108']]

        self.spriteActual = self.spriteAbajo[0]
        self.escalaActual = self.escalaAbajo[0]

        self.boton = None
    
    def actualizar(self,botones,frame):
        boton = None
        if botones == []:
            self.boton = None
            self.frameSiguiente = -10
            self.siguienteSprite = 0
            self.spriteActual = self.spriteAbajo[0]
            self.escalaActual = self.escalaAbajo[0]
        else:
            boton = botones[0]
            if boton != self.boton:
                self.frameSiguiente = -10
                self.siguienteSprite = 0
                self.boton = boton
            
            if self.frameSiguiente == -10 or frame == self.frameSiguiente and boton != None:
                self.siguienteSprite += 1
                if self.controles[0] == self.boton:
                    if(frame + 10 > self.frameMaximo):
                        self.frameSiguiente = frame + 10 - self.frameMaximo
                    else:
                        self.frameSiguiente = frame + 10
                    
                    if self.siguienteSprite >= 3:
                        self.siguienteSprite = 0
                    self.spriteActual = self.spriteIzquierda[self.siguienteSprite]
                    self.escalaActual = self.escalaIzquierda[self.siguienteSprite]
                
                if self.controles[1] == self.boton:
                    if(frame + 10 > self.frameMaximo):
                        self.frameSiguiente = frame + 10 - self.frameMaximo
                    else:
                        self.frameSiguiente = frame + 10
                    
                    if self.siguienteSprite >= 3:
                        self.siguienteSprite = 0
                    self.spriteActual = self.spriteAbajo[self.siguienteSprite]
                    self.escalaActual = self.escalaAbajo[self.siguienteSprite]

                if self.controles[2] == self.boton:
                    if(frame + 10 > self.frameMaximo):
                        self.frameSiguiente = frame + 10 - self.frameMaximo
                    else:
                        self.frameSiguiente = frame + 10
                    
                    if self.siguienteSprite >= 3:
                        self.siguienteSprite = 0
                    self.spriteActual = self.spriteDerecha[self.siguienteSprite]
                    self.escalaActual = self.escalaDerecha[self.siguienteSprite]

                if self.controles[3] == self.boton:
                    if(frame + 10 > self.frameMaximo):
                        self.frameSiguiente = frame + 10 - self.frameMaximo
                    else:
                        self.frameSiguiente = frame + 10
                    
                    if self.siguienteSprite >= 3:
                        self.siguienteSprite = 0
                    self.spriteActual = self.spriteArriba[self.siguienteSprite]
                    self.escalaActual = self.escalaArriba[self.siguienteSprite]
            
        #print(f"frame actual {frame} -> siguiente frame {self.frameSiguiente} siguiente frame {self.siguienteSprite}")

pygame.init()
ventanax= 980
ventanay = 520
escalax = 50
escalay = 50
ventana = pygame.display.set_mode((ventanax,ventanay))


clock = pygame.time.Clock()
abierto = True
contarFrame = 0
frameMaximo = 30

botonesPresionados = []
botonesValidos = [pygame.K_a,pygame.K_s,pygame.K_d,pygame.K_w]

nombreImagenes,escalaImagenes = devolverMapas()
MapaScript = get_mapaSprit(nombreImagenes)
prota = protagonista(nombreImagenes=MapaScript,escalaImagenes=escalaImagenes,frameMaxmimo=frameMaximo,botonesValidos=botonesValidos)

while abierto:
    contarFrame += 1
    #print(contarFrame)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            abierto = False
        if event.type == pygame.KEYDOWN:
            if event.key in botonesValidos:
                teclaPulsada = event.key
                if not (teclaPulsada in botonesPresionados):
                    botonesPresionados.append(teclaPulsada)
        if event.type == pygame.KEYUP:
            teclaPulsada = event.key
            if teclaPulsada in botonesValidos:
                botonesPresionados.remove(teclaPulsada)
    
    prota.actualizar(botonesPresionados,contarFrame)


    clock.tick(frameMaximo)
    if contarFrame == frameMaximo: contarFrame = -1


    ventana.fill("black")

    imagen = pygame.transform.scale(
                    prota.spriteActual,
                    (escalax*prota.escalaActual[0],escalay*prota.escalaActual[1])
                    )
    
    posicion = prota.spriteActual.get_rect()
    posicion.move_ip(ventanax/2,ventanay/2)
    ventana.blit(imagen,posicion)
    pygame.display.flip()


    

pygame.quit()
    

