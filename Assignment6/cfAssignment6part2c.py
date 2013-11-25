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
Asian_Price = 0.0
European_Price = 0.0
dt = 0.0001
asian_prices = []
ro2 = 0
run = False

I = 0.0
G = 0.0

CovPrev = 0.0
aCovPrev = 0.0
eCovPrev = 0.0
aVarPrev = 0.0
eVarPrev = 0.0

k = 0.0

for i in range(n):
	S = S0
	S2 = S0
	Ka = S0

	for j in range(0,T*10000):
		S =   S*math.exp(random.gauss((r-0.5*(o**2))*dt, o*math.sqrt(dt)))
		Ka = Ka+S
	Ka = Ka/(T/dt)
	if Ka < S:
		_Asian_Price = (S-Ka)*math.exp(-r*T)
	else:
		_Asian_Price = 0.0
	if S0 < S:
		_Euro_Price = (S-S0)*math.exp(-r*T)
	else:
		_Euro_Price = 0.0

	if not run:
		k = float(i+1)
		aCovCurrent = aCovPrev + (_Asian_Price-aCovPrev)/k
		eCovCurrent = eCovPrev + (_Euro_Price-eCovPrev)/k
		CovCurrent  = (CovPrev*(k-1)+(k-1)*(_Asian_Price-aCovPrev)*(_Euro_Price-eCovPrev)/(k))/(k)
		aVarCurrent = (((k-1)*aVarPrev)+((_Asian_Price-aCovPrev)*(_Asian_Price-aCovCurrent)))/(k)
		eVarCurrent = (((k-1)*eVarPrev)+((_Euro_Price -eCovPrev)*(_Euro_Price -eCovCurrent)))/(k)
		CovPrev = CovCurrent
		aCovPrev = aCovCurrent
		eCovPrev = eCovCurrent
		aVarPrev = aVarCurrent
		eVarPrev = eVarCurrent

		if aVarPrev==0 or eVarPrev==0:
			ro2 = 0
		else:
			ro2 = (CovPrev**2)/(aVarPrev*eVarPrev)
		if i > math.sqrt(float(n)/(1-ro2)):
			print "Stopped Pilot"
			run = True
	else:
		European_Price = European_Price + (_Euro_Price-European_Price)/(float(i)+1.0-k)
		Asian_Price = Asian_Price + (_Asian_Price-Asian_Price)/(float(i)+1.0-k)
		asian_prices.append(Asian_Price)

	if i%100 == 0:
		print i

alpha = -CovPrev/eVarPrev

d1 = (r+(0.5*(o**2)))*math.sqrt(T)/o
d2 = (r-(0.5*(o**2)))*math.sqrt(T)/o
G = S0*stats.norm.cdf(d1)-S*math.exp(-r*T)*stats.norm.cdf(d2)

print "dt = 0.0001 uSa = "+str(Asian_Price)
print "mean = "+str(Asian_Price + (alpha*(European_Price-G)))
print "error  = "+str(((stats.tvar(asian_prices)/(n-k))*((1/k)+1-ro2)))
