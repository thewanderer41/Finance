import math
import random
import numpy
import scipy
import time

def B(S0, K, T, r, o, N):
	dt = float(T)/N
	u = r-(0.5*(o**2))
	lambda_plus = math.exp((u*dt)+(o*math.sqrt(dt)))
	lambda_minus = math.exp((u*dt)-(o*math.sqrt(dt)))
	p_ = (math.exp(r*dt)-lambda_minus)/(lambda_plus-lambda_minus)
	v = []

	for k in range(N+1):
		log_s_k = k*math.log(lambda_plus)+(N-k)*math.log(lambda_minus)+math.log(S0)
		v.append(max(K-math.exp(log_s_k), 0))

	x = range(N)
	x.reverse()
	for i in x:
		for k in range(i+1):
			v_hold = math.exp(-r*dt)*((p_*v[k+1])+((1-p_)*v[k]))
			log_s_i = k*math.log(lambda_plus)+(i-k)*math.log(lambda_minus)+math.log(S0)
			v_ex   = max(K-math.exp(log_s_i), 0)
			v[k] = max( v_hold, v_ex)
	return v[0]

def LSM(S0, K, T, r, o, N, M, L):
	start = time.clock()
	dt = float(T)/N
	u  = r-(0.5*(o**2))
	p  = []
	for i in range(M):
		pj = []
		Sj = S0
		for j in range(N):
			pj.append(Sj)
			Sj = Sj*math.exp(random.gauss(u*dt, o*dt))
		p.append(pj)
	v = []
	for i in range(M):
		if K-p[i][-1] > 0:
			v.append(K-p[i][-1])
		else:
			v.append(0.0)
	index = range(N-1)
	index.reverse()
	pi_star = []
	for i in index:
		xj = []
		yj = []
		for j in range(M):
			xj.append( p[j][i] )
			yj.append( math.exp(-r*dt)*v[j] )
		ai = numpy.polyfit(xj, yj, 2)
		#print ai
		_pi = ((-1*(ai[1]+1))+math.sqrt(((ai[1]+1)**2)-(4*ai[0]*(ai[2]-K))))/(2*ai[0])
		pi_star.append(_pi)
		for j in range(M):
			if p[j][i] < _pi:
				v[j] = K-p[j][i]
			else:
				v[j] = yj[j]
	pi_star.append(K)
	price = 0
	for i in range(L):
		S = S0
		pj = 0
		for j in range(N):
			if S < pi_star[j]:
				if K > S:
					pj = pj + (math.exp(-r*j*dt)*float(K-S))
			S = S*math.exp(random.gauss(u*dt, o*dt))
		price = price + (pj-price)/(i+1)
	end = (time.clock()-start)
	return price, end

S0 = 10
K  = 10
T  = 2
r  = 0.05
o  = 0.2
print "N = 100"
print B(S0, K, T, r, o, 100)
print "N = 1000"
print B(S0, K, T, r, o, 1000)
print "(N, M, L) = (50, 10000, 10000)"
price, end = LSM(S0, K, T, r, o, 50, 10000, 10000)
print "price = "+str(price)
print "time  = "+str(end)
print "(N, M, L) = (100, 5000, 5000)"
price, end = LSM(S0, K, T, r, o, 100, 5000, 5000)
print "price = "+str(price)
print "time  = "+str(end)
print "(N, M, L) = (50, 5000, 50000)"
price, end = LSM(S0, K, T, r, o, 50, 5000, 50000)
print "price = "+str(price)
print "time  = "+str(end)
