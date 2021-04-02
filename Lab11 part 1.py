from serial import Serial
import serial
from time import sleep
import matplotlib.pyplot as plt
import numpy as np

qi = input("Initial Position")
qi = float(qi)
qf = input("Final Position")
qf = float(qf)
tf = input("Final Time, 20 second maximum")
tf = float(tf)
resolution = input("Resolution in degrees")
resolution = float(resolution)

a0 = qi
a1 = 0
a2 = 3*(qf-qi)/(tf**2)
a3 = -2*(qf - qi)/(tf**3)
#a4 = -15*(qf - qi)/(tf**4)
#a5 = 6*(qf - qi)/(tf**5)

Ts = 0.01
Ns = tf/Ts
Ns = int(Ns)

q = np.zeros(Ns)
dq = np.zeros(Ns)
ddq = np.zeros(Ns)
time_sec = np.zeros(Ns)
data = np.zeros(Ns)
t = 0

for k in range(0,Ns):
    q[k] = a0 + a1*t + a2*t**2 + a3*t**3
    dq[k] = 2*a2*t + 3*a3*t**2
    ddq[k] = 2*a2 + 6*a3*t
    time_sec[k] = k*Ts
    t = t + Ts

for k in range(0, Ns):
    Temp = dq[k]/resolution
    if(Temp != 0.0):
        Temp = 1 / Temp 
    data[k] = Temp / 0.0001
    #print(data[k])
    
ser = serial.Serial("/dev/ttyUSB0", 9600)
ser.flush()
sleep(3)

for t in range(0, Ns):
    ser.write(str(data[t]).encode('utf-8'))
    ser.write(str("\n").encode('utf-8'))

plt.plot(time_sec,q,"r")
plt.plot(time_sec,dq,"b")
plt.plot(time_sec,ddq,"g")
plt.ylabel("q(t)")
plt.xlabel("Time")
plt.show()