# -*- coding = utf-8 -*-
# @Time : 2024/4/16 15:39
# @Author : Lic
# @File best ds.py
# @Software : PyCharm
import json
import os
import csv
import re
from datetime import datetime

import pandas as pd
# 定义一个函数来替换单个字符串中的 "\"
def remove_backslash(comment):
    if isinstance(comment, str):
        return comment.replace("\\", "")
    return comment
def post_weibo_average(input_file, col):
    try:
        df = pd.read_csv(input_file)
        col_name = df.columns[col]  # 获取指定整数对应的列名
        df[col_name] = pd.to_datetime(df[col_name])  # 转换日期格式
        days = (df[col_name].max() - df[col_name].min()).days  # 计算天数差
        average_days = days / len(df)  # 计算平均发帖子时间
        return average_days
    except Exception as e:
        print("Error reading CSV file:", e)
        return None



# 定义文件夹路径
folder_path = 'weibo/'
# 定义结果存储的字典
result_dict = {}
average_days_of_users = []
id_counter = 1
# 获取当前工作目录
current_dir = os.getcwd()
# 遍历文件夹
for subdir, dirs, files in os.walk(folder_path):
    # 获取微博名称
    weibo_name = os.path.basename(subdir)
    for file in files:
        # 如果文件是CSV文件
        if file.endswith('.csv'):
            # 构建文件的绝对路径
            file_path = os.path.join(current_dir, subdir, file)
            # print(file_path)
            user_id = os.path.basename(file_path).split('.')[0]
            # print(user_id)
            average_days = post_weibo_average(file_path, 7)
            # print(average_days)
            # if average_days is not None:
            #     print(average_days)
            # 获取文件路径的上级目录名
            parent_folder_name = os.path.split(os.path.abspath(file_path))[0]
            # 获取分割后的最后一截字符串
            user_name = parent_folder_name.split('\\')[-1]
            average_days_of_user = {
                'name': user_name,
                'average_days': average_days
            }
            average_days_of_users.append(average_days_of_user)
            # print(user_name)
            file_path = os.path.join(subdir, file)
            file_name = os.path.splitext(file)[0]
            # 使用pandas读取CSV文件
            df = pd.read_csv(file_path)
            # 过滤评论值大于 0 的行
            df = df[df['评论数'] > 0]
            # 输出df的'id'、'评论数'和'评论'三列内容
            # print(df[['id', '评论数', '评论']])
            neg_lists = []
            pos_lists = []
            if not df.empty:
                rows_to_delete = []
                # 遍历 DataFrame

                for index, row in df.iterrows():
                    if row['评论数'] == 1:
                        comment = str(row['评论'])
                        pattern = r"'screen_name': '([^']+)'"
                        match = re.search(pattern, comment)
                        if match:
                            screen_name = match.group(1)
                            if screen_name == user_name:
                                rows_to_delete.append(index)

                # 删除要删除的行
                df = df.drop(rows_to_delete, axis=0)

                # 打印结果
                # print(df[['id', '评论数', '评论']])
                # 创建两个字典分别为pos_list和neg_list
                pos_list = []
                neg_list = []
                neg_count = 0
                pos_count = 0
                pattern_name = r"'screen_name': '([^']+)'"
                # x-reply-again
                pattern_text = r"'text': '([^']+)'"
                # y-reply
                pattern_reply_text = r"'reply_text': '([^']+)'"
                pattern_created_at = r"'created_at': '([^']+)'"
                pattern_y_id = r"'id': (\d+), 'screen_name'"
                reply_texts = []
                comment_user_names = []
                # 遍历 DataFrame
                for index, row in df.iterrows():
                    comment = str(row['评论'])
                    date_str = row['日期']
                    bid = row['bid']
                    datetime_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
                    formatted_date = datetime_obj.strftime('%Y-%m-%d')
                    # print(formatted_date)
                    match_name = re.search(pattern_name, comment)
                    match_text = re.search(pattern_text, comment)
                    match_reply_text = re.search(pattern_reply_text, comment)
                    match_created_at = re.search(pattern_created_at, comment)
                    match_y_id = re.search(pattern_y_id, comment)
                    get_weibo_time_str = "2024-04-20"
                    get_weibo_time = datetime.strptime(get_weibo_time_str, "%Y-%m-%d").date()
                    if row['评论数'] == 1:
                        if match_name:
                            screen_name = match_name.group(1)
                            if screen_name != user_name:
                                if match_text:
                                    text = match_text.group(1)
                                    if match_created_at and match_y_id:
                                        created_at = match_created_at.group(1)
                                        y_id = match_y_id.group(1)
                                        if "前" not in created_at and len(created_at) == 5:
                                            created_at = "2024-" + created_at
                                            created_at = datetime.strptime(created_at, "%Y-%m-%d").date()
                                            time_diff = get_weibo_time - created_at
                                            days_diff = time_diff.days
                                            average_days_of_users_dic = {item['name']: item['average_days'] for item in average_days_of_users}
                                            # print(average_days_of_users_dic)
                                            average_days = average_days_of_users_dic.get(user_name)
                                            # print(average_days)

                                            entry = {
                                                'id': neg_count,
                                                'user_id': user_id,
                                                'weibo_id': bid,
                                                'y_id': y_id,
                                                'X_history_density': average_days,
                                                'formatted_date': formatted_date,
                                                'X_post': row['正文'],
                                                'Y_reply': text
                                            }
                                            neg_count += 1
                                            neg_list.append(entry)
                    if row['评论数'] >= 2:
                        if match_name and match_text and match_reply_text:
                            screen_name = match_name.group(1)
                            text = match_text.group(1)
                            clean_text = re.sub(r'回复@[^:]+:', '', text)
                            reply_text = match_reply_text.group(1)
                            reply_texts.append(reply_text)
                            if (screen_name == user_name) and ('回复@' in text):
                                if match_created_at and match_y_id:
                                    created_at = match_created_at.group(1)
                                    y_id = match_y_id.group(1)
                                    # print(created_at)
                                    if "前" not in created_at and len(created_at) == 5:
                                        created_at = "2024-" + created_at
                                        created_at = datetime.strptime(created_at, "%Y-%m-%d").date()
                                        time_diff = get_weibo_time - created_at
                                        days_diff = time_diff.days
                                        average_days_of_users_dic = {item['name']: item['average_days'] for
                                                                     item in average_days_of_users}
                                        # print(average_days_of_users_dic)
                                        average_days = average_days_of_users_dic.get(user_name)
                                        # print(average_days)

                                        entry = {
                                            'id': pos_count,
                                            'user_id': user_id,
                                            'weibo_id': bid,
                                            'y_id': y_id,
                                            'X_history_density': average_days,
                                            'formatted_date': formatted_date,
                                            'X_post': row['正文'],
                                            'Y_reply': reply_text,
                                            'X_reply_again': clean_text
                                        }
                                        pos_count += 1
                                        pos_list.append(entry)
                            if (screen_name != user_name) and ('回复@' not in text):
                                if match_text and not match_reply_text:
                                    if text not in reply_texts:
                                        if match_text:
                                            if match_created_at and match_y_id:
                                                created_at = match_created_at.group(1)
                                                y_id = match_y_id.group(1)
                                                # print(created_at)
                                                if "前" not in created_at and len(created_at) == 5:
                                                    created_at = "2024-" + created_at
                                                    created_at = datetime.strptime(created_at, "%Y-%m-%d").date()
                                                    time_diff = get_weibo_time - created_at
                                                    days_diff = time_diff.days
                                                    average_days_of_users_dic = {item['name']: item['average_days'] for
                                                                                 item in average_days_of_users}
                                                    # print(average_days_of_users_dic)
                                                    average_days = average_days_of_users_dic.get(user_name)
                                                    # print(average_days)

                                                    entry = {
                                                        'id': neg_count,
                                                        'user_id': user_id,
                                                        'weibo_id': bid,
                                                        'y_id': y_id,
                                                        'X_history_density': average_days,
                                                        'formatted_date': formatted_date,
                                                        'X_post': row['正文'],
                                                        'Y_reply': text
                                                    }
                                                    neg_count += 1
                                                    neg_list.append(entry)

                print(neg_list)
                print(pos_list)
