import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
mpl.rcParams["font.sans-serif"]=["SimHei"]#显示中文
#name=["type 0","type 1","type 2"]
bar_width1=0.2
x = [1,2,3,4,5]
rs = [1735+503,3435+1018,5112+1643,6785+2148,8710+2690]
bs = [2003,3868,5267,7224,8514]
zk = [2230,4258,6392,8232,10190]
plt.plot(x, rs, color='b', linestyle='--', label='DBRS', marker='o')#s,+,x,.
plt.plot(x, bs, color='g', linestyle='--', label='BSBE', marker='s')#s,+,x,.
plt.plot(x, zk, color='r', linestyle='--', label='ZK-SNARK', marker='x')#s,+,x,.
plt.legend(loc="upper left", fontsize=15)
plt.xticks(x)#设置坐标标签
plt.yticks([0,2000,4000,6000,8000,10000,12000])
plt.ylim([0,12000])
plt.xlim([1,5])
plt.xlabel("匿名分配次数",fontdict={'size':15})
plt.ylabel("耗时(ms)",fontdict={'size':15})
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()