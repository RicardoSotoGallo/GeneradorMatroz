
def devolverMapas(dir:"str"="Dibujos/definir2.txt"):
    diccionarioNombre = {}
    diccionarioEscalas = {}
    with open(dir,'r') as fichero:
        for linea in fichero:
            split1 = linea.replace('\n','')
            split1 = split1.split(":")
            split2 = split1[2].split(",")
            diccionarioNombre[split1[0]] = split1[1]
            
            diccionarioEscalas[split1[0]] = [int(split2[0]),int(split2[1])]
    return diccionarioNombre,diccionarioEscalas

def devolverPosiciones():
    posi = []
    dir = 'posiciones.txt'
    with open(dir,'r') as fichero:
        for linea in fichero:
                enTexto = linea.replace("\n","").split(",")
                print(enTexto)
                posi.append([ int(enTexto[0]),int(enTexto[1]) ])
    return posi
