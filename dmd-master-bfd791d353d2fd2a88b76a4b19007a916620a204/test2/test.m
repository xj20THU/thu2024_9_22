clear all;
load nand.mat
close all
n = 10000;
dt = TIME(end)/(n-1);
T1=(0:n-1)*dt;
a = interp1(TIME, a, T1);
b = interp1(TIME, b, T1);
y = interp1(TIME, y, T1);
TIME=T1;
figure
subplot(3, 1, 1);
plot(TIME, a);
subplot(3, 1, 2);
plot(TIME, b);
subplot(3, 1, 3);
plot(TIME, y);
X = [y;a;b];
Xp = X(:,2:end);
X = X(:, 1:end-1);
% X = [X;X.^2;X.^3];
% X = [X;X(1,:).*X(2,:)];
% X = [X;X(2,:).*X(3,:)];
% X = [X;X(1,:).*X(3,:)];
n = size(X, 2);
m = 20;
H = [];
for i=1:m
    H = [H;X(:,i:n-m+i)];
end

figure 
[U,S,V] = svd(H,'econ');
r = 20;
U=U(:,1:r);
S=S(1:r,1:r );
V=V(:,1:r);
plot(diag(S))
yt = y(m+1:end);
A1 = yt*pinv(H);
A2 = yt*V*inv(S)*U';
figure 
TIME=TIME(1:n-m+1);
yp1 = A1*H;
yp2 = A2*H;
plot(TIME, yt, TIME, yp1)
figure 
%plot(TIME, yt, TIME, yp2)
plot(TIME, V(:,1), TIME, V(:,4))
% % step 2
% Sinv = S(1:r,1:r)^(-1);
% Atilde = U(:,1:r)'*XD2*V(:,1:r)*Sinv(1:r,1:r);