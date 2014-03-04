import math
import numpy as np
def zeroCR(frames,winSize):
	'''Calculate the Zero-Crosing-Rate

	Return a list indicating the Zero-Crosing-Rate'''

	frameNum = len(frames)
	zcr = np.zeros((frameNum,1))
	zcrThread = 400
	length = winSize - 1
	for i in range(frameNum):
		cnt = 0
		#zcrThread = max(frames[i]) / 8
		if i == frameNum-1:
			length = len(frames[i]) - 1
		for j in range(length):
			if(abs(frames[i][j] - frames[i][j+1])>zcrThread):
				if (np.sign(frames[i][j])-np.sign(frames[i][j+1]))!=0:
					cnt = cnt + 1
		#curZCR = cnt*1.0/winSize
		if cnt == 0:
			cnt = 1
		zcr[i] = cnt
	
	return zcr

