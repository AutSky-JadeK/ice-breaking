from openai import OpenAI
import os

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

def reply_by_chatgpt(post):
    api_key = "sk-7XFxuOWXwkmFaOjfA71e05C132564fCbB7820eBeB38354F9"
    api_base = "https://api.xi-ai.cn/v1"
    client = OpenAI(api_key=api_key, base_url=api_base)

    prompt = """你是一个富有同理心的好心人，下面是网友对自己情况的描述：
    {{post}}

    请你用亲切友好的语言安慰这位网友。
    """.strip()
    # try_num = 5
    # while try_num:
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt.replace('{{post}}', post)}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(e)
        # try_num -= 1
    
    return ""
        
# 读取 contents.txt 中的内容
with open('data/contents.txt', 'r', encoding='utf-8') as file:
    posts = file.readlines()

# 生成回复并输出到 comments.txt 中
with open('data/comments.txt', 'w', encoding='utf-8') as output_file:
    for post in posts:
        print(post)
        reply = reply_by_chatgpt(post.strip())
        print(reply)
        output_file.write(reply + '\n')