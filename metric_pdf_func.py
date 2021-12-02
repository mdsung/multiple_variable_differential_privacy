import numpy as np
import time
epsilon = 0.1
value = 0.5

# @profile
def pdf(x: float) -> float:
    """ bounded laplacian distribution pdf"""
    b = 2 / (epsilon)
    c = 1 - 0.5 * (np.exp(-(value + 1)/b) + np.exp(-(1 - value)/b))
    return 1 / (b * c * 2) * np.exp(-np.absolute(x - value)/b) 

start_time = time.time()
elements = np.linspace(-1, 1, 10**5)
pdf(elements)
print(time.time() - start_time)