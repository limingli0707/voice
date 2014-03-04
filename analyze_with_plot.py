from voice import Voice 
import pylab as pl 
import numpy as np
def analyze_with_plot(filename):
	'''Analyze a single voice file and plot its volume, pitch, end_point.

	Example:
		python analyze 'myfile'
	'''
	#print 'Analyzing %s'%filename

	m = Voice()
	m.analyze(filename)
	t = np.linspace(0,len(m.y)*1.0/m.fs,len(m.frames))
	mul = len(m.y)*1.0/m.fs/len(m.frames)
	pl.subplot(311)
	pl.plot(t, m.volume)
	print m.speech_segment
	print mul
	for s in m.speech_segment:
		print s[0]*mul,s[1]*mul
		pl.plot([s[0]*mul,s[0]*mul],[0,max(m.volume)],color='red')
		pl.plot([s[1]*mul,s[1]*mul],[0,max(m.volume)],color='blue')
	pl.subplot(312)
	pl.plot(t, m.pitch)
	pl.subplot(313)
	pl.plot(t, m.energyBelow250)
	pl.show()
	'''
	m.calFeatures()
	m.mood_predict()
	m.callInfo()
	m.report()
	'''
	

if __name__ == '__main__':
	import sys
	import os
	if len(sys.argv) < 2:
		print analyze.__doc__
		sys.exit(0)
	arg = sys.argv[1] 
	analyze_with_plot(arg)
	
	

