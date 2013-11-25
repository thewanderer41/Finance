from numpy import matrix
from numpy import linalg
from numpy import arange
import os
import math
import matplotlib.pyplot as plt

X = [100, 100, 100]
t_X = [1, 2, 3]
r = 0.05
t = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5]

B = []

for k in range(10):
	b = 0
	for j in range(3):
		b = b + (X[j]*(t_X[j]**k)*(math.e**(-r*t_X[j])))
	B.append([b])
#print B
a = []
for i in range(10):
	r_a = []
	for j in range(10):
		r_a.append((math.e**(-r*t[j]))*(t[j]**i))
	a.append(r_a)
#print a
m_B = matrix(B)
m_a = matrix(a)

#print m_B
#print ""
#print m_a

alpha = linalg.solve(m_a,m_B)
print alpha
alpha = alpha.reshape(-1,).tolist()[0]
print ""
print ""

error = []
d_t = 1.0/12
for d_r in arange(-0.02,0.021,0.001):
	A = 0
	for i in range(10):
		A = A+(alpha[i]*(math.e**(-(r+d_r)*t[i])))
	x = 0
	for j in range(3):
		x = x+(X[j]*(math.e**(-(r+d_r)*t_X[j])))
	error.append((math.e**((r+d_r)*d_t))*(A-x))

d_r_list = list(arange(-0.02,0.021,0.001))
#print "d_r_list"
#print d_r_list
#print "error"
#error = [x for x in error]
print error
plt.plot(d_r_list ,error, 'bo')
plt.xlabel("Delta r")
plt.ylabel("Error")
plt.title("Error vs Delta r, dt=1/12")
plt.savefig(os.path.expanduser("~")+"/Pictures/2c.png")
