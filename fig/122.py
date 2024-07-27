import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
mpl.rcParams["font.sans-serif"]=["SimHei"]#显示中文
#name=["type 0","type 1","type 2"]
name = ["MB算法","RSB算法","SSB算法"]
x=np.arange(1,4,1)
rm1=[89,0,0]
rm2=[11,100,100]
rc1=[100,6,95]
rc2= [0,94,5]
ra1=[97,0,0]
ra2=[3,100,100]
bar_width1 =0.2
g1p = [89,100,97]
g1n = [11,0,3]
g2p = [0,6,0]
g2n = [100,94,100]
g3p = [0,95,0]
g3n =[100,5,100]
# plt.bar(x-0.1,rm1,bar_width1,color='orange',label='阴性率',edgecolor='black')
# plt.bar(x+0.1,rm2,bar_width1,color='deepskyblue',label='阳性率',edgecolor='black')#edgecolor给边界加黑框
# plt.bar(x-0.1,rc1,bar_width1,color='orange',label='阴性率',edgecolor='black')
# plt.bar(x+0.1,rc2,bar_width1,color='deepskyblue',label='阳性率',edgecolor='black')#edgecolor给边界加黑框
# plt.bar(x-0.1,ra1,bar_width1,color='orange',label='阴性率',edgecolor='black')
# plt.bar(x+0.1,ra2,bar_width1,color='deepskyblue',label='阳性率',edgecolor='black')#edgecolor给边界加黑框
plt.bar(x-0.1,g3p,bar_width1,color='orange',label='阴性率',edgecolor='black')
plt.bar(x+0.1,g3n,bar_width1,color='deepskyblue',label='阳性率',edgecolor='black')#edgecolor给边界加黑框
plt.legend(loc="upper right", fontsize=15)
plt.xticks(x,name,fontsize=15)#设置坐标标签
plt.yticks([0,20,40,60,80,100])
plt.ylim([0,130])
plt.xlabel("算法",fontdict={'size':15})
plt.ylabel("百分比(%)",fontdict={'size':15})
plt.show()
