import fullRNN
import random

import matplotlib.pyplot as plt
import numpy as np

f = open("output.txt", 'w')
arr = []
xarr = []
for x in range(0,200):
    a, b, c = random.randint(18, 22), random.randint(18, 22), random.randint(18, 22)
    water = fullRNN.getWater('1', a, b, c, "")
    water = (water[0] + water[1])/2
    err = abs(random.randint(int(((200-x)/water))**2-20, int(((200-x)/water))**2+20))
    arr.append(err/15)
    xarr.append(x)
    f.write(str(err/15+1))
    f.write('\n')

plt.plot(xarr, arr, 'o', color='black')

f.close()
plt.show()
