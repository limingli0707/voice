from math import ceil
import numpy as np
def enframe(x,win,overlap):
	'''Split signal up into (overlapping) frames: .

	Inputs:		x:	  input signal
				win:   window length in samples
				overlap:   frame overlap in samples

	Outputs:	f 	  enframed signal
				n	  total frame number'''

	step = win - overlap
	totalNum = len(x)
	n = int(ceil((totalNum-step)/overlap+1))
	f = []
	for i in range(n):
		curFrame = x[i*step:min(totalNum,i*step+win)]
		#To avoid DC bias, usually we need to perform mean subtraction on each frame
		curFrame = curFrame - np.mean(curFrame)
		f.append(curFrame)
	return f,n



