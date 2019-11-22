import numpy as np
from sympy import *

x = Symbol('x')
A, B, C = np.polyfit([-2,0,2,3],[4,0,4,17],2)
y = A*x**2 + B*x + C
yprime = y.diff(x)
print(yprime)
