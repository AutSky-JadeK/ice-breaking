# -*- coding = utf-8 -*-
# @Time : 2024/3/31 18:33
# @Author : Lic
# @File demo.py
# @Software : PyCharm

import time
import random
from selenium import webdriver
from reply_by_chat import reply_by_chatgpt
# 把content用reply_by_chatgpt生成即可（参数post指的是帖主发的帖子，即被回复的内容）

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        return [line.strip() for line in lines]

def reply_to_weibo(contents, urls):
    path = 'D:/chromedriver-win64/chromedriver.exe'
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path=path, options=chrome_options)
    driver.maximize_window()

    print('# get打开微博主页')

    url = 'https://passport.weibo.com/sso/signin?entry=miniblog&source=miniblog&url='
    driver.get(url)  # get打开微博主页
    time.sleep(5)  # 页面加载完全
    time.sleep(10)

    for content, weibo_url in zip(contents, urls):
        driver.get(weibo_url)
        time.sleep(10)
        time.sleep(5)
        comment_input = driver.find_element_by_xpath('//*[@class="wbpro-form focus Form_wbproform_1F8KL"]/textarea')
        comment_input.send_keys(content)

        # 定位发布按钮，并点击发布评论
        comment_button = driver.find_element_by_xpath('//*[@class="wbpro-form focus Form_wbproform_1F8KL"]/parent::*/parent::*/div[3]/div/button')
        comment_button.click()
        print("评论成功！")

        time.sleep(5)  # 等待评论完成

    driver.close()

def main():
    # 读取评论内容
    contents = read_file('data/comments.txt')

    # 读取URL列表
    urls = read_file('data/urls.txt')

    # 调用函数评论
    reply_to_weibo(contents, urls)

if __name__ == "__main__":
    main()
