import os
import pandas as pd
import json
import random
import csv

userid_to_nickname = {}
with open('weibo_no_follow/users.csv', 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        nickname = row['昵称'].strip()
        user_id = row['用户id'].strip()
        userid_to_nickname[user_id] = nickname

# 需要过滤的关键词
filter_keywords = {"抑郁症", "焦虑症", "精神分裂症", "抑郁症超话", "抑郁症患者", "抑郁", "走出抑郁症", "抑郁症重度患者", "双相情感障碍"}

def extract_text_from_csv(directory):
    data = {}
    
    # 遍历目录中的每个子目录
    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)
        
        if os.path.isdir(subdir_path):
            # 查找子目录中的CSV文件
            for file in os.listdir(subdir_path):
                if file.endswith('.csv'):
                    file_path = os.path.join(subdir_path, file)
                    
                    # 读取CSV文件
                    df = pd.read_csv(file_path)
                    
                    text_list, json_data = [], []
                    # 提取“正文”列的内容
                    if '正文' in df.columns:
                        df['正文'] = df['正文'].fillna('')
                        text_list = df['正文'].tolist()
                        cleaned_text_list = []
                        for text in text_list:
                            segments = text.split('\n')
                            cleaned_segments = [seg for seg in segments if seg not in filter_keywords]
                            cleaned_content = '\n'.join(cleaned_segments)
                            cleaned_text_list.append(cleaned_content)
                    if '日期' in df.columns:
                        df['日期'] = df['日期'].fillna('')
                        json_data_time = df['日期'].tolist()
                    if '评论' in df.columns:
                        df['评论'] = df['评论'].fillna('')
                        json_data = df['评论'].tolist()
                    if 'id' in df.columns:
                        df['id'] = df['id'].fillna('')
                        json_data_id = df['id'].tolist()
                    '''
                    if subdir == '7238428936':
                        for text in cleaned_text_list:
                            print(text)
                            print('\n\n')
                        for text in json_data:
                            print(text)
                            print('\n\n')
                    '''
                    
                    if len(cleaned_text_list) != len(json_data):
                        print(len(cleaned_text_list), len(json_data))
                    data[subdir] = {'正文': cleaned_text_list, '日期': json_data_time, '评论': json_data, '昵称': userid_to_nickname[subdir], "id": json_data_id}
                    break  # 假设每个子目录只有一个CSV文件
    
    return data

def write_jsonl(data, output_file):
    # 打乱顺序
    items = list(data.items())
    random.shuffle(items)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for key, value in items:
            json_record = json.dumps({key: value}, ensure_ascii=False)
            f.write(json_record + '\n')

if __name__ == "__main__":
    directory = 'weibo_no_follow'  # 替换为你的目录路径
    output_file = 'weibo_data.jsonl'
    
    data = extract_text_from_csv(directory)
    write_jsonl(data, output_file)