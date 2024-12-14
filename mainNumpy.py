import pygame
from leerNumpy import devolverMapas,devolverPosiciones
from funciones import *
from disenarMapa import *
from seres import *
import os
import llamadaServer



#Borramos los archivos de chunk
carpeta = "entrda"
if os.path.exists(carpeta) and os.path.isdir(carpeta):
    for archivo in os.listdir(carpeta):
        ruta_archivo = os.path.join(carpeta, archivo)
        
        if os.path.isfile(ruta_archivo) and "Cabecera.txt" != archivo:
            os.remove(ruta_archivo)  # Elimina el archivo
            print(f"Archivo eliminado: {ruta_archivo}")
#borramos archivo de arboles
carpeta = "arboles"
if os.path.exists(carpeta) and os.path.isdir(carpeta):
    for archivo in os.listdir(carpeta):
        ruta_archivo = os.path.join(carpeta, archivo)
        
        if os.path.isfile(ruta_archivo) and "CabezeraArbol.txt" != archivo:
            os.remove(ruta_archivo)  # Elimina el archivo
            print(f"Archivo eliminado: {ruta_archivo}")

#prueb
#websocket = websockets.connect(web)
def main():
    user_id = llamadaServer.login()
    if user_id is None:
        print("error de conexion")
    
    pygame.init()   #Iniciar juego

    

    ventanax = 800  #Definir el tamaño x de la ventana
    ventanay = 500  #Definir el tamaño y de la ventana

    llamadaServer.preMandarPosiciones(user_id,192,192)
    llamadaServer.mandar_posicion()
    llamadaServer.obtener_posiciones()
    listaPosiciones = devolverPosiciones()
    #print(listaPosiciones)

    ventana = pygame.display.set_mode((ventanax,ventanay))  #Crea ventana
    clock = pygame.time.Clock()                             #Crea reloj

    abierto = True      #Condicion de encendido del programa
    contarFrame = 0     #Contar para las animacion
    frameMaximo = 30    #El maximo fotograma que va a tener
    contarActualizarInfo = 0
    tasaActulizarInfo = 30
    contarMoviento = 0
    tasaMoviemto = 10

    listaPosiciones = []

    #Carga ajustes del juego
    MapaNombre,MapaEscala = devolverMapas()
    MapaScript = get_mapaSprit(MapaNombre)      #Carga las imagenes lo siento a veces confundo Sprite con Script (dislexia)


    # #Creamos el mapa desde el punto (0,0)
    claseMatriz = matrizMapa()
    claseMatriz.iniciar()
    actualX = int(claseMatriz.matriz.shape[0]/2) #Posicion inicial de x
    actualY = int(claseMatriz.matriz.shape[0]/2) #Posicion inicial de y
    desplazarX = 1 #Cuanto se desplaza por cada frame/o lo que toque
    desplazarY = 1 #Cuanto se desplaza por cada frame/o lo que toque
    dx = 10    #Escala x de las imagenes (he usado D de dimension dx -> dimension x Se que tambien es derivada XD)
    dy = 10   #Escala y de las imagenes

    #Ajustes de controles
    botonesValidos = [pygame.K_a,pygame.K_s,pygame.K_d,pygame.K_w]      #Lista de los controles
    teclaPulsadaLista = []                                              #Lista de controles pulsados

    #Creamos la clase del protagonista
    prota = protagonista(nombreImagenes=MapaScript,escalaImagenes=MapaEscala,frameMaxmimo=frameMaximo,botonesValidos=botonesValidos)

    print(claseMatriz.matriz.shape)


    while abierto:
        
        contarFrame += 1
        contarActualizarInfo += 1
        #contarMoviento += 1

        #Detectar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                llamadaServer.logout(user_id)
                abierto = False
            #teclado
            if event.type == pygame.KEYDOWN:
                if event.key in botonesValidos:
                    teclaPulsadaLista.append(event.key)
            elif event.type == pygame.KEYUP and event.key in teclaPulsadaLista:
                teclaPulsadaLista.remove(event.key)
        
        
        #if contarMoviento == tasaMoviemto:
        #    contarMoviento = -1
            #detectar teclado
        if teclaPulsadaLista != []:
                if teclaPulsadaLista[0] == pygame.K_a:
                    #las variables del tamaño se van a ir modificando cuando hagamos el procedural
                    actualX = max([claseMatriz.sizeX[0], actualX - desplazarX])
                if teclaPulsadaLista[0] == pygame.K_d:
                    actualX = min([ claseMatriz.sizeX[1], actualX + desplazarX])
                if teclaPulsadaLista[0] == pygame.K_s:
                    actualY = min([ claseMatriz.sizeY[1], actualY + desplazarY ]) 
                if teclaPulsadaLista[0] == pygame.K_w:
                    actualY = max([ claseMatriz.sizeY[0] , actualY - desplazarY])
        clock.tick(15)
        
        #Comprobar  si hay que actualizar el mapa
        claseMatriz.comprobarCambio(actualX,actualY)
        
        #Crear fondo
        ventana.fill("black")
        #Dibujar fondo de mapa
        dibujar_fondo(  claseMatriz.matriz,
                    MapaScript,
                    MapaEscala,
                    ventana,
                    actualX + claseMatriz.posicionRelativa[0],
                    actualY + claseMatriz.posicionRelativa[1],
                    #10,10,
                    int( ventanax/(dx*2)) ,int( ventanay/(dy*2)),
                    dx,dy)
        os.system('cls')
        #Actualizar la posicion del prota y la imagen
        prota.actualizar(teclaPulsadaLista,contarFrame)
        print(f"Posicion({actualX},{actualY})  Posicion relativa({actualX + claseMatriz.posicionRelativa[0] , actualY + claseMatriz.posicionRelativa[1]})")
            
        # print(f"size mapa X {claseMatriz.sizeX}  size mapa Y {claseMatriz.sizeY}")
        # print(f"Chunk cargado X {claseMatriz.chunkX}  Chunk cargado Y {claseMatriz.chunkY}")
        # #print(f"Rango a cambiar {claseMatriz.rangoCambiar}")
        # print(f"size un chunk {claseMatriz.sizeUnChunk}  Tamaño del mapa es {claseMatriz.matriz.shape}")
        # print(f"listado de posiciones -> {listaPosiciones}")
        dibujarSer(
            prota,
            ventana,
            dx,dy
            ,int( ventanax/(dx*2)) , int( ventanay/(dy*2))
        )
        
        dibujarOtros(listaPosiciones,
                         actualX + claseMatriz.posicionRelativa[0],
                         actualY + claseMatriz.posicionRelativa[1],
                         actualX,actualY,
                         dx,dy,
                         MapaScript,MapaEscala
                         ,ventana,
                         int( ventanax/((dx*2))) ,int( ventanay/((dy*2))))
        
        
        pygame.display.flip()   #Esperamos al siguiente refresco de imagen
        if contarFrame == frameMaximo: contarFrame = -1     #si los frames llegan a los frame maximo se reinicia
        if contarActualizarInfo == tasaActulizarInfo:
            contarActualizarInfo = 0
            llamadaServer.preMandarPosiciones(user_id,actualX,actualY)
            hiloMandar = threading.Thread(target=llamadaServer.mandar_posicion)
            hiloMandar.start()
            hiloRecopilar = threading.Thread(target=llamadaServer.obtener_posiciones)
            hiloRecopilar.start()
            listaPosiciones = devolverPosiciones()
            
            
    pygame.quit()


main()