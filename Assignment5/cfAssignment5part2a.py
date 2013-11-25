import math
import random
from scipy.stats import norm

n  = 1000
S0 = 1.0
u  = 0.07
r  = 0.03
o  = 0.2
T  = 2
K  = 1
uS = 0.0
dt = 0.1
uS2 = 0.0
dt2 = 0.01
uS3 = 0.0
dt3 = 0.0001

for i in range(n):
	S = S0
	for j in range(0,T*10):
		S =   S*math.exp(random.gauss((r-0.5*(o**2))*dt, o*math.sqrt(dt)))
	S2 = S0
	for j in range(0,T*100):
		S2 = S2*math.exp(random.gauss((r-0.5*(o**2))*dt2, o*math.sqrt(dt2)))
	S3 = S0
	for j in range(0,T*10000):
		S3 = S3*math.exp(random.gauss((r-0.5*(o**2))*dt3, o*math.sqrt(dt3)))

	if S-K > 0:
		uS = uS+(S-K)*math.exp(-r*T)
	if S2-K > 0:
		uS2 = uS2+(S2-K)*math.exp(-r*T)
	if S3-K > 0:
		uS3 = uS3+(S3-K)*math.exp(-r*T)
	
print "dt = 0.1 uS = "+str(uS/n)
print "dt = 0.01 uS = "+str(uS2/n)
print "dt = 0.0001 uS = "+str(uS3/n)

d1 = (math.log(S0/K)+((r+(0.5*(o**2)))*T))/(o*math.sqrt(T))
d2 = (math.log(S0/K)+((r-(0.5*(o**2)))*T))/(o*math.sqrt(T))
print "S = "+str(S0*norm.cdf(d1)-K*math.exp(-r*T)*norm.cdf(d2))
