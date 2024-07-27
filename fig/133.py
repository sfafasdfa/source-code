import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
def draw_distribution():
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    # 1、获取数据
    data = pd.read_csv("./crowd_temperature.csv",header=0)
    x = data['Longitude'].values
    y = data['Latitude'].values
    # 2、创建画布
    # figsize是长宽，dpi是dot per inch
    plt.figure(figsize=(60, 48), dpi=200)

    # 3、绘制图像
    plt.scatter(x, y)

    # 显示图例，这里显示图例的前提是plt.plot时要添加标签label=“”
    plt.legend(loc=4)
    j=10
    # 修改x、y刻度
    y_ticks = [i/(100) for i in range(4176, 4207,3)]
    x_ticks = [i/(100) for i in range(1235, 1266,3)]
    plt.xticks(x_ticks)
    plt.yticks(y_ticks)

    # 添加网格显示，其中的alpha是网格的透明程度
    plt.grid(True, linestyle='--', alpha=0.5)

    # 添加描述信息
    plt.xlabel('经度',fontdict={'size':15})
    plt.ylabel('纬度',fontdict={'size':15})

    # 4、显示图
    plt.show()

draw_distribution()
