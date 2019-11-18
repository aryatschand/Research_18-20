import numpy as np
A, B, C = np.polyfit([-2,0,2],[4,0,4],2)
print(A, 'x^2 +', B, 'x +', C)