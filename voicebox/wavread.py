import wave
import numpy as np
def wavread(filename):
	'''
	Read WAVE(.wav) sound file

	[y,Fs,nbits] = wavread(filename)'''


	fs = wave.open(filename,'r')
	params = fs.getparams()
	if params[0]!=1:
		raise Exception('Only mono audio is supported')
	Fs = params[2]
	nbits = params[1]*8
	num = params[3]
	y = fs.readframes(num)
	if nbits == 8:
		dtype = np.int8
	elif nbits == 16:
		dtype = np.int16
	elif nbits == 32:
		dtype = np.int32
	y = np.fromstring(y,dtype = dtype)
	return y,Fs,nbits
