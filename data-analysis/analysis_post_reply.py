# -*- coding = utf-8 -*-
# @Time : 2024/5/21 14:59
# @Author : Lic
# @File analysis_density.py
# @Software : PyCharm
import textwrap

import matplotlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# 设置全局字体样式
matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['font.size'] = 36  # 设置字体大小为12

# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False

# 读取第二个Excel数据
df = pd.read_excel('data/Y_Reply_multi_en.xlsx')

# 将type列中的多个类型分割成单独的行
df['type'] = df['type'].str.split(',')

# 创建一个新的DataFrame来保存拆分后的数据
new_df = pd.DataFrame(columns=['type', 'label'])

# 遍历原始DataFrame，对每个条目中的多个类别进行拆分
for index, row in df.iterrows():
    types = row['type']
    for t in types:
        new_df = new_df.append({'type': t.strip(), 'label': row['label']}, ignore_index=True)

# 计算每个类型类别中标签为 positive 占该类别所有数量的比例
result = new_df.groupby('type')['label'].apply(lambda x: (x == 'positive').sum() / len(x)).reset_index()
result.columns = ['type', 'positive_percentage']

result['type'] = result['type'].apply(lambda x: '\n'.join(textwrap.wrap(x, width=12)))  # 每行最多显示10个字符

# 绘制柱状图并调整图形大小
plt.figure(figsize=(40, 60))
sns.barplot(x='type', y='positive_percentage', data=result, palette='plasma')

plt.xlabel('Category')
plt.ylabel('Proportion')
plt.ylim(0, 1)  # 设置y轴范围为0到1，显示比例
plt.grid(axis='y')  # 显示水平网格线
plt.subplots_adjust(bottom=0.3)  # 调整底部间距
plt.xticks(rotation=0)  # 旋转x轴标签
plt.savefig("analysis_post_reply.png")