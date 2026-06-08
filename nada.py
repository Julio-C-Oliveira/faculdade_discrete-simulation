matriz = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]
c = 3
r = 3

import simpy
import random

def selecionar():
    for i in range(c*r):
        while True:
            s_c = random.randint(0, 2)
            s_r = random.randint(0, 2)

            if matriz[s_c][s_r] == 0:
                matriz[s_c][s_r] = 1
                break
        yield matriz

ordem = selecionar()

for i in ordem:
    for row in i:
        print(row)
    print()
