"""Module for doing some basic vector math.
"""

__author__ = 'Scott Powers'

def dot(v1, v2):
	''' dot accepts to vectors in the form of iterables and returns the
		dot product of the vectors
	'''
	if len(v1) == len(v2):
		f = lambda a,b: a*b
		g = lambda a,b: a+b
		return reduce(g, map(f, v1, v2))
	else:
		#there should be a real sum for this but I don't need it right now
		return None

def vec_add(v1, v2):
	if len(v1) == len(v2):
		f = lambda a,b: a+b
		return map(f, v1, v2)

def vec_sub(v1, v2):
	if len(v1) == len(v2):
		f = lambda a,b: a-b
		return map(f, v1, v2)
