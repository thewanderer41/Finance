import math
import random
import scipy
import numpy

def MAX1(S0, K, T, r, o, N, M):
	dt = float(T)/N
	u = r-(0.5*(o**2))
	price = 0
	for j in range(M):
		pj = max(float(K)-S0,0.0)
		S = S0
		S_min = S0
		for i in range(N):
			if S < S_min:
				S_min = S
				if S_min < K:
					pj = math.exp(-r*i*dt)*(K-S_min)
			S = S*math.exp(random.gauss(u*dt, o*math.sqrt(dt)))
		price = price + (pj - price)/(j+1)
	return price

def MAX2(S0, K, T, r, o, N, M):
	dt = float(T)/N
	u = r-(0.5*(o**2))
	price = 0
	for j in range(M):
		pj = 0.0
		S = S0
		for i in range(N):
			if S < K:
				pj_temp = math.exp(-r*i*dt)*(K-S)
				if pj < pj_temp:
					pj = pj_temp
			S = S*math.exp(random.gauss(u*dt, o*math.sqrt(dt)))
		price = price + (pj - price)/(j+1)
	return price

S0 = 10
K  = 10
T  = 2
r  = 0.05
o  = 0.2

print "price MAX1"
print MAX1(S0, K, T, r, o, 50, 50000)
print "price MAX2"
print MAX2(S0, K, T, r, o, 50, 50000)
