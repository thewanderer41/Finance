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
uSh = 0.0
uSa = 0.0
uSg = 0.0
dt = 0.1
uS2h = 0.0
uS2a = 0.0
uS2g = 0.0
dt2 = 0.01
uS3h = 0.0
uS3a = 0.0
uS3g = 0.0
dt3 = 0.0001

for i in range(n):
	S = S0
	Kh = 1/S0
	Ka = S0
	Kg = S0
	for j in range(0,T*10):
		S =   S*math.exp(random.gauss((r-0.5*(o**2))*dt, o*math.sqrt(dt)))
		Kh = Kh+1/S
		Ka = Ka+S
		Kg = Kg*S
	Kh = (T/dt)/Kh
	Ka = Ka/(T/dt)
	Kg = math.pow(Kg, 1/T/dt)
	if Kh < S:
		uSh = uSh + (S-Kh)*math.exp(-r*T)
	if Ka < S:
		uSa = uSa + (S-Ka)*math.exp(-r*T)
	if Kg < S:
		uSg = uSg + (S-Kg)*math.exp(-r*T)

	S2 = S0
	Kh = 1/S0
	Ka = S0
	Kg = S0
	for j in range(0,T*100):
		S2 = S2*math.exp(random.gauss((r-0.5*(o**2))*dt2, o*math.sqrt(dt2)))
		Kh = Kh+1/S
		Ka = Ka+S2
		Kg = Kg*S
	Kh = (T/dt2)/Kh
	Ka = Ka/(T/dt2)
	Kg = math.pow(Kg, 1/T/dt)
	if Kh < S2:
		uS2h = uS2h + (S2-Kh)*math.exp(-r*T)
	if Ka < S2:
		uS2a = uS2a + (S2-Ka)*math.exp(-r*T)
	if Kg < S2:
		uS2g = uS2g + (S2-Kg)*math.exp(-r*T)

	S3 = S0
	Kh = 1/S0
	Ka = S0
	Kg = S0
	for j in range(0,T*10000):
		S3 = S3*math.exp(random.gauss((r-0.5*(o**2))*dt3, o*math.sqrt(dt3)))
		Kh = Kh+1/S3
		Ka = Ka+S3
		Kg = Kg*S3
	Kh = (T/dt3)/Kh
	Ka = Ka/(T/dt3)
	Kg = math.pow(Kg, 1/T/dt)
	if Kh < S3:
		uS3h = uS3h + (S3-Kh)*math.exp(-r*T)
	if Ka < S3:
		uS3a = uS3a + (S3-Ka)*math.exp(-r*T)
	if Kg < S3:
		uS3g = uS3g + (S3-Kg)*math.exp(-r*T)

print "dt = 0.1 uSh = "+str(uSh/n)
print "dt = 0.1 uSa = "+str(uSa/n)
print "dt = 0.1 uSg = "+str(uSg/n)
print "dt = 0.01 uSh = "+str(uS2h/n)
print "dt = 0.01 uSa = "+str(uS2a/n)
print "dt = 0.01 uSg = "+str(uS2g/n)
print "dt = 0.0001 uSh = "+str(uS3h/n)
print "dt = 0.0001 uSa = "+str(uS3a/n)
print "dt = 0.0001 uSg = "+str(uS3g/n)
