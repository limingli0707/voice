import numpy as np 
from scipy.signal import iirdesign,lfilter
def calPitch(maxData,frames,fs):
	'''Calculate the signal pitch, regardless vowel or not

	'''
	
	pitch = []
	acf = []
	b, a = iirdesign([60.0*2/fs,950.0*2/fs],[50.0*2/fs,1000.0*2/fs],2,40)
	for frame in frames:
		#cur = lfilter(b,a,frame)
		cur = frame
		curPitch, curAcf = ACF(maxData,cur,fs)
		pitch.append(curPitch)
		acf.append(curAcf)
	return pitch,acf


def ACF(maxData,frame,fs):
	'''Auto-Correlation Function

	Return the fundermental frequency and the its acf value'''

	frameLen = len(frame)
	acf = np.zeros(frameLen)

	for i in range(frameLen):
		acf[i] = np.dot(frame[i:]/maxData,frame[:frameLen-i]/maxData)

	acf[:int(fs/900)] = -1
	pitch = fs/np.argmax(acf)
	acf = max(acf)
	return pitch,acf