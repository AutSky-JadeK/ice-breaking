# -*- coding = utf-8 -*-
# @Time : 2024/4/29 22:15
# @Author : Lic
# @File ds_data_process.py
# @Software : PyCharm
import re

# 读取data.txt文件
with open('data/positive.txt', 'r', encoding='utf-8') as file:
    data = [line.strip() for line in file.readlines() if line.strip()]  # 跳过空行并去除首尾空白字符

# 创建一个新的txt文件用于写入处理后的数据
with open('output/output.txt', 'w', encoding='utf-8') as new_file:
    for i in range(len(data)):
        try:
            posts = eval(data[i])  # 将字符串转换为字典列表
            X_history = ''
            for j in range(len(posts) - 1, -1, -1):  # Iterate over posts in reverse order
                if j != len(posts) - 1:  # If it's not the last post
                    X_history += posts[j + 1]['X_post'].strip().replace('\n', '') + ";"  # Append the next post to history
                user_id = posts[j]['user_id']
                weibo_id = posts[j]['weibo_id']
                X_history_density = posts[j]['X_history_density']
                date = posts[j]['formatted_date']
                X_post = posts[j]['X_post'].strip().replace('\n', '')
                Y_reply = posts[j]['Y_reply'].strip().replace('\n', '')
                new_file.write(f"positive\t{user_id}\t{weibo_id}\t{X_history_density}\t{date}\t{X_history}\t{X_post}\t{Y_reply}\n")
        except Exception as e:
            print(f"Error processing line {i + 1}: {e}")  # 打印出错行的信息