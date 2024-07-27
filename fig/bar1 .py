import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
mpl.rcParams["font.sans-serif"]=["SimHei"]#显示中文
#name=["type 0","type 1","type 2"]

g3n=[349.504,320.504,2186.033]#合约消耗rs,bs,zk
g3p=[1971.077,1811.089,1116.160]#单次消耗
bar_width1=0.2
x = [1,2,3,4,5]
rs = []
bs = []
zk = []
for i in range(1,6):
    rs.append(g3n[0]+g3p[0]*i)
    bs.append(g3n[1]+g3p[1]*i)
    zk.append(g3n[2]+g3p[2]*i)
plt.plot(x, rs, color='b', linestyle='--', label='DBRS', marker='o')#s,+,x,.
plt.plot(x, bs, color='g', linestyle='--', label='BSBE', marker='s')#s,+,x,.
plt.plot(x, zk, color='r', linestyle='--', label='ZK-SNARK', marker='x')#s,+,x,.
plt.legend(loc="upper left", fontsize=15)
plt.xticks(x)#设置坐标标签
plt.yticks([0,2000,4000,6000,8000,10000,12000])
plt.ylim([0,12000])
plt.xlim([1,5])
plt.grid(True, linestyle='--', alpha=0.5)
plt.xlabel("匿名分配次数",fontdict={'size':15})
plt.ylabel("gas消耗(TWei)",fontdict={'size':15})
plt.show()