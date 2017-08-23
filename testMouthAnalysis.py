# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import re
import pylab
import matplotlib.pyplot as plt

# Load in the text file
file = pd.read_table('results.txt', header = None)
# Take out the duration string value
durationString = str(file.loc[0])[14:16]

# Take out the data
arrayValues = file.values[1:]
arrayValues = arrayValues.tolist()

# List to string conversion
strArrayValues = []
for row in arrayValues:
    strArrayValues.append(str(row))
    
# Float conversion
# Array to hold the jaw angles
floatArray = []
for row in strArrayValues:
    process = re.split("[']",row)
    floatArray.append(float(process[1]))
timeLabel = np.arange(0,int(durationString),step=float(durationString)/len(floatArray))
# Calculating Peaks
peaks = 0
peaksArray = []
peaksTimeLabel = []
for i in range(1,len(floatArray)-1):
    if(floatArray[i] > floatArray[i-1] and floatArray[i] > floatArray[i+1]):
        peaks = peaks + 1
        peaksArray.append(floatArray[i])
        peaksTimeLabel.append(timeLabel[i])
        
# Calculating Troughs
troughs = 0
troughsArray = []
troughsTimeLabel = []
for i in range(1,len(floatArray)-1):
    if(floatArray[i] < floatArray[i-1] and floatArray[i] < floatArray[i+1]):
        troughs = troughs + 1
        troughsArray.append(floatArray[i])
        troughsTimeLabel.append(timeLabel[i])     

plt.plot(timeLabel,floatArray, label ="Jaw Angle", color='k')
#plt.plot(midPointTimeLabel,midPointArray, label ="MidPoint", color='y')
plt.plot(peaksTimeLabel,peaksArray, label ="Peaks", color='r')
#plt.plot(troughsTimeLabel,troughsArray, label ="Troughs", color='b')
plt.xlabel = ('Seconds')
plt.ylabel = ('Values')
plt.title("Peaks:"+str(peaks)+"Troughs:"+str(troughs))
plt.legend()
plt.show()
print("No. of Peaks:",peaks)
print("No. of Troughs:",troughs)
