import numpy
import math
import matplotlib.pyplot as plt
import os

dataFile = open(os.path.expanduser("~")+"/Downloads/zero_coupon.dat")

data_values = []

for i in dataFile:
	values = i.split()
	line_values = map(float, values)
	data_values.append(line_values)

B = []
T = []
plt.hold(True)
for i in data_values:
	plt.plot(i[3], i[4], 'bo')
plt.xlabel("T")
plt.ylabel("B(0,T)")
plt.title("B(0,T) versus T")
plt.savefig(os.path.expanduser("~")+"/Pictures/1bi.png")
plt.hold(False)

plt.cla()
plt.hold(True)
for i in data_values:
	r = math.log(i[4]/100)/-i[3]
	plt.plot(i[3], r, 'ko')
plt.xlabel("T")
plt.ylabel("r")
plt.title("r versus T")
plt.savefig(os.path.expanduser("~")+"/Pictures/1bii.png")
plt.hold(False)

t1 = 0
nt1 = 0
t2 = 0
nt2 = 0
for i in data_values:
	if i[:3] == [2, 15, 2006]:
		t1 = t1+i[4]
		nt1 = nt1+1
	elif i[:3] == [8, 15, 2009]:
		t2 = t2+i[4]
		nt2 = nt2+1

ut1 = t1/nt1
ut2 = t2/nt2
print ut1
print ut2
print (ut1/-100)+(ut2/50)
