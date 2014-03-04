import numpy as np
def calFft(frames,fs):
	'''Calculate the descrete fast fourier transform

	Return the fftFrames'''

	fftFrames = []
	frameNum = len(frames)
	
	for i in range(frameNum):
		frame = frames[i]
		fftFrame = np.fft.fft(frame)/len(frame)
		fftFrames.append(fftFrame)
	return fftFrames
