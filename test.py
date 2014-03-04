from voice import Voice 
import pylab as pl
m = Voice()
m.analyze('../luyin/moni-2.wav')

print m.speech_segment
pl.subplot(311)
pl.plot(m.volume)
pl.subplot(312)
pl.plot(m.zcr)
pl.subplot(313)
pl.plot(m.acf)
pl.show()
'''
m.calFeatures()
m.mood_predict()
m.callInfo()
m.report()
'''