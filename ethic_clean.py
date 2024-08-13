import os
import shutil
import pandas as pd
import hashlib
import time
from datetime import datetime
import chardet
import json
import re

def convert_to_json(input_str):
    # 将单引号替换为双引号
    input_str = input_str.replace("'", '"')
    
    # 将布尔值替换为小写的 true 和 false
    input_str = re.sub(r'\bTrue\b', 'true', input_str)
    input_str = re.sub(r'\bFalse\b', 'false', input_str)
    
    # 将 None 替换为 null
    input_str = re.sub(r'\bNone\b', 'null', input_str)
    
    try:
        # 尝试解析 JSON
        data = json.loads(input_str)
        # 转换为格式化的 JSON 字符串
        json_str = json.dumps(data, ensure_ascii=False, indent=4)
        return json_str
    except json.JSONDecodeError as e:
        return f"JSONDecodeError: {str(e)}"

# 定义需要提取的列名的子串
COLUMN_SUBSTRINGS = [
    "用户id", "昵称", "主页", "头像", "高清头像", "user_id", "weibo_id", "url", "id", "bid",
    "头条文章url", "原始图片url", "视频url", "@用户", "评论"
]

def get_current_time_str():
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def hash_text(text):
    return f"[{hashlib.sha256(text.encode()).hexdigest()[:10]}]"

def copy_directory(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copy_directory(s, d)
        else:
            shutil.copy2(s, d)

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding']

def try_read_csv(file_path, encodings):
    for encoding in encodings:
        try:
            return pd.read_csv(file_path, encoding=encoding), encoding
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Cannot decode file {file_path} with provided encodings.")

def try_read_excel(file_path):
    return pd.read_excel(file_path)

def column_contains_substring(column_name, substrings):
    return any(substring in column_name for substring in substrings)

def extract_data_from_file(file_path, data_set):
    encodings = ['utf-8', 'gb2312', 'gbk', 'latin1']
    if file_path.endswith('.csv'):
        df, encoding = try_read_csv(file_path, encodings)
    elif file_path.endswith('.xlsx'):
        df = try_read_excel(file_path)
    else:
        return
    for column in df.columns:
        if column_contains_substring(column, COLUMN_SUBSTRINGS):
            if "评论" in column:
                for item in df[column].dropna().astype(str):
                    try:
                        comments_list = json.loads(convert_to_json(item))
                        if isinstance(comments_list, list):
                            for comment_dict in comments_list:
                                if isinstance(comment_dict, dict):
                                    if 'id' in comment_dict:
                                        data_set.add(str(comment_dict['id']))
                                    if 'user' in comment_dict:
                                        user_dict = comment_dict['user']
                                        if isinstance(user_dict, dict):
                                            if 'id' in user_dict:
                                                data_set.add(str(user_dict['id']))
                                            if 'screen_name' in user_dict:
                                                data_set.add(str(user_dict['screen_name']))
                    except json.JSONDecodeError:
                        continue
            else:
                data_set.update(df[column].astype(str).tolist())

def replace_data_in_file(file_path, data_set):
    encodings = ['utf-8', 'gb2312', 'gbk', 'latin1']
    if file_path.endswith('.csv'):
        df, encoding = try_read_csv(file_path, encodings)
    elif file_path.endswith('.xlsx'):
        df = try_read_excel(file_path)
    else:
        return
    for column in df.columns:
        if column_contains_substring(column, COLUMN_SUBSTRINGS):
            if "评论" in column:
                def replace_comment(comment):
                    try:
                        comments_list = json.loads(convert_to_json(str(comment)))
                        if isinstance(comments_list, list):
                            for comment_dict in comments_list:
                                if isinstance(comment_dict, dict):
                                    if 'id' in comment_dict and str(comment_dict['id']) in data_set:
                                        comment_dict['id'] = hash_text(str(comment_dict['id']))
                                    if 'user' in comment_dict:
                                        user_dict = comment_dict['user']
                                        if isinstance(user_dict, dict):
                                            if 'id' in user_dict and str(user_dict['id']) in data_set:
                                                user_dict['id'] = hash_text(str(user_dict['id']))
                                            if 'screen_name' in user_dict and str(user_dict['screen_name']) in data_set:
                                                user_dict['screen_name'] = hash_text(str(user_dict['screen_name']))
                        return json.dumps(comments_list, ensure_ascii=False)
                    except json.JSONDecodeError:
                        return comment
                df[column] = df[column].apply(replace_comment)
            else:
                df[column] = df[column].apply(lambda x: hash_text(str(x)) if str(x) in data_set else x)
    if file_path.endswith('.csv'):
        df.to_csv(file_path, index=False, encoding='utf-8-sig')  # 确保输出为UTF-8并带有BOM
    elif file_path.endswith('.xlsx'):
        df.to_excel(file_path, index=False)

def rename_files_and_directories(root_dir, data_set):
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        for name in filenames:
            orig_name, ext = os.path.splitext(name)
            if orig_name in data_set:
                new_name = hash_text(orig_name) + ext
                os.rename(os.path.join(dirpath, name), os.path.join(dirpath, new_name))
                print(f"Renamed file: {os.path.join(dirpath, name)} to {os.path.join(dirpath, new_name)}")
        for name in dirnames:
            if name in data_set:
                new_name = hash_text(name)
                os.rename(os.path.join(dirpath, name), os.path.join(dirpath, new_name))
                print(f"Renamed directory: {os.path.join(dirpath, name)} to {os.path.join(dirpath, new_name)}")

def extract_weibo_subdir_names(src_directory, data_set):
    weibo_dir = os.path.join(src_directory, 'weibo')
    if os.path.exists(weibo_dir) and os.path.isdir(weibo_dir):
        for dirpath, dirnames, filenames in os.walk(weibo_dir):
            for dirname in dirnames:
                data_set.add(dirname)
            for filename in filenames:
                if filename.endswith('.csv'):
                    file_basename, _ = os.path.splitext(filename)
                    data_set.add(file_basename)

def main():
    src_directory = input("请输入源目录路径: ")
    start_time_str = get_current_time_str()
    dst_directory = f"{os.path.basename(src_directory)}_{start_time_str}"
    
    # 拷贝目录
    copy_directory(src_directory, dst_directory)
    print(f"Copied directory from {src_directory} to {dst_directory}")

    # 提取数据
    data_set = set()
    # 提取 weibo 子目录下的所有子目录名
    extract_weibo_subdir_names(src_directory, data_set)
    
    for dirpath, _, filenames in os.walk(dst_directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            print(f"Extracting data from file: {file_path}")
            extract_data_from_file(file_path, data_set)
    
    # 替换数据
    for dirpath, _, filenames in os.walk(dst_directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            print(f"Replacing data in file: {file_path}")
            replace_data_in_file(file_path, data_set)
    
    # 重命名文件和目录
    rename_files_and_directories(dst_directory, data_set)

if __name__ == "__main__":
    main()