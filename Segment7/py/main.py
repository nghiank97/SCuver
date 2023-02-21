
import numpy as np
import matplotlib.pyplot as plt

class LSPB:

    def __init__(self,*args,**kwargs):

        self.Amax = kwargs['A']
        self.Vmax = kwargs['V']
        self.Jmax = kwargs['J']
        self.index = kwargs['t']

        self.q0 = 0
        self.qf = 0

        self.T = 0
        self.t1 = 0
        self.t3 = 0
        self.t2 = 0
        self.t4 = 0
        self.t5 = 0
        self.t6 = 0

        self.a1 = self.Jmax
        self.a2 = 0
        self.a3 = -self.Jmax
        self.a4 = 0
        self.a5 = -self.Jmax
        self.a6 = 0
        self.a7 = self.Jmax

        self.position = 0
        self.velocity = 0
        self.t = 0
        self.finish = 1

    def get_data(self,t):
        if ((0<t) and (t<= self.t1)):
            self.position = t*t*t*self.a1/6 + t*t*self.b1/2 + t*self.c1 +self.d1
            self.velocity = t*t*self.a1/2 + t*self.b1 + self.c1

        elif ((self.t1<t) and (t<= self.t2)):
            self.position = t*t*t*self.a2/6 + t*t*self.b2/2 + t*self.c2 +self.d2
            self.velocity = t*t*self.a2/2 + t*self.b2 + self.c2

        elif ((self.t2<t) and (t<= self.t3)):
            self.position = t*t*t*self.a3/6 + t*t*self.b3/2 + t*self.c3 +self.d3
            self.velocity = t*t*self.a3/2 + t*self.b3 + self.c3

        elif ((self.t3<t) and (t<= self.t4)):
            self.position = t*t*t*self.a4/6 + t*t*self.b4/2 + t*self.c4 +self.d4
            self.velocity = t*t*self.a4/2 + t*self.b4 + self.c4

        elif ((self.t4<t) and (t<= self.t5)):
            self.position = t*t*t*self.a5/6 + t*t*self.b5/2 + t*self.c5 +self.d5
            self.velocity = t*t*self.a5/2 + t*self.b5 + self.c5

        elif ((self.t5<t) and (t<= self.t6)):
            self.position = t*t*t*self.a6/6 + t*t*self.b6/2 + t*self.c6 +self.d6
            self.velocity = t*t*self.a6/2 + t*self.b6 + self.c6

        elif ((self.t6<t) and (t< self.T)):  
            self.position = t*t*t*self.a7/6 + t*t*self.b7/2 + t*self.c7 +self.d7
            self.velocity = t*t*self.a7/2 + t*self.b7 + self.c7

    def set_velocity(self):
        return self.velocity

    def set_position(self):
        return self.position

    def operation(self,*args,**kwargs):
        delta = kwargs['sp']-self.qf
        if (delta != 0) and ((self.t >= self.T) or (self.t == 0)):
        
            self.q0 = self.qf
            self.qf = kwargs['sp']

            self.T = (self.Amax/self.Jmax) + (self.Vmax/self.Amax) + (self.qf/self.Vmax)
            
            self.t1 = self.Amax/self.Jmax
            self.t3 = self.t1 + (self.Vmax/self.Amax)
            self.t2 = self.t3 - self.t1

            self.t4 = self.T - self.t3
            self.t5 = self.T - self.t2
            self.t6 = self.T - self.t1

            self.b1 = 0
            self.b2 = self.Amax
            self.b3 = self.Amax + self.Jmax*self.t2
            self.b4 = 0
            self.b5 = self.Jmax*self.t4
            self.b6 = -self.Amax
            self.b7 = -self.Amax - self.Jmax*self.t6

            self.c1 = 0
            self.c2 = ((self.a1*self.t1**2)/2 + self.b1*self.t1 + self.c1) - ((self.a2*self.t1**2)/2 + self.b2*self.t1)
            self.c3 = ((self.a2*self.t2**2)/2 + self.b2*self.t2 + self.c2) - ((self.a3*self.t2**2)/2 + self.b3*self.t2)
            self.c4 = ((self.a3*self.t3**2)/2 + self.b3*self.t3 + self.c3) - ((self.a4*self.t3**2)/2 + self.b4*self.t3)
            self.c5 = ((self.a4*self.t4**2)/2 + self.b4*self.t4 + self.c4) - ((self.a5*self.t4**2)/2 + self.b5*self.t4)
            self.c6 = ((self.a5*self.t5**2)/2 + self.b5*self.t5 + self.c5) - ((self.a6*self.t5**2)/2 + self.b6*self.t5)
            self.c7 = ((self.a6*self.t6**2)/2 + self.b6*self.t6 + self.c6) - ((self.a7*self.t6**2)/2 + self.b7*self.t6)

            self.d1 = 0
            self.d2 = ((self.a1*self.t1**3)/6 + (self.b1*self.t1**2)/2 + self.c1*self.t1 + self.d1) - ((self.a2*self.t1**3)/6 + (self.b2*self.t1**2)/2 + self.c2*self.t1)
            self.d3 = ((self.a2*self.t2**3)/6 + (self.b2*self.t2**2)/2 + self.c2*self.t2 + self.d2) - ((self.a3*self.t2**3)/6 + (self.b3*self.t2**2)/2 + self.c3*self.t2)
            self.d4 = ((self.a3*self.t3**3)/6 + (self.b3*self.t3**2)/2 + self.c3*self.t3 + self.d3) - ((self.a4*self.t3**3)/6 + (self.b4*self.t3**2)/2 + self.c4*self.t3)
            self.d5 = ((self.a4*self.t4**3)/6 + (self.b4*self.t4**2)/2 + self.c4*self.t4 + self.d4) - ((self.a5*self.t4**3)/6 + (self.b5*self.t4**2)/2 + self.c5*self.t4)
            self.d6 = ((self.a5*self.t5**3)/6 + (self.b5*self.t5**2)/2 + self.c5*self.t5 + self.d5) - ((self.a6*self.t5**3)/6 + (self.b6*self.t5**2)/2 + self.c6*self.t5)
            self.d7 = ((self.a6*self.t6**3)/6 + (self.b6*self.t6**2)/2 + self.c6*self.t6 + self.d6) - ((self.a7*self.t6**3)/6 + (self.b7*self.t6**2)/2 + self.c7*self.t6)

            self.t = 0
            self.finish = 0

        if self.t < self.T:
            self.t+= self.index
            self.get_data(self.t)
        else:
            self.finish = 1
            self.get_data(self.t)

s_cuver = LSPB(A = 20,V = 12, J = 200, t = 0.01)

sp = [-10,10]
i = 0
j = 0
p = []
while(1):
    if (s_cuver.finish == 1):
        i+=1
        if(i == 2):
            i = 0
        j+=1
        if (j == 2):
            break
    s_cuver.operation(sp = sp[i])
    p.append(s_cuver.set_velocity())

position = np.array(p)

fig, axs = plt.subplots(2, sharex=True, sharey=True)
fig.suptitle('Profile')

axs[0].plot(position, c='r')
axs[0].legend()

plt.show()