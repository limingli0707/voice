def add_to_learn(filename, features, labels):
	no = len(features)
	if no>1:
		raise Exception('only one speech segment is supported')
	fs = open(filename,'a')
	line = ''
	for i,f in enumerate(features[0]):
		line = line+' %d:%s'%(i+1,f)
	line = '%s '%labels + line + '\n'
	#print 'writing %s'%line
	fs.write(line)

