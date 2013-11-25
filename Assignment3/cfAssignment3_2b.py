import numpy
import sys
from collections import deque

alpha = float(sys.argv[1])
beta  = float(sys.argv[2])

def p(x):
	return 100 - alpha*x

def f(x):
	return beta * x

def g(x):
	return beta * x

C_star = numpy.zeros((11,10))
l_star = numpy.zeros((11,10))

for i in range(11):
	C_star[i][9] = i*(p(10)-g(i))
	l_star[i][9] = i

for i in range(8,-1,-1):
	for k in range(11):
		for l in range(k+1):
			C_ = l*p(i+1)-l*g(l)-(k-l)*f(l)+C_star[k-l][i+1]
			if C_ > C_star[k][i]:
				C_star[k][i] = C_
				l_star[k][i] = l

print "C*:"
print C_star
print "\nl*:"
print l_star

K = 10
k = deque()
C = 0
q = 0

for i in range(10):
	k.append(l_star[K][i])
	C = C + C_star[l_star[K][i]][i] - l_star[K][i]*q
	q = q + f(l_star[K][i])
	K = K-l_star[K][i]

print k
print C
