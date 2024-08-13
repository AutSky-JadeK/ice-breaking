# -*- coding = utf-8 -*-
# @Time : 2024/5/2 15:18
# @Author : Lic
# @File delete.py
# @Software : PyCharm
# 打开旧文件和新文件
with open('tr.txt', 'r', encoding='utf-8') as old_file, open('new_tr.txt', 'w', encoding='utf-8') as new_file:
    # 逐行读取旧文件
    for line in old_file:
        # 查找X_post的位置
        index = line.find('X_post')
        if index != -1:
            # 写入X_post和之后的字符串
            new_file.write(line[index:])