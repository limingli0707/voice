import math
import numpy as np

# method 1: absSum
def calVolume(waveData):
    frameNum = len(waveData)
    volume = np.zeros((frameNum,1))
    for i in range(frameNum):
        volume[i] = np.sum(np.abs(waveData[i]))
    return volume