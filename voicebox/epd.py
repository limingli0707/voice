def epd(volume,zcr,fs,minSilence=0.3,minLen=10,frameSize=128):
	'''End-Point_Detection by volume and zcr

	Return an index labeling the end point'''
	speech_segment = []
	num = len(volume)
	status = 0
	count = 0
	silence = 0
	minSilence = minSilence*fs/frameSize
	#minLen = 15
	#amp1 = max(volume)/8
	#amp2 = max(volume)/12
	amp1 = 80000
	amp2 = 150000
	zcr1 = 10
	zcr2 = 0.15 * frameSize
	#tHoldLow = min(max(self.absVolume)/10,3*self.maxData)
	#tHoldHigh = min(max(self.absVolume)/6,6*self.maxData)


	print 'zcr',zcr2,'silence',minSilence
	last = -1
	for i in range(num):
		if status==0 or status==1:
			if volume[i] > amp2:
				beg = i - count + 1
				silence = 0
				status = 2
				count = count + 1
			elif (volume[i]>amp1 or zcr[i] > zcr2):
				status = 1
				count = count + 1
			else:
				status = 0
				count = 0
		else:
			if ((volume[i]>amp1) or (zcr[i]>zcr2)):
				count = count + 1
				if i - last > 3:
					silence = 0
			else:
				last = i
				#print 'bumanzu in %d %d %d,silence %d'%(i,volume[i],zcr[i],silence)
				silence = silence + 1
				if silence < minSilence:
					count = count + 1
				elif count < minLen:
					status = 0
					silence = 0
					count = 0
					beg = -1
				else:
					status = 0
					#print 'ending in %d %d %d %d'%(i,volume[i],zcr[i],silence)
					speech_segment.append((beg,i-silence))
					count = 0
					silence = 0
					beg = -1

	if status == 2:
		speech_segment.append((beg,num))
	return speech_segment