import matplotlib.pyplot as plt


def draw_result22_for_nums_overall_user():
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.rcParams.update({'font.size': 16})
    # 1、获取数据
    x = [0, 5, 10, 15, 20]

    bar1 = [1, 2, 23, 14, 13, 3, 6]
    bar2 = [1, 2, 23, 14, 13, 3, 6]

    # 2、创建画布
    # figsize是长宽，dpi是dot per inch
    plt.figure(figsize=(8, 6), dpi=80)

    # 3、绘制图像
    plt.bar([25 * i + 50 - 4 for i in range(7)], bar1, width=8, label="label1")
    plt.bar([25 * i + 50 + 4 for i in range(7)], bar2, width=8, label="label2")

    # 修改x、y刻度
    plt.xticks([50, 75, 100, 125, 150, 175, 200])
    plt.yticks([0, 10, 20, 30])

    # 添加网格显示，其中的alpha是网格的透明程度
    plt.grid(True, linestyle='--', alpha=0.5)

    # 添加描述信息
    plt.xlabel('x轴')
    plt.ylabel('y轴')
    plt.legend(loc="upper left", fontsize=11)

    # 4、显示图
    plt.show()


def draw_result22_for_accept_ratio_overall_user():
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.rcParams.update({'font.size': 16})
    # 1、获取数据
    x = [0, 20, 40, 60, 80,100]

    rm0 = [1,0.92, 0.89, 0.91, 0.90,0.91]  
    rm1 = [1,-0.30, -0.30, -0.34, -0.34,-0.30]
    rm2 = [1,0.09,0.10,0.11,0.10,0.06]  
    rc0 = [1,1.19,1.22,1.23,1.23,1.23]
    rc1 = [1,0.53,0.46,0.43,0.42,0.42]
    rc2 = [1,0.76,0.71,0.70,0.70,0.72]
    ra0 = [1,0.85,1.22,1.56,1.82,1.97]
    ra1 = [1,-0.1,-0.14,-0.19,-0.23,-0.27]
    ra2 = [1,0.2,0.02,0.03,0.03,0.05]
    # 2、创建画布
    # figsize是长宽，dpi是dot per inch
    plt.figure(figsize=(8, 6), dpi=120)

    # 3、绘制图像
    # plt.plot(x, rm0, color='b', linestyle='--', label='type 0', marker='o')#s,+,x,.
    # plt.plot(x, rm1, color='r', linestyle='--', label='type 1', marker='*')
    # plt.plot(x, rm2, color='g', linestyle='--', label='type 2', marker='+')
    # plt.plot(x, rc0, color='b', linestyle='--', label='type 0', marker='o')#s,+,x,.
    # plt.plot(x, rc1, color='r', linestyle='--', label='type 1', marker='*')
    # plt.plot(x, rc2, color='g', linestyle='--', label='type 2', marker='+')
    #plt.plot(x, ra0, color='b', linestyle='--', label='type 0', marker='o')#s,+,x,.
    #plt.plot(x, ra1, color='r', linestyle='--', label='type 1', marker='*')
    #plt.plot(x, ra2, color='g', linestyle='--', label='type 2', marker='+')
    # 修改x、y刻度
    plt.plot(x, rm2, color='b', linestyle='--', label='MB算法', marker='o')#s,+,x,.
    plt.plot(x, rc2, color='r', linestyle='--', label='RSB算法', marker='o')#s,+,x,.
    plt.plot(x, ra2, color='g', linestyle='--', label='SSB算法', marker='o')#s,+,x,.
    plt.xticks([0, 20, 40,60,80,100])
    plt.xlim([0,100])
    plt.yticks([-1,-0.5,0,0.5,1,1.5,2,2.5])
    plt.ylim([-1,2.5])

    # 添加网格显示，其中的alpha是网格的透明程度
    plt.grid(True, linestyle='--', alpha=0.5)

    # 添加描述信息
    plt.xlabel('提交数据次数',fontdict={'size':15})
    plt.ylabel('信誉值均值',fontdict={'size':15})
    plt.legend(loc="upper left", fontsize=15)

    # 4、显示图
    plt.show()


draw_result22_for_accept_ratio_overall_user()