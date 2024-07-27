import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import random
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

ant = pd.read_csv("./anttrac.csv",header=0)
rand = pd.read_csv("./randomtrac.csv",header=0)
marl = pd.read_csv("./marltrac.csv",header=0)
greedy = pd.read_csv("./greedytrac.csv",header=0)

t = ant['time'].values
ant_x = ant['x'].values
ant_y = ant['y'].values
rand_x = rand['x'].values
rand_y = rand['y'].values
greedy_x = greedy['x'].values
greedy_y = greedy['y'].values

marl_x = marl['x'].values
marl_y = marl['y'].values


# figsize是长宽，dpi是dot per inch
plt.figure(figsize=(60, 48), dpi=200)

# 3、绘制图像
x = []
y = []
for i in range(0,100):
    x.append(random.random()+marl_x[i])
for i in range(0,100):
    y.append(random.random()+marl_y[i])
plt.scatter(x, y)

# 显示图例，这里显示图例的前提是plt.plot时要添加标签label=“”
plt.legend(loc=4)
j=10
# 修改x、y刻度
y_ticks = [i for i in range(0,11)]
x_ticks = [i for i in range(0,11)]
plt.xticks(x_ticks)
plt.yticks(y_ticks)

# 添加网格显示，其中的alpha是网格的透明程度
plt.grid(True, linestyle='--', alpha=0.5)

# 添加描述信息
plt.xlabel('X',fontdict={'size':15})
plt.ylabel('Y',fontdict={'size':15})

# 4、显示图
plt.show()


