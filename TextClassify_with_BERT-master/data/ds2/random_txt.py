# -*- coding = utf-8 -*-
# @Time : 2024/4/17 9:09
# @Author : Lic
# @File random_txt.py
# @Software : PyCharm
import random

def shuffle_lines_except_first(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()  # 读取所有行到一个列表中

    first_line = lines[0]  # 保存第一行
    remaining_lines = lines[1:]  # 除去第一行的其余行

    random.shuffle(remaining_lines)  # 随机打乱除去第一行的其余行

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(first_line)  # 写入第一行
        file.writelines(remaining_lines)  # 将打乱后的其余行写入到输出文件

# 使用示例
input_path = 'all.txt'  # 指定输入文件路径
output_path = 'shuffled_all.txt'  # 指定输出文件路径
shuffle_lines_except_first(input_path, output_path)