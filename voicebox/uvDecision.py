import numpy as np
def uvDecision(energy, zcr, acf):
	'''Voiced, unvoiced decision 

	Return a list indicating voiced index'''

	energyT = 100000
	zcrT = 50
	acfT = max(acf)/7

	frameLen = len(energy)
	decision = np.zeros(frameLen)
	status = 0
	
	for i in range(frameLen):
		if energy[i] > energyT and zcr[i]<zcrT:
			decision[i] = 1
		elif zcr[i]<zcrT and acf[i]>acfT:
			decision[i] = 1
	return decision
