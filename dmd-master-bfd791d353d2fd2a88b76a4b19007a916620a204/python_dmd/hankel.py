import numpy as np


class Hankel:
    time = np.load('time.npy')
    a = np.load('a.npy')
    b = np.load('b.npy')
    y = np.load('y.npy')
    vdd = np.load('vdd.npy')

    def __init__(self,n=10000,m=20):
        self.n = n
        self.m = m

    def embedding(self):
        self.T1 = np.linspace(0,max(self.time),self.n) # 起点为0，终点为time(end)，取n个点
        self.y = np.interp(self.T1, self.time, self.y)
        self.a = np.interp(self.T1, self.time, self.a)
        self.b = np.interp(self.T1, self.time, self.b)

    def mode(self):
        self.ab = self.a * self.b
        self.c = [1] * (self.n-self.m)

    def build_H(self):
        self.H = np.matrix(self.y[0:self.n-self.m])
        for i in range(1,self.m):
            self.H = np.append(self.H,[self.y[i:self.n-self.m+i]],axis = 0)
        self.H = np.append(self.H,[self.ab[self.m:self.n]],axis = 0)
        self.H = np.append(self.H,[self.c[0:self.n-self.m]],axis = 0)
        self.HNI = np.linalg.pinv(self.H)
        self.xp = self.y[self.m:self.n]
        self.A1 = np.matmul(self.xp,self.HNI)

    def calculate_Y(self):
        self.H1 = self.H[:,0:self.m]
        self.Yp1 = self.A1*self.H1[:,0:self.m]
        for i in range(self.m,self.n-self.m):
            self.s = np.append([self.H1[1:len(self.H1)-2,i-1]],[self.Yp1[:,i-1]])
            self.s = np.append(self.s,self.H[len(self.H)-2:len(self.H),i])
            self.s = np.array([self.s]).T
            self.H1 = np.append(self.H1,self.s[0:len(self.H1)],axis = 1)
            self.Yp1 = self.A1*self.H1

    def compare(self):
        self.yp1 = self.Yp1[0,:]
        self.yt = self.xp
        self.dif_y = [0]*len(self.yt)
        for i in range(0,len(self.yt)):
            self.dif_y[i]=self.yp1[0,i]-self.yt[i]

    def test(self):
        print("测试，time的长度 = %d" % len(self.time))
        print("测试，T1的长度 = %d" % len(self.T1))
        print("H的维度",self.H.shape)

if __name__=="__main__":
    hankel = Hankel(10000,20)
    hankel.embedding()
    hankel.mode()
    hankel.build_H()
    hankel.test()
    hankel.calculate_Y()
    hankel.compare()
    print(hankel.dif_y[20:50])

    