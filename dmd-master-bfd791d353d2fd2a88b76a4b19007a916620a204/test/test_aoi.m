clear all;
load aoi22.mat
close all
n = 100000;


%% 差值，均匀时间
T1=(0:n-1)*TIME(end)/(n-1);
a = interp1(TIME, a, T1);
b = interp1(TIME, b, T1);
c = interp1(TIME, c, T1);
d = interp1(TIME, d, T1);
y = interp1(TIME, y, T1);
TIME=T1;

%% 不差值，采用原始时间
dt = diff(TIME);

figure
subplot(5, 1, 1);
plot(TIME, a);
subplot(5, 1, 2);
plot(TIME, b);
subplot(5, 1, 3);
plot(TIME, c);
subplot(5, 1, 4);
plot(TIME, d);
subplot(5, 1, 5);
plot(TIME, y);

XX = y;%[y;a;b];
Xp = XX(:,2:end);
X  = XX(:, 1:end-1);

n = size(X, 2);
m = 20;
H = [];
for i=1:m
    H = [H;X(:,i:n-m+i)];
end
H = [H;a(m+1:end);b(m+1:end);c(m+1:end);d(m+1:end)];

figure 
[U,S,V] = svd(H,'econ');
plot(diag(S))
r = 10;
U=U(:,1:r);
S=S(1:r,1:r );
V=V(:,1:r);

Xp = Xp(:,m:end);
% yt = Xp(1,m:end); %y(m+1:end);

A1 = Xp*pinv(H);
A2 = Xp*V*inv(S)*U';
% [B2,fitinfo] = lasso(H', yt','Lambda',1e-5);
% A2 = B2(:,1)';

TIME=TIME(1:n-m+1);
Yp1 = A1*H;
Yp2 = A2*H;

yt  = Xp(1,:);
yp1 = Yp1(1,:);
yp2 = Yp2(1,:);

figure
plot(TIME, yt, TIME, yp1, TIME, yp2)

figure
plot(TIME, abs(yt-yp1))
