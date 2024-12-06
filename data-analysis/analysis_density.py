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
# 读取Excel文件
df = pd.read_excel('data/density.xlsx')

# 根据密度数据将样本分进不同的区间段
df['density_range'] = pd.cut(df['density'], bins=[0, 0.05, 0.1, 0.5, 1, 1.33, 2, 4, 50])

# 计算每个密度范围中标签为 positive 的数量和总数
result = df.groupby('density_range')['label'].apply(lambda x: (x == 'positive').sum() / len(x)).reset_index()
result.columns = ['density_range', 'positive_percentage']

# 排序密度范围
result['density_range'] = result['density_range'].astype(str)
result = result.sort_values(by='density_range')

# 绘制折线图
plt.figure(figsize=(100, 100))
sns.lineplot(x='density_range', y='positive_percentage', data=result, marker='o')
plt.xlabel('Density Range')
plt.ylabel('Success Rate')
# plt.title('Success Rate by Density Range')
plt.xticks(rotation=45)  # 旋转 x 轴标签，使其更易阅读
plt.grid(True)  # 显示网格线
plt.subplots_adjust(bottom=0.3)  # 调整底部间距
plt.savefig("analysis_density.png")