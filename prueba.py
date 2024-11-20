import numpy as np
import os
"""c = np.array([[1,1,1],[2,2,2],[3,3,3]])
d = np.array([[4,4,4],[5,5,5],[6,6,6]])
e = np.concatenate((c,d),axis=1)
print("========================")
print(c)
print("========================")
print(d)
print("========================")
print(e)
print("========================")"""

#print([1,1,1] - [2,2,2])

def cambio():
    Imayor = 100
    Imenor = -100
    Jmayor = 100
    Jmenor = -100
    for i in range(-20,20):
        for j in range(-20,20):
            if os.path.exists(f"entrda/plano{i}_{j}.npy"):
                print(f"existe {i} {j}")
                if i <= Imayor: Imayor = i
                if i >= Imenor: Imenor = i
                if j <= Jmayor: Jmayor = j
                if j >= Jmenor: Jmenor = j
    print(Imayor)
    print(Imenor)
    print(Jmayor)
    print(Jmenor)
def cambio2():
    for i in range(-20,30):
        for j in range(-20,30):
            if os.path.exists(f"entrda/plano{i}_{j}.npy"):
                if i == 20:
                    os.rename(f"entrda/plano{i}_{j}.npy",f"entrda/plano{4}_{j}.npy")

#cambio2()
#cambio()
