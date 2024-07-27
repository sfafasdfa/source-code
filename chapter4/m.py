import random
import math
import os
import numpy as np
import csv
import pandas as pd
'''
type 0:
95%  10%
5%  random
type 1:
100% 30%
type 2:
50% 10%
50% random

data: 10%:valid 30%:invalid other%:complaint
'''
class worker:
    def __init__(self, wtype, reputation):
        self.type = wtype
        self.reputation = reputation
        self.state = True
    def updatestate(self, newstate):
        self.state = newstate
    def updateputation(self, newreputation):
        self.reputation = newreputation

def markov(r_old, valid, invalid, complaint,n):
    eta = valid/n
    r_new = (r_old*eta +valid-invalid-complaint)/(valid+invalid+complaint+1)
    return r_new

def cloud(r_old,miu, valid, invalid,complaint,alpha,beta,tv,n):
    
    lr = (1/n)*(valid*((valid+1)/(valid+invalid+complaint+1)+alpha)+(invalid+complaint)*((valid)/(valid+invalid+complaint+1)+2-beta))
    gr = r_old*(math.exp(-tv))+lr/n
    r_new = miu*gr+(1-miu)*lr
    return r_new
def anew(r_old, miu, t,tv, valid, invalid, complaint,R,P):
    rh =r_old*(1-math.exp(-t*tv))
    rc = math.exp(-invalid-complaint)*R-math.exp(-valid)*P
    r_new = miu*rh+(1-miu)*rc
    return r_new


rm = []
rc = []
ra = []
rd = []
datalist = [{'m0':1,'m1':1,'m2':1,'m0p':100,'m1p':100,'m2p':100,
             'c0':1,'c1':1,'c2':1,'c0p':100,'c1p':100,'c2p':100,
             's0':1,'s1':1,'s2':1,'s0p':100,'s1p':100,'s2p':100,
             'd0':1,'d1':1,'d2':1,'d0p':100,'d1p':100,'d2p':100}]
miu = 0.7
n = 10
alpha = 1
beta =2
tv =0.5
for i in range(0,1000):
    rand = random.random()
    if rand < 0.5:
        rm.append(worker(0,1))
        rc.append(worker(0,1))
        ra.append(worker(0,1))
        rd.append(worker(0,1))
    elif rand <0.75:
        rm.append(worker(1,1))
        rc.append(worker(1,1))
        ra.append(worker(1,1))
        rd.append(worker(1,1))
    else:
        rm.append(worker(2,1))
        rc.append(worker(2,1))
        ra.append(worker(2,1))
        rd.append(worker(2,1))

