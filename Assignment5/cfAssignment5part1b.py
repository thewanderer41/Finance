import os
import sys
import math
import random
import matplotlib.pyplot as plot

def simulation(argv):
	u = float(argv[0])
	r = float(argv[1])
	o = float(argv[2])
	S0 = float(argv[3])
	T = float(argv[4])
	Dt = float(argv[5])
	fn = argv[6]
	print u, r, o, S0, T, Dt
	dt = 0.000001
	p  = 2.0/3.0
	l_p = math.exp((u*dt)+(o*math.sqrt(dt)*(p/(1-p))))
	l_m = math.exp((u*dt)-(o*math.sqrt(dt)*(p/(1-p))))
	p_ = (math.exp(r*dt)-l_m)/(l_p-l_m)

	t = [0]
	S = [S0]
	_t = 0
	while _t <= T:
		x = random.random()
		if x < p_:
			_S = l_p*S[-1]
		else:
			_S = l_m*S[-1]
		_t = _t+Dt
		t.append(_t)
		S.append(_S)
	plot.plot(t, S, 'b-')
	plot.xlabel("t")
	plot.ylabel("S")
	plot.title("Stock price at dt="+str(Dt))
	plot.savefig(os.path.expanduser("~")+"/Pictures/cfa5/"+fn)
	plot.hold(False)

if __name__ == "__main__":
	simulation(sys.argv[1:])
