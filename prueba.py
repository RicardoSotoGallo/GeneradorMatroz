import time
import asyncio
import numpy as np
import llamadaServer
import threading
import os
import leerNumpy



a = leerNumpy.devolverPosiciones()
print(a)

#Borramos los archivos de chunk
# carpeta = "entrda"
# if os.path.exists(carpeta) and os.path.isdir(carpeta):
#     for archivo in os.listdir(carpeta):
#         ruta_archivo = os.path.join(carpeta, archivo)
        
#         if os.path.isfile(ruta_archivo) and "Cabecera.txt" != archivo:
#             os.remove(ruta_archivo)  # Elimina el archivo
#             print(f"Archivo eliminado: {ruta_archivo}")
# #borramos archivo de arboles
# carpeta = "arboles"
# if os.path.exists(carpeta) and os.path.isdir(carpeta):
#     for archivo in os.listdir(carpeta):
#         ruta_archivo = os.path.join(carpeta, archivo)
        
#         if os.path.isfile(ruta_archivo) and "CabezeraArbol.txt" != archivo:
#             os.remove(ruta_archivo)  # Elimina el archivo
#             print(f"Archivo eliminado: {ruta_archivo}")

def main():
        llamadaServer.siguientePedido(1,1)
        hilo = threading.Thread(target= llamadaServer.pedir_bioma)
        print("Debe de estar antes")
        hilo.start()
        

        

        #print(target)
        # np.save(f"entrda\plano{1}_{1}.npy",target)
        while not(os.path.isfile(f"entrda\plano{1}_{1}.npy")):
            print("Cargando")
        matriz = np.load(f"entrda\plano{1}_{1}.npy")
        print(matriz)
            

#main()