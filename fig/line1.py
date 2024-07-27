import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.rcParams.update({'font.size': 16})
# 1、获取数据
x = [0, 10, 20, 30, 40,50]
data = pd.read_csv("./linedata.csv",header=0)
markov0 = data['m0'].values
markov1 = data['m1'].values
markov2 = data['m2'].values
markov0t =data['m0p'].values
markov1t =data['m1p'].values
markov2t = data['m2p'].values
cloud0 = data['c0'].values
cloud1 = data['c1'].values
cloud2 = data['c2'].values
cloud0t = data['c0p'].values
cloud1t =data['c1p'].values
cloud2t = data['c2p'].values
ssb0 = data['s0'].values
ssb1 = data['s1'].values
ssb2 = data['s2'].values
ssb0t =data['s0p'].values
ssb1t =data['s1p'].values
ssb2t = data['s2p'].values
decb0 = data['d0'].values
decb1 = data['d1'].values
decb2 = data['d2'].values
decb0t =data['d0p'].values
decb1t =data['d1p'].values
decb2t = data['d2p'].values

# plt.plot(x, markov2, color='b', linestyle='--', label='MB', marker='1')#s,+,x,.
# plt.plot(x, cloud2, color='r', linestyle='--', label='RSB', marker='*')
# plt.plot(x, ssb2, color='g', linestyle='--', label='SSB', marker='+')
# plt.plot(x, decb2, color='grey', linestyle='--', label='DECB', marker='x')

plt.plot(x, markov2t, color='b', linestyle='--', label='MB', marker='1')#s,+,x,.
plt.plot(x, cloud2t, color='r', linestyle='--', label='RSB', marker='*')
plt.plot(x, ssb2t, color='g', linestyle='--', label='SSB', marker='+')
plt.plot(x, decb2t, color='grey', linestyle='--', label='DECB', marker='x')


plt.legend(loc="center right", fontsize=15)
plt.xticks(x)#设置坐标标签
# plt.yticks([-1,-0.5,0,0.5,1,1.5,2,2.5])
plt.yticks([0,20,40,60,80,100])
plt.ylim([-10,108])
plt.xlim([0,50])
plt.xlabel("上传数据次数",fontdict={'size':15})
# plt.ylabel("平均信誉",fontdict={'size':15})
plt.ylabel("阴性率(%)",fontdict={'size':15})
plt.grid(True, linestyle='--', alpha=0.5)
plt.annotate('此段MB和SSB曲线重合',(7.5,40),(12,40),arrowprops=dict(facecolor='k',alpha=0.5,lw=0.5,arrowstyle='simple',connectionstyle='arc3,rad=0.1',ec='k'))
plt.annotate('此段MB和SSB曲线重合',(35,5),(20,20),arrowprops=dict(facecolor='k',alpha=0.5,lw=0.5,arrowstyle='simple',connectionstyle='arc3,rad=0.1',ec='k'))
plt.show()
