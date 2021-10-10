import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

from 网络运营商客户价值分析.某网络运营商客户价值分析.Function import density_plot

data = pd.read_csv("data_1-2.csv")
data_feature = data.drop('Customer_ID',1)
data_feature = data_feature.drop('Age', 1)
data_feature = data_feature.drop('Gender', 1)
data_feature = data_feature.drop('Tariff', 1)
data_feature = data_feature.drop('Handset', 1)
data_zs = 1.0 * (data_feature - data_feature.mean()) / data_feature.std()  # 数据标准化

k = 4  # 聚类的类别
iteration = 500  # 聚类最大循环次数

model = KMeans(n_clusters=k,
               max_iter=iteration)  # 分为k类，并发数1，数值大系统卡死
model.fit(data_zs)  # 开始聚类

r1 = pd.Series(model.labels_).value_counts()  # 统计各个类别的数目
r2 = pd.DataFrame(model.cluster_centers_)  # 找出聚类中心

r = pd.concat([r2, r1], axis=1)  # 横向连接（0是纵向），得到聚类中心对应的类别下的数目
r.columns = list(data_zs.columns) + [u'class']  # 重命名表头
print(r)

# 类中心比较
# r[cols].plot(figsize=(10,10))
r2.columns = list(data_feature.columns)
r2.plot(figsize=(10, 10))
plt.show()

# 详细输出原始数据及其类别
res = pd.concat([data,
                 pd.Series(model.labels_, index=data.index)],
                axis=1)  # 详细输出每个样本对应的类别
res.columns = list(data.columns) + [u'class']  # 重命名表头
res.to_csv('result.cxv')  # 保存结果

pd.crosstab(res['Tariff'], res['class'])
pd.crosstab(res['Handset'], res['class'])
pd.crosstab(res['Gender'], res['class'])

res[[u'Age', u'class']].hist(by='class')
res[u'Age'].groupby(res['class']).mean()


"""
    看密度图的话可以看到更多的细节，但是对比效果不明显。
    pd_: 概率密度图文件名前缀
"""
pic_output = 'data'
for i in range(k):
    density_plot(data[res[u'class'] == i],k).savefig(u'%s%s.png' % (pic_output, i))
