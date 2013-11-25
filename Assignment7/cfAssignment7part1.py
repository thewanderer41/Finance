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
			Sj = Sj*math.exp(random.gauss(u*dt, o*math.sqrt(dt)))
		p.append(pj)
	v = []
	for i in range(M):
		if K-p[i][-1] > 0:
			v.append(K-p[i][-1])
		else:
			v.append(0.0)
	index = range(N-1)
	index.reverse()
	pi_star = [K]
	for i in index:
		xj = []
		yj = []
		for j in range(M):
			xj.append( p[j][i] )
			yj.append( math.exp(-r*dt)*v[j] )
		ai = numpy.polyfit(xj, yj, 2)
		#rint i, ai
		if (((ai[1]+1)**2)-(4*ai[0]*(ai[2]-K))) < 0:
			_pi = 0.0
		else:
			_pi = ((-1*(ai[1]+1))-math.sqrt(((ai[1]+1)**2)-(4*ai[0]*(ai[2]-K))))/(2*ai[0])
		pi_star.append(_pi)
		for j in range(M):
			if p[j][i] < _pi:
				v[j] = K-p[j][i]
			else:
				v[j] = yj[j]
	price = 0
	pi_star.reverse()
	for i in range(L):
		S = [S0]
		for j in range(N-1):
			S.append(S[-1]*math.exp(random.gauss(u*dt, o*math.sqrt(dt))))
		index = range(N)
		index.reverse()
		pj = 0
		for j in index:
			if S[j] < pi_star[j]:
				pj = K-S[j]
			else:
				pj = math.exp(-r*dt)*pj
		price = price + (pj-price)/(i+1)
	end = (time.clock()-start)
	return price, end

def OPT(S0, K, T, r, o, N, M, L):
	start = time.clock()
	dt = float(T)/N
	u = r-(0.5*(o**2))
	Sj = [S0]*M
	S  = []
	for i in range(N):
		S.append(Sj)
		Sj = []
		for j in range(M):
			Sj.append(S[i][j]*math.exp(random.gauss(u*dt, o*math.sqrt(dt))))
	v = []
	Vh = {}
	for i in range(M):
		if K-S[N-1][i] > 0:
			Vh[S[N-2][i]] = math.exp(-r*dt)*(K-S[N-1][i])
		else:
			Vh[S[N-2][i]] = 0.0
	pi_star = [0.0]*N
	pi_star[N-1] = K
	index = range(N-1)
	index.reverse()
	for i in index:
		error = 0
		for j in range(M):
			if Vh[S[i][j]]-(K-S[i][j]) < 0:
				error = error - (Vh[S[i][j]]-(K-S[i][j]))
		sorted_values = sorted(S[i])
		error2 = error
		for Sj in sorted_values:
			error2 = error2 + (Vh[Sj]-(K-Sj))
			if error2 < error:
				error = error2
				pi_star[i] = Sj
		if i != 0:
			Vh_temp = {}
			for j in range(M):
				if S[i][j] <= pi_star[i]:
					Vh_temp[S[i-1][j]] = math.exp(-r*dt)*(K-S[i][j])
				else:
					Vh_temp[S[i-1][j]] = math.exp(-r*dt)*Vh[S[i][j]]
			Vh = Vh_temp
	price = 0
	for i in range(L):
		S = [S0]
		for j in range(N-1):
			S.append(S[-1]*math.exp(random.gauss(u*dt, o*math.sqrt(dt))))
		index = range(N)
		index.reverse()
		pj = 0
		for j in index:
			if S[j] < pi_star[j]:
				pj = K-S[j]
			else:
				pj = math.exp(-r*dt)*pj
		price = price + (pj-price)/(i+1)
	end = (time.clock()-start)
	return price, end

def OPT2(S0, K, T, r, o, N, M):
	start = time.clock()
	dt = float(T)/N
	u = r-(0.5*(o**2))
	Sj = [S0]*M
	S  = []
	for i in range(N):
		S.append(Sj)
		Sj = []
		for j in range(M):
			Sj.append(S[i][j]*math.exp(random.gauss(u*dt, o*math.sqrt(dt))))
	v = []
	Vh = {}
	for i in range(M):
		if K-S[N-1][i] > 0:
			Vh[S[N-2][i]] = math.exp(-r*dt)*(K-S[N-1][i])
		else:
			Vh[S[N-2][i]] = 0.0
	pi_star = [0.0]*N
	pi_star[N-1] = K
	index = range(N-1)
	index.reverse()
	for i in index:
		error = 0
		for j in range(M):
			if Vh[S[i][j]]-(K-S[i][j]) < 0:
				error = error - (Vh[S[i][j]]-(K-S[i][j]))
		sorted_values = sorted(S[i])
		error2 = error
		for Sj in sorted_values:
			error2 = error2 + (Vh[Sj]-(K-Sj))
			if error2 < error:
				error = error2
				pi_star[i] = Sj
		if i != 0:
			Vh_temp = {}
			for j in range(M):
				if S[i][j] <= pi_star[i]:
					Vh_temp[S[i-1][j]] = math.exp(-r*dt)*(K-S[i][j])
				else:
					Vh_temp[S[i-1][j]] = math.exp(-r*dt)*Vh[S[i][j]]
			Vh = Vh_temp
	price = 0
	pj = [0.0]*M
	index = range(N)
	index.reverse()
	for i in index:
		for j in range(M):
			if S[i][j] < pi_star[i]:
				pj[j] = K-S[i][j]
			else:
				pj[j] = math.exp(-r*dt)*pj[j]
	for j in range(M):
		price = price + (pj[j]-price)/(j+1)
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
print "LSM(N, M, L) = (50, 10000, 10000)"
price, end = LSM(S0, K, T, r, o, 50, 10000, 10000)
print "  price = "+str(price)
print "  time  = "+str(end)
print "LSM(N, M, L) = (100, 5000, 5000)"
price, end = LSM(S0, K, T, r, o, 100, 5000, 5000)
print "  price = "+str(price)
print "  time  = "+str(end)
print "LSM(N, M, L) = (50, 5000, 50000)"
price, end = LSM(S0, K, T, r, o, 50, 5000, 50000)
print "  price = "+str(price)
print "  time  = "+str(end)
print "OPT(N, M, L) = (50, 10000, 10000)"
price, end = OPT(S0, K, T, r, o, 50, 10000, 10000)
print "  price = "+str(price)
print "  time  = "+str(end)
print "OPT(N, M, L) = (100, 5000, 5000)"
price, end = OPT(S0, K, T, r, o, 100, 5000, 5000)
print "  price = "+str(price)
print "  time  = "+str(end)
print "OPT(N, M, L) = (50, 5000, 50000)"
price, end = OPT(S0, K, T, r, o, 50, 5000, 50000)
print "  price = "+str(price)
print "  time  = "+str(end)
print "OPT2 Average"
avg = 0.0
for i in range(1000):
	price, end = OPT2(S0, K, T, r, o, 50, 50)
	avg = avg+((price-avg)/(i+1))
print "  "+str(avg)
print "OPT Average"
avg = 0.0
for i in range(1000):
	price, end = OPT(S0, K, T, r, o, 50, 50, 50)
	avg = avg+((price-avg)/(i+1))
print "  "+str(avg)
