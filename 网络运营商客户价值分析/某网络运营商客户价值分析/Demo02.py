import csv

import pandas as pd
import matplotlib.pyplot as plt

from 网络运营商客户价值分析.某网络运营商客户价值分析.Function import select, cost_, ltcs, All_show

"""
对表data_1-1.csv进行数据处理
"""

"""
使用data_1-1.csv
1,搜寻五种话费类型对应月份的数据,联立为新表,
    例如:CAT 50月份为1的数据命名为C51.csv,
    一共有30个表
2,选定话费类型计算其每个月份的话费,并将其求平均数,最后作为消费标准
    一共5个列表
3,选定话费类型,以客户做表关联,找到同一客户的上网时间,以及国外通话时间
    将月平均消费,上网时间,国外通话时间三类数据写入csv中
    一共五个表,对应每种话费类型
4,对每个表进行kmeans分类,做出雷达图根据图表强弱关系分为重要客户,可发展客户,一般客户.
"""

All_show('data_1-1.csv', 'Play 100', 'P100.csv', 'total-P1.csv')
All_show('data_1-1.csv', 'Play 300', 'P300.csv', 'total-P3.csv')
All_show('data_1-1.csv', 'CAT 50', 'C50.csv', 'total-C5.csv')
All_show('data_1-1.csv', 'CAT 100', 'C100.csv', 'total-C1.csv')
All_show('data_1-1.csv', 'CAT 200', 'C200.csv', 'total-C2.csv')

