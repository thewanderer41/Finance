import numpy
import scipy
from scipy import optimize
import math

n = 100
p = 0.05
S = numpy.ones((n,1))
Corr = (1-p)*numpy.identity(n)+p*numpy.dot(numpy.ones((n,1)),numpy.ones((1,n)))
Sigma = Corr.copy()
u = numpy.random.normal(0.25, 1.0, (n,1))
U = {}
for i in range(n):
	U[u[i][0]] = numpy.random.normal(u[i][0],1,1)[0]

def fun(w):
	return numpy.dot(w.T,numpy.dot(Sigma,w))

def jac(w):
	return 2*numpy.dot(w.T, Sigma)

cons1 = {'type':'eq', 'fun':lambda w: numpy.dot(w.T,numpy.ones((n,1)))-1}
cons3 = {'type':'ineq', 'fun':lambda w: w}

for m in sorted(u):
	cons2 = {'type':'eq', 'fun':lambda w:numpy.dot(w.T, u)-m}
	constraints = (cons1, cons2, cons3)
	w0 = numpy.random.random((n,1))
	res = scipy.optimize.minimize(fun, w0, jac=jac, constraints=constraints, method='SLSQP', options={'disp':False})
	w = res['x'][numpy.newaxis]
	print w.shape
	print numpy.dot(w, numpy.dot(Sigma, w.T)), numpy.dot(w, [U[x[0]] for x in sorted(u)])
	#print res
	print ""

