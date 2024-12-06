import json
from bs4 import BeautifulSoup

# 读取HTML文件
with open('index.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# 解析HTML文件
soup = BeautifulSoup(html_content, 'html.parser')

# 读取JSON文件
with open('final_ps.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 函数：提取翻译内容
def extract_translations(soup):
    translations = {}
    users = soup.find_all(class_='user')
    for user in users:
        user_id = user.find(class_='user-header').get_text().split()[1]
        user_details = user.find(class_='user-details')
        posts = user_details.find_all(class_='post')
        translations[user_id] = []
        for post in posts:
            post_text = post.find(class_='post-text').get_text()
            post_translation = post.find(class_='translation').get_text().replace('Translation: ', '').strip()
            comments = post.find_all(class_='comment')
            post_comments = []
            for comment in comments:
                comment_text = comment.get_text().split(':', 1)[1].strip()
                comment_translation = comment.find(class_='translation').get_text().replace('Translation: ', '').strip()
                post_comments.append({
                    'text': comment_text,
                    'text_en': comment_translation
                })
            translations[user_id].append({
                'text': post_text,
                'text_en': post_translation,
                'comments': post_comments
            })
    return translations

# 提取翻译内容
translations = extract_translations(soup)

# 更新JSON数据
for user_id, user_data in data.items():
    for i, post in enumerate(user_data['正文']):
        post['text_en'] = translations[user_id][i]['text_en']
        for j, comment in enumerate(user_data['评论'][i]):
            comment['text_en'] = translations[user_id][i]['comments'][j]['text_en']

# 输出更新后的JSON文件
with open('final_ps_direct_use.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("JSON文件已生成：final_ps_direct_use.json")