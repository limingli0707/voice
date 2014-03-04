import math
import numpy as np
def calVolumeDB(waveData):
    volume = np.zeros((frameNum,1))
    for i in range(frameNum):
        volume[i] = 10*np.log10(np.sum(waveData[i]*waveData[i]))
    return volume