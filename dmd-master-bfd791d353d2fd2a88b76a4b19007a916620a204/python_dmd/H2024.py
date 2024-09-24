import numpy as np
import matplotlib.pyplot as plt



class Hankel:
    time = np.load('time.npy')
    a = np.load('a.npy')
    b = np.load('b.npy')
    y = np.load('y.npy')
    vdd = np.load('vdd.npy')
    vd = max(vdd)

    inn = np.matrix(time)
    inn = np.append(inn,[a],axis = 0)
    inn = np.append(inn,[b],axis = 0)

    out = np.matrix(vdd)

    out = np.append(out,[y],axis = 0)
    # print(out.shape,1111111111)

    time = inn[0,:]   #inn是np.matrix类型,第一行是time  第二行开始每一行代表一个输入
    #a = inn[1,:]
    #b = inn[2,:]
    #c = inn[3,:]
    #d = inn[4,:]
    #size_in = len(inn)
    #y = out[1:len(out),:]   #out是np.matrix类型,第一行是vdd  第二行开始每一行代表一个输出
    #vdd = out[0,:]
    #for i in range(len(out)):
    #y1 = out[1,:]
    #y2 = out[2,:]
    #y3 = out[3,:]
    y_arr = out.tolist()       #列表形式
    in_arr = inn.tolist()
    def __init__(self,n = 10*len(in_arr[0]),m = min(20,len(in_arr[0])//10)):
        self.n = n
        self.m = m

    def embedding(self):
        self.T1 = np.linspace(min(self.in_arr[0]),max(self.in_arr[0]),self.n) # 起点为time中最小值，终点为time(end)，取n个点
        for i in range(1,len(self.inn)):
            self.in_arr[i] = np.interp(self.T1, self.in_arr[0], self.in_arr[i])
        for i in range(1,len(self.out)):
            self.y_arr[i] = np.interp(self.T1, self.in_arr[0], self.y_arr[i])
        self.y = np.matrix(self.y_arr[1:len(self.y_arr)])   #y为矩阵形式的输出
        self.size_y = len(self.y)

    def mode(self):
        self.mod = np.matrix(self.in_arr[1] * self.in_arr[2])
        self.mod = self.mod[:,self.m:self.n]
        self.mod = np.append(self.mod,[[1] * (self.n-self.m)],axis = 0)

    def build_H(self):
        self.H = np.matrix(self.y[:,0:self.n-self.m])
        for i in range(1,self.m):
            self.H = np.append(self.H,self.y[:,i:self.n-self.m+i],axis = 0)
        self.H = np.append(self.H,self.mod,axis = 0)
        self.HNI = np.linalg.pinv(self.H)
        self.xp = self.y[:,self.m:self.n]
        self.A1 = self.xp * self.HNI

    def calculate_Y(self):
        self.H1 = self.H[:,0:self.m]
        self.Yp1 = self.A1*self.H1[:,0:self.m]
        for i in range(self.m,self.n-self.m):
            self.s = np.append([self.H1[self.size_y:len(self.H1)-len(self.mod),i-1]],[self.Yp1[:,i-1]])
            self.s = np.append(self.s,self.H[len(self.H)-len(self.mod):len(self.H),i])
            self.s = np.array([self.s]).T
            self.H1 = np.append(self.H1,self.s[0:len(self.H1)],axis = 1)
            self.Yp1 = self.A1*self.H1
        for i in range(0,self.size_y):
            for j in range(0,len(self.Yp1.T)):
                if self.Yp1[i,j] > self.vd:
                    self.Yp1[i,j] = self.vd
                if self.Yp1[i,j] < 0:
                    self.Yp1[i,j] = 0
                else:
                    pass

    def compare(self):
        self.yp1 = self.Yp1[0,:]
        self.yt = self.xp
        self.dif_y = [0]*len(self.yt.T)
        for i in range(0,len(self.yt.T)):
            self.dif_y[i]=self.yp1[0,i]-self.yt[0,i]

    def test(self):
        print("测试，time的长度 = %d" % len(self.in_arr[0]))
        print("测试，T1的长度 = %d" % len(self.T1))
        print("H的维度",self.H.shape)

if __name__=="__main__":
    hankel = Hankel()
    hankel.embedding()
    hankel.mode()
    hankel.build_H()
    hankel.test()
    hankel.calculate_Y()
    hankel.compare()
    #print(hankel.dif_y[20:50])
    plt.plot(hankel.T1[0:len(hankel.dif_y)],hankel.dif_y)
    plt.show()