
def devolverMapas(dir:"str"="Dibujos/definir.txt"):
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