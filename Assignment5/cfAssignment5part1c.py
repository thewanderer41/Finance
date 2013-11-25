import os
import sys
import math
import random
import matplotlib.pyplot as plot

def simulation(argv):
	r = float(argv[1])
	o = float(argv[2])
	u = r-(0.5*(o*o))#float(argv[0])
	S0 = float(argv[3])
	T = float(argv[4])
	Dt = float(argv[5])
	fn = argv[6]


	t = [0]
	S = [S0]
	_t = 0
	while _t <= T:
		x = random.gauss(u*Dt, o*math.sqrt(Dt))
		_S = S[-1]*math.exp(x)
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
