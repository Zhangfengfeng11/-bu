import pandas as pd
import matplotlib.pyplot as plt

from 网络运营商客户价值分析.某网络运营商客户价值分析.Function import density_plot, Pei

"""
网路运营商客户价值分析
"""

"""1,数据特征"""
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
user_data1 = pd.read_csv('data1.csv', encoding='gbk')
user_info_data = pd.read_csv('user_info.csv', encoding='gbk')
"""
异常值探索
"""
# for i in range(len(user_info_data)):
#     for j in range(1, 4):
#         if user_info_data.iloc[i, 2 * j - 1]*user_info_data.iloc[i, 2 * j]==0.0:
#             user_info_data.iloc[i, 2 * j]=0.0
#             user_info_data.iloc[i, 2 * j - 1]=0.0
# user_info_data.to_csv('user_info.csv', index=False)
"""
合并原始数据
"""
# 数据合并1
data1 = pd.merge(user_data1, user_info_data, how='outer')
data1.to_csv('data_1-1.csv')
"""
pd.merge(df1,df2,how='outer') ##  全连接，取并集
pd.merge(df1,df2,how='left')  ### 左连接，左边取全部，右边取部分，
pd.merge(df1,df2,how='right') ###  右连接，右边取全部，左边取部分
"""
# 数据聚合:--对整个DataFrame数值求平均值,删除最后一列【month】
user_info_data = user_info_data.groupby(user_info_data['Customer_ID']).mean()
user_info_data = user_info_data.drop('month', 1)
# 数据合并2
data = pd.merge(user_data1, user_info_data, left_on='Customer_ID', right_index=True)
# 设置索引列
data.index = data['Customer_ID']
# 为什么要删除:重复
data = data.drop('Customer_ID', 1)
data.to_csv("data_1-2.csv")
print(data)
"""
寻找是否有空值
"""
explore = data.describe(percentiles=[], include='all').T
# precentiles参数指定多少分为表,T为转置
explore['null'] = len(data) - explore['count']
# 计算各属性列的空值个数
explore = explore[['null', 'max', 'min']]
# 具体探索内容
explore.columns = ['空值', '最大值', '最小值']
# 表头重命名
# print(explore)
explore.to_csv('explore.csv')  # 导出结果
# 数据探索：(mean,std,min,max,25%,50%,75%)
desc = data.describe()
print("hello",data['Age'].describe)

print(desc)
"""
 数据展示
"""
gender_cnt = pd.value_counts(data['Gender'])
print(gender_cnt)
tariff_cnt = pd.value_counts(data['Tariff'])
print(tariff_cnt)
handset_cnt = pd.value_counts(data['Handset'])
print(handset_cnt)
for col in data.columns:
    if not col in ['Gender', 'Tariff', 'Handset']:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        data[col].hist(bins=20)
        ax.set_title(col)
        # plt.show()
        plt.close()
# 探索年龄分布(饼状图)
age_data = data['Age'].tolist()
Pei(age_data)
# 根据饼状图可以看出客户大多数为青年人
# 可分析为该人群为社会工作者等日长上网通话时间较长，
# 仍有很大一部分为年龄10-20的青少年，可对该人群开通儿童套餐增加消费
# 老年人群体数量较少，可开通亲情电话套餐等

