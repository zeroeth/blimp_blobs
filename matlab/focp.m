% part of blimp 3D tracking
% focp.m (find optimized camera parameters)
clear;clc;home

pd1 = 'C:\Users\yuming\Documents\GitHub\blimp_blobs\';
filename = [pd1,'tracking_optimization.xlsx'];
num = xlsread(filename,'A2:G58');
chc = [1:57];
rxyz = num(chc,5:7);
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
% ccp = [0 ay/2 az ax ay/2 az 0 pi/2 0 0 -pi/2 pi];
ccp = [ Cx1 Cy1 Cz1 Cx2 Cy2 Cz2 thx1 thy1 thz1 thx2 thy2 thz2];
% ccp(1:6)= 1.0e+04 *[
% 
%    -0.0000    0.4214    0.6803    1.2828    0.6224    0.6585];
% ccp(7:12) =  [-0.0086    1.3983    0.0235    0.0039    0.0160    1.3337];
%    
ccpc(1,:) = ccp;
OPTIONS = optimset('TolFun',1e-3,'MaxFunEvals',1e5,'MaxIter',1e5);
ccp = fminsearch('fit3Dlocation',ccp,OPTIONS,rxyz,c1xy,c2xy);
ccpc(2,:) = ccp;
% figure(2);clf; plot(ccpc(1,:),'r*'); hold on;
% plot(ccpc(2,:),'bo');
figure(1);clf; set(gcf,'position',[50 100 500 250])
subplot(1,2,1);
plot(ccpc(1,1:6),'r*'); hold on;
plot(ccpc(2,1:6),'bo');
title('translation parameters');

subplot(1,2,2);
plot(ccpc(1,7:12),'r*'); hold on;
plot(ccpc(2,7:12),'bo');
title('rotation parameters');



exyz = get3Dlocation(ccp,c1xy,c2xy);
[exyz rxyz]
clr1 = 'rgbmckyrgbmcky';
clr2 = 'ykcmbgrykcmbgr';
mark1 = 'sdvphxo*+.<>';
figure(2);clf; axis equal; set(gcf,'position',[650 100 500 500])
[nums,numc] = size(c1xy);
k = 0;
for i = 1:6:nums
    k = k +1;
    pause;disp('new point, press any key to continue ...');
    plot3(exyz(i,1),exyz(i,2),exyz(i,3),[clr1(k),mark1(k)],'MarkerSize',12); hold on;
    pause;disp('press any key to continue ...');
    plot3(rxyz(i,1),rxyz(i,2),rxyz(i,3),[clr2(k),mark1(k)],'MarkerSize',12);hold on
    xlim([0 15000]);
    ylim([0 10000]);
    zlim([0 10000]);
    %axis([0 45000 10000 20000]);
    
    drawnow

end
% 
err = mean(sqrt(sum((exyz-rxyz).^2,2)));
disp(sprintf('fitting error is %d',err));
figure(1);figure(2)
