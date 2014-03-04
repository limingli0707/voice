#coding=utf-8
from voicebox import wavread,enframe,calVolume,zeroCR,epd,calPitch,calEnergy,uvDecision,calEnergyBelow250,calFft
import pylab as pl 
import numpy as np
from ml_svm import predict,add_to_learn
import json
import config
from collections import OrderedDict
class Voice:
	def __init__(self,report = config.report):
		self.reportFs = open(report,'a')
		#self.logFs = open(log,'a')
		self.label = '0'
	def __del__(self):
		self.reportFs.close()
		#self.logFs.close()

	def learn(self,filename='learn',label='0'):
		try:
			add_to_learn.add_to_learn(filename,self.features,label)
		except Exception as e:
			print e
	
	def mood_predict(self):
		print 'mood_predict ...'
		self.mood = 'silent'
		if self.has_feature==True:
			self.mood = 'normal'
			self.label = predict.predict(self.features)
			for label in self.label:
				if label < 0:
					self.mood = 'abnormal'
					break
		print 'mood_predict result: %s'%self.mood
		
	def analyze(self,filename,frameSize=256,overlap=128):
		print 'analyzing %s'%filename
		self.filename = filename
		self.frameSize = frameSize
		self.overlap = overlap
		try:
			self.y,self.fs,self.nbits = wavread.wavread(filename)
		except Exception as e:
			raise e
		self.frames,self.n = enframe.enframe(self.y,frameSize,overlap)
		self.volume =calVolume.calVolume(self.frames)
		self.zcr = zeroCR.zeroCR(self.frames,frameSize)
		self.maxData = max(abs(self.y))
		#energy = calEnergy.calEnergy(maxData,frames)
		total_num = len(self.y)
		self.pitch, self.acf = calPitch.calPitch(self.maxData,self.frames,self.fs)
		self.speech_segment = epd.epd(self.volume,self.zcr,self.fs)
		
		self.decision = uvDecision.uvDecision(self.volume,self.zcr,self.acf)
		self.fftFrames = calFft.calFft(self.frames,self.fs)
		self.energyBelow250 = calEnergyBelow250.calEnergyBelow250(self.fftFrames,self.fs)
		
	
	def calFeatures(self):
		print 'calFeatures...'
		self.has_feature = False
		T = 500
		if self.maxData < T:
			self.segment_info = 0
		 	return

		self.features = []
		pitch = []
		for seg in self.speech_segment:
			curPitch = []
			beg = seg[0]
			end = seg[1]
			#print self.decision
			for i in range(beg,end):
				if self.decision[i] == 1:
					curPitch.append(self.pitch[i])
			pitch.append(curPitch)
		
		for i in range(len(self.speech_segment)):
			beg = self.speech_segment[i][0]
			end = self.speech_segment[i][1]
			if end-beg < 10:
				continue
			self.has_feature = True
			aveVolume = np.average(self.volume[beg:end])
			maxVolume = np.max(self.volume[beg:end])
			stdVolume = np.std(self.volume[beg:end])
			rangeVolume = maxVolume - np.min(self.volume[beg:end])
			if len(pitch[i]) == 0:
				avePitch = 0
				maxPitch = stdPitch = avePitch = rangePitch = 0
			else:
				avePitch = np.average(pitch[i])
				maxPitch = np.max(pitch[i])
				stdPitch = np.std(pitch[i])
				rangePitch = maxPitch = np.min(pitch[i])
			
			aveLowEnergy = np.average(self.energyBelow250[beg:end])
			stdLowEnergy = np.std(self.energyBelow250[beg:end])
			self.features.append([aveVolume,maxVolume,stdVolume,rangeVolume,avePitch,maxPitch,stdPitch,rangePitch,aveLowEnergy,stdLowEnergy])
		self.segment_info = len(self.features)
		print 'end'
	def callInfo(self):
		self.total_length = len(self.y)*1.0/self.fs
		voiced_frame = 0
		for i in self.speech_segment:
			voiced_frame = voiced_frame + i[1]-i[0]
		self.voiced_length = voiced_frame*1.0*(self.frameSize-self.overlap)/self.fs
		
		if self.has_feature==False:
			return
		if len(self.features)>1:
			feature_num = len(self.features[0])
			feature = [0 for i in range(feature_num)]
			for feat in self.features:
				for i in range(feature_num):
					feature[i] = feature[i] + feat[i]
			for i in range(feature_num):
				feature[i] = feature[i]/len(self.features)
			self.feature_info = feature
		else:
			self.feature_info = []

		self.feature_info = np.average(self.features,0)

	def report(self):
		
		report_line = OrderedDict({'File Name':self.filename,'Mood Result':self.mood, 'Speech Segment Num':len(self.speech_segment),'Total Length':self.total_length,'Speech Length':self.voiced_length})
		feature_key = ('aveVolume','maxVolume','stdVolume','rangeVolume','avePitch','maxPitch','stdPitch','rangePitch','aveLowEnergy','stdLowEnergy')
		#report_line = "%s:\n %s %f %f"%(self.filename,self.mood,self.total_length,self.voiced_length)
		if self.has_feature:
			for n,feature in enumerate(self.features):
				cur_feature = {}
				for i,v in enumerate(feature):
					cur_feature[feature_key[i]] = v
				report_line['Segment '+str(n)] = cur_feature  
		report_json = json.dumps(report_line)
		self.reportFs.write(report_json)
		self.reportFs.write('\n')
		