'''My basic implementation of the perceptron algorithm, able to handle
classifying multiple classes in a run.  It must be given a dictionary with
all the data in it broken down into lists of lists for each class, where the
class is the key and the lists of data are the value.
'''
import random
import vector as v

def _perceptron(feature_vect, w, positive):
	r = v.dot(feature_vect, w)
	if positive and r<=0:
		return v.vec_add(w, feature_vect), False
	elif not positive and r>=0:
		return v.vec_sub(w, feature_vect), False
	else:
		return w, True

def _augment(data):
	#augment the data with an addional element set to 1 so that we get our 
	#constant out of the weight
	for c in data.keys():
		for datum in data[c]:
			datum.append(1)


def run_perceptron(data, dimensionality, cutoff=500000):
	'''runs the perceptron on the dataset.  data must be in a dictionary with
		a key for each class, and the list containing all the data for that 
		class as the value.  A weight will be returned to partition based on
		the number of classes presented.
	'''
	_augment(data)
	#make an initial weight vector, it must be 1 more than the dimensionality
	#of the data, since we extend the data by element.  I just map a lambda 
	#that doesn't care about the input to do this.
	z = lambda _: 0 
	w = _reset_w(dimensionality)
	
	final_weights = {}
	#run the data
	if len(data.keys())==2:
		positive = data.keys()[0]
		final_weights[positive]=_run(data, w, positive, cutoff)
	elif len(data.keys()) >2:
		for positive in data.keys():
			w = _reset_w(dimensionality)
			final_weights[positive] = _run(data, w, positive, cutoff)

	for key in final_weights.keys():
		print 'Class {0:s} will be positive with the dot product of '.format(key)
		print final_weights[key]
		print 
	return final_weights


def run_tests(data, weights):
	'''runs a test to see how many things are classified correctly, or 
		incorrectly in their class, as well as misclassified into a different
		class. 
	'''
	
	_augment(data)
	results = {}
	for data_key in data.keys():
		results[data_key] = {'correct':0, 'incorrect':0, 'misclassified':0}
		for datum in data[data_key]:
			for key in weights.keys():
				_, correct = _perceptron(datum, weights[key], key==data_key)

				if correct:
					#classified it correctly in its class
					results[data_key]['correct']+=1
				elif key != data_key and not correct:
					#classified as a being a member of a different class
					results[data_key]['misclassified']+=1	
				elif key == data_key and not correct:
					#not classified correctly in its class
					results[data_key]['incorrect']+=1
	print results		


def _reset_w(l):
	'''reset_w takes a length l and returns a weight vector zeroed out, with 
	augmentation of another 0
	'''
	f = lambda _: 0 
	return map(f, range(l+1))


def _run(data, w, positive, cutoff):
	''' a run method called for each of the different classes to get the
	different lines to get w.
	'''
	best = None
	while True and cutoff>0:
		missed = 0
		for c in data.keys():
			missed += len(data[c])
			for datum in data[c]:
				w, correct = _perceptron(datum, w, c==positive)
				if correct:
					missed -=1
				else:
					pass
		if not best:
			best = (missed, w)
		elif missed < best[0]:
			best = (missed, w)
		if missed == 0:
			return w
		cutoff -= 1
	#return the best score to date if we reach our cutoff of iterations
	print "[warning] cutoff reached before convergence"
	return best[1]


if __name__ == "__main__":
	#partition the data into two sets, one to train with and the
	#other to test the resultant weight vectors.
	import sys
	random.seed()
	training_data = {}
	test_data = {}
	for line in open(sys.argv[1], 'r'):
		data_s = line.strip().split(',')
		c = data_s.pop(0)
		data = map(float, data_s)
		if random.randint(1,3)==3:
			if c in test_data.keys():
				test_data[c].append(data)
			else:
				test_data[c] = [data]	
		else:
			if c in training_data.keys():
				training_data[c].append(data)
			else:
				training_data[c] = [data]
	dim = len(training_data[training_data.keys()[0]][0])
	w=run_perceptron(training_data, dim)
	run_tests(test_data, w)
