import math
import numpy as np
def calEnergy(maxData,waveData):
	frameNum = len(waveData)
	energy = np.zeros((frameNum,1))
	for i in range(frameNum):
		energy[i] = np.sum(waveData[i]/maxData*waveData[i]/maxData)
	return energy