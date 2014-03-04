import os
import sys
sys.path.append('/home/will/Documents/data/lib/libsvm-3.17/python')
from svmutil import *
from voice import Voice
import config
#root_dir = '/home/will/Documents/data/luyin'

def train(diretory = config.root_dir):
	'''Train all the files in diretory 'luyin'

	The diretory is made up of two subdiretories named 'normal' and 'abnormal'.
	
	As a result , the script will generate 3 files:
	(1)scale : used for scale data by the svm command 'svm-scale -s filename > scale'
	(2)dataset_scaled : the scaled dataset for training
	(3)model : the svm model file 
	'''
	files = os.listdir(config.normal)
	dataset = config.dataset
	dataset_scaled = config.dataset_scaled
	scale = config.scale

	#fs = open(dataset,'a')

	for f in files:
		f = config.normal + f
		voice = Voice()
		voice.analyze(f)
		voice.calFeatures()
		voice.learn(dataset,'+1')
	files = os.listdir(config.abnormal)
	
	for f in files:
		f = config.abnormal + f
		voice = Voice()
		voice.analyze(f)
		voice.calFeatures()
		voice.learn(dataset,'-1')

	os.system('svm-scale -s %s %s > %s'%(scale,dataset,dataset_scaled))
	y,x = svm_read_problem(dataset_scaled)
	m = svm_train(y,x)
	svm_save_model(config.model,m)

if __name__ == '__main__':
	train()