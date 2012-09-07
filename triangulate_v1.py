import numpy as np
from numpy import linalg as LA


#R matrix for camera 1 (west side)
R1 = np.array([[-74.2709, 637.41, -255.7461], [865.2027, 273.6518, -92.0415], [0.1602, 0.3172, -0.9347]])
#T matrix for camera 1
T1 = np.array([[1.3248e5], [4.1268e4], [505.0954]])
P1 = np.hstack((R1, T1))

#R matrix for camera 2 (east side)
R2 = np.array([[-20.0487, 179.5963, -666.7510], [751.5431, -397.57, -330.23], [-0.2329, -0.5675, -0.7898]])
#T matrix for camera 2
T2 = np.array([[3.7547e5], [3.3423e5], [907.6034]])
P2 = np.hstack((R2, T2))

#blimp position from camera 1
col_1 = 411
row_1 = 382
#m1 = np.array([
#blimp position from camera 2
col_2 = 531
row_2 = 178


#translated from matlab:

#Camera 1
invR1 = LA.inv(R1)
m1T1 = -1*T1
C1 = np.dot(invR1, m1T1)
x0 = C1[0]
y0 = C1[1]
z0 = C1[2]
m1 = np.array([[col_1], [row_1], [1]]);
M1 = np.dot(LA.pinv(P1), m1)
x = M1[0]/M1[3]
y = M1[1]/M1[3]
z = M1[2]/M1[3]
a = x-x0
b = y-y0
c = z-z0

#Camera 2
invR2 = LA.inv(R2)
m1T2 = -1*T2
C2 = np.dot(invR2, m1T2)
x1 = C2[0]
y1 = C2[1]
z1 = C2[2]
m2 = np.array([[col_2], [row_2], [1]]);
M2 = np.dot(LA.pinv(P2), m2)
x = M2[0]/M2[3]
y = M2[1]/M2[3]
z = M2[2]/M2[3]
d = x-x1
e = y-y1
f = z-z1

A11 = (a*a + b*b + c*c)
A12 = -1*(a*d + e*b + f*c)
A21 = -1*(a*d + e*b + f*c)
A22 = d*d + e*e + f*f
A = np.array([[A11, A12], [A21, A22]])
A = np.squeeze(A) #get rid of 3rd dimension
v = np.array([[(x1-x0)*a + (y1-y0)*b + (z1-z0)*c], [(x0-x1)*d + (y0-y1)*e + (z0-z1)*f]])
v = np.squeeze(v) #get rid of 3rd dimension
invA = LA.inv(A)
r = np.dot(invA,v)
x_coord = x0+a*r[0]
y_coord = y0+b*r[0]
z_coord = z0+c*r[0]