for i in range(0,5):
    w = [0 for i in range(0,1000)]
    for j in range(0,1000):
        if rm[j].type == 0:
            valid = 0
            invalid = 0
            complaint = 0
            vr = []
            vp = []
            for k in range(0,10):
                rand = random.random()
                if rand <0.95:
                    valid = valid + 1
                    error = (random.random())/10
                    vr.append(math.tanh(1/error)+1)
                else:
                    error = random.random()
                    if error < 0.1:
                        valid = valid + 1
                        vr.append(math.tanh(1/error)+1)
                    elif error < 0.3:
                        invalid = invalid +1
                        vp.append(math.tanh(1/error)+1)
                    else:
                        complaint = complaint+1
                        vp.append(math.tanh(1/error)+1)
            r = ((math.fsum(vr))+alpha*len(vr))/10
            p = ((2*len(vp)-math.fsum(vr))+beta*len(vp))/10
            w[j] = valid
            rm[j].reputation = markov(r_old=rm[j].reputation,valid=valid,invalid=invalid,complaint=complaint,n=10)
            
            rc[j].reputation = cloud(r_old=rc[j].reputation,miu=miu,valid=valid,invalid=invalid,complaint=complaint,alpha=alpha,beta=beta,tv=tv,n=10)
            ra[j].reputation = anew(r_old=ra[j].reputation,miu=miu,t=i,tv=tv,valid=valid,invalid=invalid,complaint=complaint,R=r,P=p)
            if rm[j].reputation < 0.6:
                rm[j].state = False
            if rc[j].reputation < 0.4:
                rc[j].state = False
            if ra[j].reputation < 0.09:
                ra[j].state = False
        elif rm[j].type == 1:
            valid = 0
            invalid = 0
            complaint = 0
            vr = []
            vp = []
            for k in range(0,10):
                error = random.random()*0.3
                if error <0.1:
                    valid = valid + 1
                    vr.append(math.tanh(1/error)+1)
                else:
                    vp.append(math.tanh(1/error)+1)
                    invalid = invalid +1
            r = ((math.fsum(vr))+alpha*len(vr))/10
            p = ((2*len(vp)-math.fsum(vr))+beta*len(vp))/10
            w[j] = valid
            rm[j].reputation = markov(r_old=rm[j].reputation,valid=valid,invalid=invalid,complaint=complaint,n=10)
            rc[j].reputation = cloud(r_old=rc[j].reputation,miu=miu,valid=valid,invalid=invalid,complaint=complaint,alpha=alpha,beta=beta,tv=tv,n=10)
            ra[j].reputation = anew(r_old=ra[j].reputation,miu=miu,t=i,tv=tv,valid=valid,invalid=invalid,complaint=complaint,R=r,P=p)
            if rm[j].reputation < 0.6:
                rm[j].state = False
            if rc[j].reputation < 0.4:
                rc[j].state = False
            if ra[j].reputation < 0.09:
                ra[j].state = False
        else:
            valid = 0
            invalid = 0
            complaint = 0
            vr = []
            vp = []
            for k in range(0,10):
                rand = random.random()
                if rand <0.5:
                    valid = valid + 1
                    error = (random.random())/10
                    vr.append(math.tanh(1/error)+1)
                else:
                    error = random.random()
                    if error < 0.1:
                        valid = valid + 1
                        vr.append(math.tanh(1/error)+1)
                    elif error < 0.3:
                        invalid = invalid +1
                        vp.append(math.tanh(1/error)+1)
                    else:
                        complaint = complaint+1
                        vp.append(math.tanh(1/error)+1)
            r = ((math.fsum(vr))+alpha*len(vr))/10
            p = ((2*len(vp)-math.fsum(vr))+beta*len(vp))/10
            w[j] = valid
            rm[j].reputation = markov(r_old=rm[j].reputation,valid=valid,invalid=invalid,complaint=complaint,n=10)
            rc[j].reputation = cloud(r_old=rc[j].reputation,miu=miu,valid=valid,invalid=invalid,complaint=complaint,alpha=alpha,beta=beta,tv=tv,n=10)
            ra[j].reputation = anew(r_old=ra[j].reputation,miu=miu,t=i,tv=tv,valid=valid,invalid=invalid,complaint=complaint,R=r,P=p)
            if rm[j].reputation < 0.6:
                rm[j].state = False
            if rc[j].reputation < 0.4:
                rc[j].state = False
            if ra[j].reputation < 0.09:
                ra[j].state = False
    for j in range(0,1000,5):
        total = w[j]+w[j+1]+w[j+2]+w[j+3]+w[j+4]
        w[j]=w[j]/total
        w[j+1]=w[j+1]/total
        w[j+2]=w[j+2]/total
        w[j+3]=w[j+3]/total
        w[j+4]=w[j+4]/total
    for j in range(0,1000):
        rd[j].reputation = miu*rd[j].reputation+(1-miu)*w[j]
    for j in range(0,1000,5):
        total = rd[j].reputation+rd[j+1].reputation+rd[j+2].reputation+rd[j+3].reputation+rd[j+4].reputation
        rd[j].reputation=rd[j].reputation/total
        rd[j+1].reputation=rd[j+1].reputation/total
        rd[j+2].reputation=rd[j+2].reputation/total
        rd[j+3].reputation=rd[j+3].reputation/total
        rd[j+4].reputation=rd[j+4].reputation/total
    for j in range(0,1000):
        rd[j].reputation = rd[j].reputation*4
        if rd[j].reputation <0.8:
            rd[j].state = False
    if (i+1) %1 == 0:
        count0=0
        count1=0
        count2=0
        rm0=[]
        rm1=[]
        rm2=[]
        rm0p = 0
        rm1p = 0
        rm2p = 0
        rc0=[]
        rc1=[]
        rc2=[]
        rc0p = 0
        rc1p = 0
        rc2p = 0
        ra0=[]
        ra1=[]
        ra2=[]
        ra0p = 0
        ra1p = 0
        ra2p = 0
        rd0=[]
        rd1=[]
        rd2=[]
        rd0p = 0
        rd1p = 0
        rd2p = 0
        for j in range(0,1000):
            if rm[j].type == 0:
                count0 += 1
                if rm[j].state == True:
                    rm0p += 1
                if rc[j].state == True:
                    rc0p += 1
                if ra[j].state == True:
                    ra0p += 1
                if rd[j].state == True:
                    rd0p += 1
                rm0.append(rm[j].reputation)
                rc0.append(rc[j].reputation)
                ra0.append(ra[j].reputation)
                rd0.append(rd[j].reputation)
            elif rm[j].type == 1:
                count1 +=1
                if rm[j].state == True:
                    rm1p += 1
                if rc[j].state == True:
                    rc1p += 1
                if ra[j].state == True:
                    ra1p += 1
                if rd[j].state == True:
                    rd1p += 1
                rm1.append(rm[j].reputation)
                rc1.append(rc[j].reputation)
                ra1.append(ra[j].reputation)
                rd1.append(rd[j].reputation)
            else:
                count2 +=1
                if rm[j].state == True:
                    rm2p += 1
                if rc[j].state == True:
                    rc2p += 1
                if ra[j].state == True:
                    ra2p += 1
                if rd[j].state == True:
                    rd2p += 1
                rm2.append(rm[j].reputation)
                rc2.append(rc[j].reputation)
                ra2.append(ra[j].reputation)
                rd2.append(rd[j].reputation)
        print(f"after {i+1}th iteration")
        print("markov group")
        mean0 = np.mean(rm0)
        mean1 = np.mean(rm1)
        mean2 = np.mean(rm2)
        std0 = np.std(rm0)
        std1 = np.std(rm1)
        std2 = np.std(rm2)
        print(f"0group  mean:{mean0} std:{std0}")
        print(f"1group  mean:{mean1} std:{std1}")
        print(f"2group  mean:{mean2} std:{std2}")
        print(f"0 group true:{rm0p/count0} ")
        print(f"1 group true:{rm1p/count1} ")
        print(f"2 group true:{rm2p/count2} ")
        print("............................")
        print("cloud group")
        mean0 = np.mean(rc0)
        mean1 = np.mean(rc1)
        mean2 = np.mean(rc2)
        std0 = np.std(rc0)
        std1 = np.std(rc1)
        std2 = np.std(rc2)
        print(f"0group  mean:{mean0} std:{std0}")
        print(f"1group  mean:{mean1} std:{std1}")
        print(f"2group  mean:{mean2} std:{std2}")
        print(f"0 group true:{rc0p/count0} ")
        print(f"1 group true:{rc1p/count1} ")
        print(f"2 group true:{rc2p/count2} ")
        print("............................")
        print("anew group")
        mean0 = np.mean(ra0)
        mean1 = np.mean(ra1)
        mean2 = np.mean(ra2)
        std0 = np.std(ra0)
        std1 = np.std(ra1)
        std2 = np.std(ra2)
        print(f"0group  mean:{mean0} std:{std0}")
        print(f"1group  mean:{mean1} std:{std1}")
        print(f"2group  mean:{mean2} std:{std2}")
        print(f"0 group true:{ra0p/count0} ")
        print(f"1 group true:{ra1p/count1} ")
        print(f"2 group true:{ra2p/count2} ")
        print("............................")
        print("decb group")
        mean0 = np.mean(rd0)
        mean1 = np.mean(rd1)
        mean2 = np.mean(rd2)
        std0 = np.std(rd0)
        std1 = np.std(rd1)
        std2 = np.std(rd2)
        print(f"0group  mean:{mean0} std:{std0}")
        print(f"1group  mean:{mean1} std:{std1}")
        print(f"2group  mean:{mean2} std:{std2}")
        print(f"0 group true:{rd0p/count0} ")
        print(f"1 group true:{rd1p/count1} ")
        print(f"2 group true:{rd2p/count2} ")
        print("............................")
        print("==================================")
        print("==================================")
        datalist.append({'m0':np.mean(rm0),'m1':np.mean(rm1),'m2':np.mean(rm2),'m0p':rm0p/count0*100,'m1p':rm1p/count1*100,'m2p':rm2p/count2*100,
             'c0':np.mean(rc0),'c1':np.mean(rc1),'c2':np.mean(rc2),'c0p':rc0p/count0*100,'c1p':rc1p/count1*100,'c2p':rc2p/count2*100,
             's0':np.mean(ra0),'s1':np.mean(ra1),'s2':np.mean(ra2),'s0p':ra0p/count0*100,'s1p':ra1p/count1*100,'s2p':ra2p/count2*100,
             'd0':np.mean(rd0),'d1':np.mean(rd1),'d2':np.mean(rd2),'d0p':rd0p/count0*100,'d1p':rd1p/count1*100,'d2p':rd2p/count2*100})

with open('linedata.csv',"w") as file:
    header = ['m0','m1','m2','m0p','m1p','m2p',
             'c0','c1','c2','c0p','c1p','c2p',
             's0','s1','s2','s0p','s1p','s2p',
             'd0','d1','d2','d0p','d1p','d2p']
    writer = csv.DictWriter(file,fieldnames=header)
    writer.writeheader()
    writer.writerows(datalist)


            

                



