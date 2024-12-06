from openai import OpenAI

class GPT35TurboAPI:
    def __init__(self):
        self.openai = OpenAI(base_url="https://api.gptsapi.net/v1", api_key="sk-6JI7fb0e58e792c222cd33e2b99d5c810386079d448qNYjx") #replace as your own api_key
    
    def get_response(self, nm = "默认nm", post = "默认post"):
        prompt = ""
        if "Normal Person" in nm:
            prompt = """
你是一个富有同理心的好心人，下面是网友对自己情况的描述：
{{post}}

请你以一名普通人的口吻回复这位网友。
你的回复字数在140字以内，不要生成emoji。
""".strip()
        elif "Depressed Patient" in nm:
            prompt = """
你是一个富有同理心的好心人，下面是网友对自己情况的描述：
{{post}}

请你以一名抑郁症患者的口吻回复这位网友。
你的回复字数在140字以内，不要生成emoji。
""".strip()
        elif "Recovered Patient" in nm:
            prompt = """
你是一个富有同理心的好心人，下面是网友对自己情况的描述：
{{post}}

请你以一名康复的抑郁症患者的口吻回复这位网友。
你的回复字数在140字以内，不要生成emoji。
""".strip()
        elif "Psychiatrist" in nm:
            prompt = """
你是一个富有同理心的好心人，下面是网友对自己情况的描述：
{{post}}

请你以一名心理咨询师的口吻回复这位网友。
你的回复字数在140字以内，不要生成emoji。
""".strip()
        try:
            real_post = post
            response = self.openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt.replace('{{post}}', real_post)},
                ]
            )
            # 获取模型的回复内容
            reply = response.choices[0].message.content
            return reply
        except Exception as e:
            return f"Error occurred: {e}"

"""
# 示例调用
if __name__ == "__main__":
    gpt_api = GPT35TurboAPI()
    response = gpt_api.get_response()
    print("模型回复:", response)
"""

import requests
from urllib.parse import urlencode

class WeiboAPI:
    def __init__(self, access_token):
        self.base_url = 'https://api.weibo.com/2/'
        self.access_token = access_token

    def reply_to_status(self, weibo_id, comment):
        """
        回复指定微博ID的微博
        :param weibo_id: 要回复的微博ID
        :param comment: 回复内容
        :return: API响应
        """
        url = f'{self.base_url}comments/create.json'
        params = {
            'access_token': self.access_token,
            'id': weibo_id,
            'comment': comment,
            'rip': '58.247.22.62' #replace as your own real ip
        }
        response = requests.post(url, data=params)
        return response.json()

def get_chat(nm = "默认nm", post = "默认post"):
    gpt_api = GPT35TurboAPI()
    return gpt_api.get_response(nm, post)

def res_to_post(nm = "默认nm", weibo_id = 4636457585346578, comment = "默认comment"):
    access_token = ""
    if "Normal Person" in nm:
        if 'bot' in nm:
            access_token = '2.00vUC7dIfODv5E57dfe27490DMe1dB'
        else:
            access_token = '2.00zqLgNII9hs5Ce7bb059b82eGZT6D'
    elif "Depressed Patient" in nm:
        if 'bot' in nm:
            access_token = '2.00OeY_eIIPDCDC75ca52807feDNyNC'
        else:
            access_token = '2.0029yQEHo1v11Bef6da8f6a0ZBXGKB'
    elif "Recovered Patient" in nm:
        if 'bot' in nm:
            access_token = '2.00dGtf7IhxzaNDe451bb079fSN291C'
        else:
            access_token = '2.00NG4lfI7E23AC29f975d211XQgVoD'
    elif "Psychiatrist" in nm:
        if 'bot' in nm:
            access_token = '2.00mw8ReImcUDkCc86cdbfc11361pKC'
        else:
            access_token = '2.00QEgD2I0xIpTa81d358d07e0ZkySI'
    
    # 创建WeiboAPI实例
    weibo_api = WeiboAPI(access_token)
    
    # 指定要回复的微博ID和回复内容
    weibo_id = 4636457585346578
    
    # 调用回复函数
    response = weibo_api.reply_to_status(weibo_id, comment)
    
    # 输出响应结果
    return response["id"]

if __name__ == "__main__":
    res = get_chat()
    res_to_post(comment = res)