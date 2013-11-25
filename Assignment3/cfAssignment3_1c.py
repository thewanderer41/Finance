import sys
import os
import math
import random
from collections import deque
import matplotlib.pyplot as plt

def main(argv):
	spread = 0.02
	t = []

	#Adjust for risk free
	bond_file = open(argv[1])
	bt0, bv0 = map(float, bond_file.readline().split())
	bt, bv_prev = map(float, bond_file.readline().split())
	bu = (bv0+bv_prev)/2

	#ibm data
	dat_file = open(argv[0])
	it0, iv0 = map(float, dat_file.readline().split())
	it, iv_prev = map(float, dat_file.readline().split())
	iu = (iv0+iv_prev)/2

	if "bond.dat" in argv:
		b = [math.log(bv_prev/bv0)-math.log(bv_prev/bv0)]
		s = [math.log(iv_prev/iv0)-math.log(bv_prev/bv0)]
	else:
		b = [math.log(bv_prev/bv0)]
		s = [math.log(iv_prev/iv0)]
	tau = 5/(60*24*250.0)
	i = 2
	t.append(float(bt0))
	t.append(float(bt))

	print "Initialized"

	for line in dat_file:
		it, iv = map(float, line.split())
		bt, bv = map(float, bond_file.readline().split())

		t.append(float(bt))

		bu = (i*bu+bv)/(i+1)
		iu = (i*iu+iv)/(i+1)

		if "bond.dat" in argv:
			b.append(math.log(bv/bv_prev)-math.log(bv/bv_prev))
			s.append(math.log(iv/iv_prev)-math.log(bv/bv_prev))
		else:
			b.append(math.log(bv/bv_prev))
			s.append(math.log(iv/iv_prev))
		bv_prev = bv
		iv_prev = iv

	c = deque()
	r = deque()

	cr0_prev = 0.0
	fee0 = spread*bu
	cr1_prev = 0.0
	fee1 = spread*iu

	state = 0

	print "Mean calculated"

	for i in range(len(s)):
		if cr0_prev + b[i] > cr1_prev + b[i] - fee0:
			cr0_current = (0, cr0_prev + b[i])
		else:
			cr0_current = (1, cr1_prev + b[i] - fee0)
		if cr0_prev + s[i] - fee1 > cr1_prev + s[i]:
			cr1_current = (0, cr0_prev + s[i] - fee1)
		else:
			cr1_current = (1, cr1_prev + s[i])
		c.appendleft((cr0_current, cr1_current))
		
		if cr0_current[1] > cr1_current[1]:
			state = 0
		else:
			state = 1

		cr0_prev = cr0_current[1]
		cr1_prev = cr1_current[1]

	print "Optimized route calculated"

	for cumulative_return in c:
		r.appendleft(cumulative_return[state][1])
		state = cumulative_return[state][0]

	#i, r = optimal_trade(0, 0.0, 0.0, spread*bu, spread*iu, b, s)
	#r.reverse()

	print "Reversed"

	u_current = 0
	var_prev = 0
	MDD = 0
	r_max = 0
	u_prev = 0
	i = 0
	cr_array = [0.0]
	#plt.hold(True)
	for r_current in r:
		#plt.plot(t[i], r_current, 'bo')
		cr_array.append(i*u_prev+r_current)
		u_current = (i*u_prev+r_current)/(i+1)
		var_current = (i*var_prev+(r_current-u_prev)*(r_current-u_current))/(i+1)
		DD_current = r_max - r_current
		if MDD < DD_current:
			MDD = DD_current
		if r_max < r_current:
			r_max = r_current
		u_prev = u_current
		var_prev = var_current
		i = i+1

	print "Stats calculated\nPlotted"

	plt.plot(t, cr_array, 'bo')
	plt.xlabel("T")
	plt.ylabel("Cumulative Return")
	plt.title(argv[1]+" versus "+argv[0])
	plt.savefig(os.path.expanduser("~")+"/Pictures/"+argv[1].split('.')[0]+argv[0].split('.')[0]+".png")
	#plt.hold(False)

	print "Saved"

	u = u_current/tau
	#Adjust for risk free
	if var_current == 0:
		Sharpe = 0
	else:
		Sharpe = u_current/math.sqrt(var_current*tau)
	if MDD == 0:
		Sterling = 0
	else:
		Sterling = u_current/(tau*MDD)

	print "Mean: "+str(u)
	print "Sharpe: "+str(Sharpe)
	print "Sterling: "+str(Sterling)

if __name__ == "__main__":
	main(sys.argv[1:])
