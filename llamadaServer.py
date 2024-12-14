import requests
import random
import numpy as np
import time
import os

# URL base del servidor
base_url =  "http://kubernetes.procsmocscimsi.uk/"
#"http://kubernetes.procsmocscimsi.uk/"
#"http://127.0.0.1:6969"

x = 0
y = 0

posId = 0
posX = 0
posY = 0
tasaActualizacion = 2
def siguientePedido(xe,ye):
    global x,y
    x = xe
    y = ye

# Función para hacer login y obtener un ID de usuario
def login():
    response = requests.get(f"{base_url}/login")
    if response.status_code == 200:
        data = response.json()
        print(f"Login exitoso: {data}")
        return data["id"]
    else:
        print(f"Error en login: {response.status_code}")
        return None

def preMandarPosiciones(id, x, y):
    global posId,posX,posY
    posId = id
    posX = x
    posY = y

# Función para mandar posición
def mandar_posicion():
    global posId , posX , posY, tasaActualizacion
    print(f"mandar posi -> ({posX},{posY})")
    response = requests.post(f"{base_url}/posicion/{posId}/{posX}/{posY}")
    if response.status_code == 200:
        print(f"Posición enviada: {response.json()}")
        tasaActualizacion = 2
    else:
        print(f"Error al enviar posición: {response.status_code}")
        tasaActualizacion = 100


# Función para pedir objeto
def pedir_objeto(): #x y
    global x,y,tasaActualizacion
    if tasaActualizacion != 200:
        response = requests.get(f"{base_url}/objects/{x}/{y}")
        
        if response.status_code == 200:
            #f"arboles/arbol{posiciones[0][0]}_{posiciones[0][1]}.npy"
            ruta = f"arboles/arbol{x}_{y}.npy"
            os.makedirs(os.path.dirname(ruta), exist_ok=True)
            with open(ruta, "wb") as f:
                f.write(response.content)
            print(f"Objeto recibido y guardado en: {ruta}")
            return np.load(ruta)
        else:
            print(f"Error al pedir objeto: {response.status_code}")
            return None

# Función para pedir bioma
def pedir_bioma(): #x, y
    global x,y
    response = requests.get(f"{base_url}/biomes/{x}/{y}")
    if response.status_code == 200:
       
        ruta =  f"entrda/plano{x}_{y}.npy"
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "wb") as f:
            f.write(response.content)
            print(f"Bioma recibido y guardado en: {ruta}")
        #return response
    else:
        print(f"Error al pedir bioma: {response.status_code}")
        #return None


# Función para obtener posiciones
def obtener_posiciones():
    global posId
    response = requests.get(f"{base_url}/lista_posiciones/{posId}")
    if response.status_code == 200:
        posi = response.json()["posiciones"]
        with open('posiciones.txt', 'w') as fichero:
            for i in posi:
                if i != None:
                    fichero.write(f"{i[0]},{i[1]}\n")
    else:
        print(f"Error al obtener posiciones: {response.status_code}")

# Función para hacer logout
def logout(id):
    response = requests.post(f"{base_url}/logout/{id}")
    if response.status_code == 200:
        print(f"Logout exitoso: {response.json()}")
    else:
        print(f"Error en logout: {response.status_code}")

def main():
    # Login
    user_id = login()
    if user_id is None:
        exit()

    # Mandar posición aleatoria
    x, y = random.randint(0, 10), random.randint(0, 10)
    mandar_posicion(user_id, x, y)

    # Pedir objeto y guardarlo en una variable
    objeto = pedir_objeto(x, y)

    # Mandar otra posición aleatoria
    time.sleep(30)
    x, y = random.randint(0, 10), random.randint(0, 10)
    mandar_posicion(user_id, x, y)

    # Pedir bioma
    bioma = pedir_bioma(x, y)

    # Obtener posiciones
    obtener_posiciones(user_id)

    # Logout
    time.sleep(60)
    logout(user_id)

# user_id = login()

# preMandarPosiciones(user_id,10,20)
# mandar_posicion()
# obtener_posiciones()
# logout(user_id)
# if __name__ == "__main__":
#     main()