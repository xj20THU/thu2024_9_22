clear all;
load nand.mat
close all
n = 10000;


%% 差�?，均�?���?
T1=(0:n-1)*TIME(end)/(n-1);
a = interp1(TIME, a, T1);
b = interp1(TIME, b, T1);
y = interp1(TIME, y, T1);
TIME=T1;


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
% Xp = (X(:,2:end)-X(:,1:end-1))./repmat(dt, 3, 1);
Xp = XX(:,2:end);
X  = XX(:, 1:end-1);
% X(2:3,:) = XX(2:3, 2:end);

% X = [X;X.^2;X.^3];
% X = [X;X(1,:).*X(2,:)];
% X = [X;X(2,:).*X(3,:)];
% X = [X;X(1,:).*X(3,:)];
n = size(X, 2);
m = 20;
H = [];
ab=a.*b;
for i=1:m
    H = [H;X(:,i:n-m+i);ab(i+1:n-m+i+1)];
end
c(1:n+1-m)=2.5;
H = [H;c(1:n+1-m)];

figure 
[U,S,V] = svd(H,'econ');
r = 20;
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
%Yp1 = A1*H;   %�Ľ�H����˴��в�����
Yp2 = A2*H;

%�Ľ�H
H1=H(:,1:m);           %H��ǰm�в��仯
Yp1(:,1:m)=A1*H1(:,1:m);    %��ǰm�е�Yp1

for i=m+1:n+1-m
    H1(:,i)=[H1(3:end-1,i-1);Yp1(:,i-1);H(end-1:end,i)];
    Yp1(:,i)=A1*H1(:,i);
end

yt  = Xp(1,:);
yp1 = Yp1(1,:); 
yp2 = Yp2(1,:);

figure
plot(TIME, yt, TIME, yp1)

%plot(yt-yp1)
%plot(yp1-A1*H)
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