# -*- coding = utf-8 -*-
# @Time : 2024/4/9 15:40
# @Author : Lic
# @File get_user.py
# @Software : PyCharm
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.support.wait import WebDriverWait

def scroll_to_bottom(driver):
    # 获取页面当前高度
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # 模拟页面滑动至底部
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 等待加载新内容
        time.sleep(3)

        # 获取新的页面高度
        new_height = driver.execute_script("return document.body.scrollHeight")

        # 如果新的页面高度和上一次相同，则说明已经到达页面底部
        if new_height == last_height:
            break

        # 更新页面高度
        last_height = new_height

path = 'D:/chromedriver-win64/chromedriver.exe'
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(executable_path=path, options=chrome_options)
driver.maximize_window()

print('# get打开微博主页')

url = 'http://weibo.com/login.php'
driver.get(url)  # get打开微博主页
time.sleep(5)  # 页面加载完全

# print('找到用户名 密码输入框')
# input_account = driver.find_element_by_id('loginname')  # 找到用户名输入框
# input_psw = driver.find_element_by_css_selector('input[type="password"]')  # 找到密码输入框
# # 输入用户名和密码
# input_account.send_keys("13227652098")
# input_psw.send_keys("05041005lyfxz")
#
# print('# 找到登录按钮')
# bt_logoin = driver.find_element_by_xpath('//div[@node-type="normal_form"]//div[@class="info_list login_btn"]/a')  # 找到登录按钮
#
# bt_logoin.click()  # 点击登录
# 等待页面加载完毕  #有的可能需要登录保护，需扫码确认下
time.sleep(10)

# 抑郁症超话
driver.get("https://weibo.com/p/100808f86f9e10c1d3bdefe430d95f95388c90/super_index")

# 美食超话
# driver.get("https://weibo.com/p/100808c8922754fd0f2ba821918f4e69a04a71/super_index")

# 旅游超话
# driver.get("https://weibo.com/p/1008080ebbd85f68911401fb897b0a97f2de91/super_index")

# 生活碎片超话
# driver.get("https://weibo.com/p/1008086cbc06663ab35242c04c106524bea8bf/super_index")
#
# # 生活超话
# driver.get("https://weibo.com/p/100808aefcbfca08c840aeb8bd72dc1c8ff7f9/super_index")


# 存储href内容的数组
user_ids = set()

# 循环获取每一页的用户ID

scroll_to_bottom(driver)

wb_info_divs = driver.find_elements(By.XPATH, '//div[@class="WB_info"]')
# 遍历所有匹配的div元素
for wb_info_div in wb_info_divs:
    # 在每个div元素下找到目标元素
    target_element = wb_info_div.find_element(By.XPATH, './a')
    # 获取href属性中的内容
    href_content = target_element.get_attribute('href')
    # 分割链接字符串，获取用户ID部分
    user_id = href_content.split('/')[-1].split('?')[0]
    # 将用户ID添加到数组中
    user_ids.add(user_id)
print("第一页：", user_ids)

time.sleep(2)
next_page_button = driver.find_element(By.XPATH, '//div[@class="W_pages"]/a')
next_page_button.click()
scroll_to_bottom(driver)
wb_info_divs2 = driver.find_elements(By.XPATH, '//div[@class="WB_info"]')
# 遍历所有匹配的div元素
for wb_info_div in wb_info_divs2:
    # 在每个div元素下找到目标元素
    target_element = wb_info_div.find_element(By.XPATH, './a')
    # 获取href属性中的内容
    href_content = target_element.get_attribute('href')
    # 分割链接字符串，获取用户ID部分
    user_id = href_content.split('/')[-1].split('?')[0]
    # 将用户ID添加到数组中
    user_ids.add(user_id)
print("第一页+第二页：", user_ids)
# 循环执行代码块n次，可根据获取id的数量改变n
for i in range(18):
    print("Iteration:", i + 1)  # Output iteration number
    # 等待2秒
    time.sleep(2)
    # 定位并点击下一页按钮
    next_page_button2 = driver.find_element(By.XPATH, '//div[@class="W_pages"]/a[2]')
    next_page_button2.click()
    # 模拟滚动到页面底部
    scroll_to_bottom(driver)
    # 定位所有符合条件的微博信息div元素
    wb_info_divs3 = driver.find_elements(By.XPATH, '//div[@class="WB_info"]')
    # 遍历所有匹配的div元素
    for wb_info_div in wb_info_divs3:
        # 在每个div元素下找到目标元素
        target_element = wb_info_div.find_element(By.XPATH, './a')
        # 获取href属性中的内容
        href_content = target_element.get_attribute('href')
        # 分割链接字符串，获取用户ID部分
        user_id = href_content.split('/')[-1].split('?')[0]
        # 将用户ID添加到集合中
        user_ids.add(user_id)

    # Output user IDs collected in this iteration
    print("User IDs collected in iteration", i + 1, ":", user_ids)

# 输出集合中的用户ID
print("用户ID集合：", user_ids)

# 关闭浏览器
driver.quit()

with open('data/depressed_ids.txt', 'w') as file:
    for user_id in user_ids:
        file.write(user_id + '\n')
