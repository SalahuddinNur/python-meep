import matplotlib.pyplot as plt
import numpy
import numpy as np
import csv
import sys

data0 = (sys.argv[1])
data1 = (sys.argv[2])
My_ref = np.genfromtxt(data0, delimiter=",")
My_res = np.genfromtxt(data1, delimiter=",")
Ref = My_ref[:,[0,1]]
Res = My_res[:,[0,1]]
X = 100/My_ref[:,1]
Y = My_res[:,2]/My_ref[:,2]
Y1 = -My_res[:,3]/My_ref[:,2]
#print(X)
plt.plot(X,Y)
#plt.plot(X,Y1)
plt.xlabel("normalized frequency")
plt.ylabel("Transmittance")
plt.xlim(500, 1000)
plt.ylim(0,1.2);
#plt.show()
plt.savefig(sys.argv[1] + '_' + sys.argv[2] + '.png')
#Image.open(sys.argv[1] + '_' + sys.argv[2] + '.png').save(sys.argv[1] + '_' + sys.argv[2] + '.jpg','JPEG')
