import sys
import os
import math
import random

def main(argv):
	spread = float(argv[0])

	#ibm data
	file_name = "ibm.dat"
	dat_file = open(file_name)
	it0, iv0 = map(float, dat_file.readline().split())
	it, iv_prev = map(float, dat_file.readline().split())
	iu = (iv0+iv_prev)/2

	#Adjust for risk free
	bond_file = open("bond.dat")
	bt0, bv0 = map(float, bond_file.readline().split())
	bt, bv_prev = map(float, bond_file.readline().split())
	bu = (bv0+bv_prev)/2

	b = [math.log(bv_prev/bv0)-math.log(bv_prev/bv0)]
	s = [math.log(iv_prev/iv0)-math.log(bv_prev/bv0)]

	tau = 5/(60*24*250.0)
	i = 2
	state = 0

	for line in dat_file:
		it, iv = map(float, line.split())
		bt, bv = map(float, bond_file.readline().split())

		bu = (i*bu+bv)/(i+1)
		iu = (i*iu+iv)/(i+1)

		b.append(math.log(bv/bv_prev)-math.log(bv/bv_prev))
		s.append(math.log(iv/iv_prev)-math.log(bv/bv_prev))

		bv_prev = bv
		iv_prev = iv

	u = 0
	Sharpe = 0
	Sterling = 0
	for j in range(1000):
		if j%100 == 0:
			print j

		u_current = 0
		var_prev = 0
		MDD = 0
		r_max = 0
		u_prev = 0
		state = 0
		for i in range(len(s)):
			choice = random.randint(0,1)
			if   choice == 0 and state == 0:
				r_current = b[i]
			elif choice == 0 and state == 1:
				r_current = b[i] - spread*bu
			elif choice == 1 and state == 0:
				r_current = s[i] - spread*iu
			else:
				r_current = s[i]
			u_current = (i*u_prev+r_current)/(i+1)
			var_current = (i*var_prev+(r_current-u_prev)*(r_current-u_current))/(i+1)
			DD_current = r_max - r_current
			if MDD < DD_current:
				MDD = DD_current
			if r_max < r_current:
				r_max = r_current
			u_prev = u_current
			var_prev = var_current
			state = choice

		u = u+u_current/tau
		#Adjust for risk free
		if var_current == 0:
			Sharpe = Sharpe + 0
		else:
			Sharpe = Sharpe + u_current/math.sqrt(var_current*tau)
		if MDD == 0:
			Sterling = Sterling + 0
		else:
			Sterling = Sterling + u_current/(tau*MDD)

	print "Mean: "+str(u/1000.0)
	print "Sharpe: "+str(Sharpe/1000.0)
	print "Sterling: "+str(Sterling/1000.0)

if __name__ == "__main__":
	main(sys.argv[1:])
