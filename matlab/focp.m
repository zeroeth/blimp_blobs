% part of blimp 3D tracking
% focp.m (find optimized camera parameters)
clear;clc;home

pd1 = 'C:\Users\yuming\Documents\GitHub\blimp_blobs\';
filename = [pd1,'tracking_optimization.xlsx'];
num = xlsread(filename,'A2:H8');
chc = [1 4:5];
rxyz = num(chc,6:8);
c1xy = num(chc,1:2);
c2xy = num(chc,3:4);

%%
% Cx1 = ccp(1);
% Cy1 = ccp(2); %centered in y dim
% Cz1 = ccp(3);
% Cx2 = ccp(4);
% Cy2 = ccp(5);
% Cz2 = ccp(6);
% thx1 = ccp(7);
% thy1 = ccp(8);
% thz1 = ccp(9);
% thx2 = ccp(10);
% thy2 = ccp(11); 
% thz2 = ccp(12);

ax = 42610;
%10947 mm in y direction
ay = 8660;
%15240 mm in z direction
az = 15240;

%Camera sensor and lens
%Focal length = 4.2 mm
fx = 4.2;
fy = fx;
%Sensor = 4.54 mm X 3.42 mm
sx = 4.54/2;
sy = 3.42/2;
%Image size = 1280 X 720 pixels
ix = 1280;
iy = 720;

%These are in the world's reference frame, to actually get camera matrices, these must be inverted.
%--Translation--
%Camera 1 (west side)
Cx1 = 0;
Cy1 = ay/2; %centered in y dim
Cz1 = az;
C1 = [Cx1; Cy1; Cz1];

%Camera 2 (east side)
Cx2 = ax;
Cy2 = ay/2;
Cz2 = az;
C2 = [Cx2; Cy2; Cz2];

%--Rotation--
%Camera 1
thx1 = 0;
thy1 = pi/1.5; %point 45 deg down
thz1 = 0;

%Camera 2
thx2 = 0;
thy2 = -pi/1.5; %point 45 deg down
thz2 = pi;
ccp = [0 ay/2 az ax ay/2 az 0 pi/2 0 0 pi/2 pi];
ccpc(1,:) = ccp;
OPTIONS = optimset('TolFun',1e-3,'MaxFunEvals',1e5,'MaxIter',1e5);
ccp = fminsearch('fit3Dlocation',ccp,OPTIONS,rxyz,c1xy,c2xy);
ccpc(2,:) = ccp;
figure(2);clf; plot(ccpc(1,:),'r*'); hold on;
plot(ccpc(2,:),'bo');


exyz = get3Dlocation(ccp,c1xy,c2xy);
[exyz rxyz]
clr1 = 'rgbmckyk';
clr2 = 'ykcmbgrk';
mark1 = 'sdvphx*o';
figure(1);clf; axis([0 45000 10000 20000]);
[nums,numc] = size(c1xy);
for i = 1:nums
    plot3(exyz(i,1),exyz(i,2),exyz(i,3),[clr1(i),mark1(i)]); hold on;
    plot3(rxyz(i,1),rxyz(i,2),rxyz(i,3),[clr2(i),mark1(i)]);hold on
    xlim([0 20000]);
    ylim([0 10000]);
    zlim([0 10000]);
    %axis([0 45000 10000 20000]);
    pause(0.5)
    drawnow

end

err = mean(sqrt(sum((exyz-rxyz).^2,2)));

disp(sprintf('fitting error is %d',err));


