import numpy as np
def calEnergyBelow250(fftFrames,fs,frameSize=256):
	fftFrames = np.abs(fftFrames)
	trh = int(250.0/fs*frameSize)
	energyBelow250 = []
	
	for fft in fftFrames:
		total = np.sum(fft)
		curEnergyBelow250 = np.sum(fft[:trh+1])
		if total==0:
			energyBelow250.append(0)
		else:
			energyBelow250.append(2*curEnergyBelow250/total)
		
	return energyBelow250