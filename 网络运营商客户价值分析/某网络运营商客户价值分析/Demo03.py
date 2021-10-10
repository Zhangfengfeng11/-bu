import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from 网络运营商客户价值分析.某网络运营商客户价值分析.Function import change, Do_KMeans

"""
数据变换——0均值标准化
统一区间长度
"""
change('total-P1.csv', 'total-AP1.csv')
change('total-P3.csv', 'total-AP3.csv')
change('total-C5.csv', 'total-AC5.csv')
change('total-C1.csv', 'total-AC1.csv')
change('total-C2.csv', 'total-AC2.csv')

"""
KMeans算法建立雷达图
"""
Do_KMeans('total-AP1.csv', "话费类型为Play 100客户群特征分析图")
Do_KMeans('total-AP3.csv', "话费类型为Play 300客户群特征分析图")
Do_KMeans('total-AC5.csv', "话费类型为CAT 50客户群特征分析图")
Do_KMeans('total-AC1.csv', "话费类型为CAT 100客户群特征分析图")
Do_KMeans('total-AC2.csv', "话费类型为CAT 200客户群特征分析图")
