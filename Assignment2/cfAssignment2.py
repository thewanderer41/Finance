import os
import math
import matplotlib.pyplot as plt

dataFile = open(os.path.expanduser("~")+"/Downloads/ibm.dat")
lamb_da = [1.0/12, 1.0/96, 1.0/1920]
x = []
y = []
MV12 = []
MV96 = []
MV1920 = []

for line in dataFile:
	t, quote = line.split()
	t = float(t)
	S = float(quote)
	x.append(t)
	y.append(S)
	if len(x) == 1:
		MV12.append((1-(math.e**(-lamb_da[0])))*S)
		MV96.append((1-(math.e**(-lamb_da[1])))*S)
		MV1920.append((1-(math.e**(-lamb_da[2])))*S)
	else:
		MV12.append(math.e**(-lamb_da[0])*MV12[-1]+(1-math.e**(-lamb_da[0]))*S)
		MV96.append(math.e**(-lamb_da[1])*MV96[-1]+(1-math.e**(-lamb_da[1]))*S)
		MV1920.append(math.e**(-lamb_da[2])*MV1920[-1]+(1-math.e**(-lamb_da[2]))*S)

plt.hold(True)
plt.plot(x, y)
plt.plot(x, MV12, 'b')
plt.plot(x, MV96, 'r')
plt.plot(x, MV1920, 'g')
plt.xlabel("T")
plt.ylabel("MV(T)")
plt.title("T vs MV(T)")
plt.hold(False)

plt.savefig(os.path.expanduser("~")+"/Pictures/2c.png")
