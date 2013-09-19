function M = triangulateJYB(P1, m1, P2, m2)
% TRIANGULATE computes the 3D point location using 2D camera views
% P1: camera matrix of the first camera.
% m1: pixel location (x1, y1) on the first view. Row vector.
% P2: camera matrix of the second camera
% m2: pixel location (x2, y2) on the second view. Row vector.
% M: the (x, y, z) coordinate of the reconstructed 3D point. Row vector.
% Camera one
C1 = inv(P1(1:3, 1:3)) * (-P1(:,4));
x0 = C1(1);
y0 = C1(2);
z0 = C1(3);
m1 = [m1'; 1];
M1 = pinv(P1) * m1;
x = M1(1)/M1(4);
y = M1(2)/M1(4);
z = M1(3)/M1(4);
a = x-x0;
b = y-y0;
c = z-z0;
% Camera Two
C2 = inv(P2(1:3, 1:3)) * (-P2(:,4));
x1 = C2(1);
y1 = C2(2);
z1 = C2(3);
m2 = [m2'; 1];
M2 = pinv(P2) * m2;
x = M2(1)/M2(4);
y = M2(2)/M2(4);
z = M2(3)/M2(4);
d = x-x1;
e = y-y1;
f = z-z1;
% Solve u and v
A = [a^2 + b^2 + c^2, -(a*d + e*b + f*c);...
-(a*d + e*b + f*c), d^2 + e^2 + f^2];
v = [ (x1-x0)*a + (y1-y0)*b + (z1-z0)*c;...
(x0-x1)*d + (y0-y1)*e + (z0-z1)*f];
r = inv(A) * v;
M = [x0+a*r(1) y0+b*r(1) z0+c*r(1)];