import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
user_info_data = pd.read_csv('user_info.csv', encoding='gbk')
print(int(user_info_data.iloc[0,2]))
for i in range(len(user_info_data)):
    for j in range(1, 4):
        if user_info_data.iloc[i, 2 * j - 1]*user_info_data.iloc[i, 2 * j]==0.0:
            user_info_data.iloc[i, 2 * j]=0.0
            user_info_data.iloc[i, 2 * j - 1]=0.0
user_info_data.to_csv('new_user_info.csv', index=False)