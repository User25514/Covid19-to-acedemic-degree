
import matplotlib.pyplot as plt
import numpy as np
import math
bodyWeight = 170
StandardD = 40
H0 = 170
SampleSize = 64
print(40/(math.sqrt(SampleSize)))
sampleMean = 173
print((sampleMean-bodyWeight)/(40/(math.sqrt(SampleSize))))
for sampleMean in range (100,300):
    #print(sampleMean)
    #print((sampleMean-bodyWeight)/(40/(math.sqrt(SampleSize))))
    plt.plot(sampleMean, ((sampleMean-bodyWeight)/(40/(math.sqrt(SampleSize)))), 'o')
plt.show()