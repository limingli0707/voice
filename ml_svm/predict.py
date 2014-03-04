import os
import sys
sys.path.append('/home/will/Documents/data/lib/libsvm-3.17/python')
from svmutil import *
import config

#root_dir = '/home/will/Documents/data/luyin'

def predict(x):
	scale = config.scale
	model = config.model
	feature_scaled = config.root_dir + '/feature_scaled'
	tmp = config.root_dir + '/tmp'
	tmpFs = open(tmp,'w')
	line = ''
	for feature in x:
		line = line + "0"
		for i in range(len(feature)):
			line = line + ' ' + str(i+1) + ':' + str(feature[i])
		line = line + '\n'
	
	tmpFs.write(line)
	tmpFs.close()

	os.system('svm-scale -r %s %s > %s'%(scale,tmp,feature_scaled))
	
	try:
		y,x = svm_read_problem('%s'%feature_scaled)
		y = [0]*len(x)
		#print 'x',x
		#print type(x)
		#print 'y',y
		m = svm_load_model(model)
		p_labels, p_acc, p_vals = svm_predict(y, x, m)
	except Exception as e:
			print e
	os.system('rm -f %s'%feature_scaled)
	os.system('rm -f %s'%tmp)

	return p_labels


