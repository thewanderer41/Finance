import math
import random
import scipy.stats as stats
#import numpy.random.RandomState as rand

n  = 1000
S0 = 1.0
u  = 0.07
r  = 0.03
o  = 0.2
T  = 2
K  = 1
Asian_Price = 0.0
dt = 0.0001
asian_prices = []

for i in range(n):
	S = S0
	S_a = S0
	aver = S0
	Ka = S0

	for j in range(0,T*10000):
		mean = (r-0.5*(o**2))
		rand = random.gauss(mean*dt, o*math.sqrt(dt))
		S =    S*math.exp(rand)
		S_a =  S_a*math.exp((2*mean*dt)-rand)
		aver = (S+S_a)/2.0
		Ka = Ka+aver
	Ka = Ka/(T/dt)
	if Ka < aver:
		Asian_Price = Asian_Price + (aver-Ka)*math.exp(-r*T)
		asian_prices.append((aver-Ka)*math.exp(-r*T))
	else:
		asian_prices.append(0.0)
	if i%100 == 0:
		print i

print "dt = 0.0001 uSa = "+str(Asian_Price/n)
print "mean = "+str(stats.tmean(asian_prices))
print "error = "+str(math.sqrt(stats.tvar(asian_prices))/math.sqrt(float(n)))
