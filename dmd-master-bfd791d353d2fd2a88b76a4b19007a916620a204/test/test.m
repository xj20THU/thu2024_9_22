clear all;
load nand.mat
close all
n = 100000;


%% 差值，均匀时间
% T1=(0:n-1)*TIME(end)/(n-1);
% a = interp1(TIME, a, T1);
% b = interp1(TIME, b, T1);
% y = interp1(TIME, y, T1);
% TIME=T1;

%% 不差值，采用原始时间
dt = diff(TIME);

figure
subplot(3, 1, 1);
plot(TIME, a);
subplot(3, 1, 2);
plot(TIME, b);
subplot(3, 1, 3);
plot(TIME, y);

XX = y;%[y;a;b];
Xp = (XX(:,2:end)-XX(:,1:end-1))./dt;
% Xp = XX(:,2:end);
X  = XX(:, 1:end-1);
% X(2:3,:) = XX(2:3, 2:end);

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
H = [H;a(m+1:end);b(m+1:end)];

figure 
[U,S,V] = svd(H,'econ');
r = 5;
U=U(:,1:r);
S=S(1:r,1:r );
V=V(:,1:r);
plot(diag(S))
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

% net = fitnet([50, 50], 'traingdm');
% net = train(net, H, yt);
% yp2 = net(H);
% yp2 = A2*H+fitinfo.Intercept(1);
figure
plot(TIME, yt, TIME, yp1, 'LineWidth', 2)
% plot(TIME, yt-yp2)

% figure
% plot(TIME, V(:,end))
% subplot(3,1,2)
% % plot(TIME, Xp(2,:), TIME, Yp1(2,:), TIME, Yp2(2,:))
% % subplot(3,1,3)
% % plot(TIME, Xp(3,:), TIME, Yp1(3,:), TIME, Yp2(3,:))
% 
% % figure 
% plot(TIME, V(:,10))
% figure 
% plot(TIME, V(:,1), TIME, V(:,4))
% % step 2
% Sinv = S(1:r,1:r)^(-1);
% Atilde = U(:,1:r)'*XD2*V(:,1:r)*Sinv(1:r,1:r);