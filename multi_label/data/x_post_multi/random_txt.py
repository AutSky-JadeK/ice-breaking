# -*- coding = utf-8 -*-
# @Time : 2024/4/17 9:09
# @Author : Lic
# @File random_txt.py
# @Software : PyCharm
import random

# 读取txt文件内容并存储在列表中
with open('all.txt', 'r', encoding='utf-8') as file:
    lines = [line.strip() for line in file.readlines()]

# 打乱行的顺序
random.shuffle(lines)

# 将打乱后的内容写回到txt文件中
with open('shuffled_all.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(lines) + '\n')

print("文件行顺序已打乱")