import time
import asyncio
import numpy as np

a = np.array([1,2,2,3,4,5])
c = np.array([0,1,0,1,1,0])
b = np.where(c == 1,a,200)
print(a)
print(b)