import math
import random
import scipy.stats as stats

n  = 1000
S0 = 1.0
u  = 0.07
r  = 0.03
o  = 0.2
T  = 2
K  = 1
uSa = 0.0
dt = 0.0001
S_prices = []

for i in range(n):
	S = S0
	Ka = S0
	for j in range(0,T*10000):
		S =   S*math.exp(random.gauss((r-0.5*(o**2))*dt, o*math.sqrt(dt)))
		Ka = Ka+S
	Ka = Ka/(T/dt)
	if Ka < S:
		uSa = uSa + (S-Ka)*math.exp(-r*T)
		S_prices.append((S-Ka)*math.exp(-r*T))
	else:
		S_prices.append(0.0)
	if i%100 == 0:
		print i

print "dt = 0.0001 uSa = "+str(uSa/n)
print "mean = "+str(stats.tmean(S_prices))
print "error  = "+str(math.sqrt(stats.tvar(S_prices))/math.sqrt(float(n)))
