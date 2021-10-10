import matplotlib.pyplot as plt
import matplotlib
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd


def select(infile, key1, key2, outfile):
    data = pd.read_csv(infile, encoding='gbk')
    data = data[data['Tariff'] == key1]
    data = data[data['month'] == key2]
    L_O_S = data['L_O_S'].tolist()
    Glob = data['International_mins'].tolist()
    # 截取需要用到的属性列
    data = data.iloc[:, range(5, 16)]
    data.index = data['Tariff']
    data = data.drop('Tariff', 1)
    # print(data)
    data.to_csv(outfile)
    data1 = pd.read_csv('data2.csv', encoding='gbk')
    # 去除对应话费类型的各项数值
    data1 = data1[data1['话费类型'] == key1]
    data1 = [float(data1['固定费用']), float(data1['免费时长']), float(data1['高峰时期单价']), float(data1['非高峰时期单价']),
             float(data1['周末单价']), float(data1['国际长途单价']), ]
    return np.genfromtxt(outfile, delimiter=','), data1, L_O_S, Glob


# 计算话费
def cost_(data, data1):
    cost_list = []

    m = (1, 2, 3, 4, 5)
    for i in range(1, len(data)):
        lt = 0
        cost = 0
        # lt_cost = 0
        new_data = data[i]
        for x in range(1, 4):
            lt = lt + new_data[2 * x] * new_data[2 * x + 1]
        # print("通话时间为:", lt)
        if lt > data1[1]:
            it = lt - data1[1]  # 计算需计算的话费
            for j in m:
                if j <= 3:
                    cost = cost + (new_data[2 * j] * data1[j + 1] * new_data[2 * j + 1]) * (it / lt)
                    # 计算高/低峰,以及周末的通话费用
                if j == 4:
                    cost = cost + new_data[2 * j] * data1[j + 1]
                    # 国际长途不算入免费通话,需另计算
                if j == 5:
                    cost = cost + new_data[2 * j - 1] + data1[0]
                    # 额外费用
            cost_list.append(cost)
        if lt <= data1[1]:
            lt_cost = new_data[8] * data1[5] + new_data[9] + data1[0]
            cost_list.append(lt_cost)
    print(cost_list)
    print(len(cost_list))
    return cost_list


# 把list集合数据写入csv文件
def ltcs(foo, colname, outfile):
    test = pd.DataFrame(columns=colname, data=list(zip(*foo)))  # zip(*)可变对象
    test.to_csv(outfile, encoding='gbk', index=False)


# 0均值标准化
def change(infile, outfile):
    filter_data = pd.read_csv(infile, encoding='UTF-8')
    filter_zscore_data = (filter_data - filter_data.mean(axis=0)) / (filter_data.std(axis=0))  # 0均值标准化
    filter_zscore_data.to_csv(outfile, index=False)


def Do_KMeans(infile, title):
    plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.rcParams['font.size'] = 12.0
    plt.rcParams['axes.unicode_minus'] = False
    data = pd.read_csv(infile)

    kmodel = KMeans(n_clusters=3)
    kmodel.fit(data)

    # 简单打印结果
    r1 = pd.Series(kmodel.labels_).value_counts()  # 统计各个类别的数目
    r2 = pd.DataFrame(kmodel.cluster_centers_)  # 找出聚类中心

    # 所有簇中心坐标值中最大值和最小值
    max = r2.values.max()
    min = r2.values.min()
    r = pd.concat([r2, r1], axis=1)  # 横向连接（0是纵向），得到聚类中心对应的类别下的数目
    r.columns = list(data.columns) + [u'类别数目']  # 重命名表头

    # 绘图
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, polar=True)

    center_num = r.values

    feature = ["上网时长", "月平均消费", "国际通话时长"]
    N = len(feature)

    for i, v in enumerate(center_num):
        # 设置雷达图的角度，用于平分切开一个圆面
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
        # 为了使雷达图一圈封闭起来，需要下面的步骤
        center = np.concatenate((v[:-1], [v[0]]))
        print(center)
        angles = np.concatenate((angles, [angles[0]]))
        print(angles)
        feature1 = np.concatenate((feature, [feature[0]]))
        # 绘制折线图
        ax.plot(angles, center, 'o-', linewidth=2, label="第%d簇人群,%d人" % (i + 1, v[-1]))
        # 填充颜色
        ax.fill(angles, center, alpha=0.25)
        # 添加每个特征的标签
        ax.set_thetagrids(angles * 180 / np.pi, feature1, fontsize=15)
        # 设置雷达图的范围
        ax.set_ylim(min - 0.1, max + 0.1)
        # 添加标题
        plt.title(title, fontsize=20)
        # 添加网格线
        ax.grid(True)
        # 设置图例
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), ncol=1, fancybox=True, shadow=True)
    # 显示图形
    plt.show()


def All_show(infile, key, outfile, outfile1):
    list_P1 = []
    list1 = []
    P_Glob = []
    for i in range(1, 7):
        data, data1, L_O_S, Glob = select(infile, key, i, outfile)
        list = cost_(data, data1)
        if i == 1:
            list1.append(L_O_S)
        for j in range(len(list)):
            if i == 1:
                list_P1.append(list[j] / 6)
                P_Glob.append(Glob[j] / 6)
            else:
                list_P1[j] = list_P1[j] + list[j] / 6
                P_Glob[j] = P_Glob[j] + Glob[j] / 6
    list1.append(list_P1)
    list1.append(P_Glob)
    name_list1 = ['L_O_S', 'avg-cost', 'International_mins']
    ltcs(list1, name_list1, outfile1)


def density_plot(data, k):  # 自定义作图函数
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    p = data.plot(kind='kde',
                  linewidth=2,
                  subplots=True,
                  sharex=False,
                  figsize=(10, 15))
    [p[i].set_ylabel(u'密度', fontproperties='SimHei') for i in range(k)]
    plt.legend()
    return plt


def Pei(list):
    new_list = [0, 0, 0, 0, ]
    for i in range(len(list)):
        if 10 < int(list[i]) & int(list[i]) <= 20:
            new_list[0] = new_list[0] + 1
        if 20 < int(list[i]) & int(list[i]) <= 40:
            new_list[1] = new_list[1] + 1
        if 40 < int(list[i]) & int(list[i]) <= 60:
            new_list[2] = new_list[2] + 1
        if int(list[i]) > 60:
            new_list[3] = new_list[3] + 1
    for j in range(len(new_list)):
        new_list[j] = new_list[j] / len(list)
    print(new_list)
    lables = ['年龄为10-20', '年龄为20-40', '年龄为40-60', '年龄为60以上']
    explode = (0, 0.01, 0, 0)
    plt.pie(new_list, explode, labels=lables, autopct='%1.1f%%', shadow=True, startangle=0)
    plt.title('年龄分布饼状图')
    plt.show()



