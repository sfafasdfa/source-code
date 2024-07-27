import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.rcParams.update({'font.size': 16})
data = pd.read_csv("./data.csv",header=0)

it = data['iter'].values
marl = data['MARL'].values
aco = data['ACO'].values
greedy =  data['GR'].values
rand =  data['RND'].values

plt.figure(figsize=(60, 48), dpi=120)
plt.plot(it, marl, color='b', linestyle='--', label='MARL', marker='o')#s,+,x,.
plt.plot(it, aco, color='r', linestyle='--', label='AC', marker='*')
plt.plot(it, greedy, color='g', linestyle='--', label='Greedy', marker='+')
plt.plot(it, rand, color='grey', linestyle='--', label='Random', marker='x')
xticks = [i for i in range(0, 1001,250)]
yticks =[i for i in range(0, 150001,2500)]
plt.xticks(xticks)
plt.xlim([0,1000])
plt.yticks(yticks)
plt.ylim([0,15000])

plt.grid(True, linestyle='--', alpha=0.5)

    # 添加描述信息
plt.xlabel('训练轮次',fontdict={'size':15})
plt.ylabel('奖励值均值',fontdict={'size':15})
plt.legend(loc="upper left", fontsize=15)

    # 4、显示图
plt.show()
