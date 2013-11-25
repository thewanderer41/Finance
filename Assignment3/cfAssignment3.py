import sys
import os
import math

print __name__
def main(argv):
	file_name = argv[0]
	dat_file = open(file_name)
	t0, v0 = map(float, dat_file.readline().split())
	t, v_prev = map(float, dat_file.readline().split())

	#Adjust for risk free
	#bond_file = open("bond.dat")
	#bt0, bv0 = map(float, bond_file.readline().split())
	#bt, bv_prev = map(float, bond_file.readline().split())
	r_max = math.log(v_prev/v0)#-math.log(bv_prev/bv0)
	u_prev = math.log(v_prev/v0)#-math.log(bv_prev/bv0)

	var_prev = 0
	MDD = 0
	tau = 5/(60*24*250.0)
	i = 2
	for line in dat_file:
		t, v = map(float, line.split())

		#Adjust for risk free
		#bt, bv = map(float, bond_file.readline().split())

		r_current = math.log(v/v_prev)#-math.log(bv/bv_prev)
		u_current = ((i-1)*u_prev+r_current)/i
		var_current = ((i-1)*var_prev+(r_current-u_prev)*(r_current-u_current))/i
		DD_current = r_max-r_current
		if MDD < DD_current:
			MDD = DD_current
		if r_max < r_current:
			r_max = r_current
		u_prev = u_current
		var_prev = var_current
		v_prev = v
		#bv_prev = bv
		i = i+1

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
