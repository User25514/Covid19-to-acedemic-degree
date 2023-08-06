
# Import libraries
import matplotlib.pyplot as plt
import numpy as np
 
 
# Creating dataset
a = np.array([[0.2,0.6,0.2], [0.3,0,0.7], [0.5,0,0.5,]])
b = np.array([0, 1.0, 0])
while True:
    c = np.matmul(b,a)
    if str(c) == str(b):
        break
    else:
        b = c
    print(b)
a = np.array([[0.9,0.1],[0.2,0.8]])
print(np.matmul(a,a))