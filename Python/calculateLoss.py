import numpy as np
from sympy import *

x = Symbol('x')
A, B, C = np.polyfit([-2,0,2,3],[4,0,4,17],2)
y = A*x**2 + B*x + C
yprime = str(y.diff(x))
arr = yprime.split(' + ')
answer = (float(arr[1]) * -1)/(float(arr[0][0:-2]))
print(answer)
