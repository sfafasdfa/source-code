import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
mpl.rcParams["font.sans-serif"]=["SimHei"]#显示中文
name=["MARL","AC","Random","Greedy"]
x=[7,8,9,10]
marl = [1645,1527,1387,1274]
ac =[1078,975,856,820]
rand = [538,530,518,491]
greedy = [1035,970,906,854]

plt.plot(x, marl, color='b', linestyle='--', label='MARL', marker='1')#s,+,x,.
plt.plot(x, ac, color='r', linestyle='--', label='AC', marker='*')
plt.plot(x, rand, color='g', linestyle='--', label='Random', marker='+')
plt.plot(x, greedy, color='grey', linestyle='--', label='Greedy', marker='x')

plt.legend(loc="upper right", fontsize=15)
plt.xticks(x)#设置坐标标签
#plt.yticks([-1,-0.5,0,0.5,1,1.5,2,2.5])
plt.yticks([250,500,750,1000,1250,1500,1750,2000])
plt.ylim([250,2000])
plt.xlim([7,10])
plt.xlabel("智能体数量",fontdict={'size':15})
#plt.ylabel("平均信誉",fontdict={'size':15})
plt.ylabel("平均奖励",fontdict={'size':15})
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()