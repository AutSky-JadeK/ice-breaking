# -*- coding = utf-8 -*-
# @Time : 2024/5/21 14:59
# @Author : Lic
# @File analysis_density.py
# @Software : PyCharm
import matplotlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# 设置全局字体样式
matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['font.size'] = 36  # 设置字体大小为12

# 绘制图表的代码
df = pd.read_excel('data/gender.xlsx')

result = df.groupby('gender')['label'].apply(lambda x: (x == 'positive').sum() / len(x)).reset_index()
result.columns = ['gender', 'positive_percentage']

plt.figure(figsize=(14, 10))
sns.barplot(x='gender', y='positive_percentage', data=result, palette='plasma')
plt.xlabel('Gender')
plt.ylabel('Success Rate')
plt.ylim(0, 1)
plt.grid(True)
plt.subplots_adjust(bottom=0.2)  # 调整底部间距
plt.show()