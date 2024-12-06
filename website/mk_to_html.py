from get_score import SentimentClassifier
import pickle
import json
import re
import simplejson


def fix_json_format(json_str):
    # 使用不会出现在JSON中的字符作为中间字符
    placeholder = "§"

    # 修正错误的单反斜杠转义为双反斜杠
    json_str = json_str.replace('\\', '\\\\')

    # 将双引号替换为中间字符
    json_str = json_str.replace('"', placeholder)
    
    # 将单引号替换为双引号
    json_str = json_str.replace("'", '"')
    
    # 将中间字符替换为单引号
    json_str = json_str.replace(placeholder, "'")

    # 处理布尔值的替换，因为在JSON中布尔值是小写的 true/false
    json_str = re.sub(r'\bFalse\b', 'false', json_str)
    json_str = re.sub(r'\bTrue\b', 'true', json_str)
    
    # 处理 None 的替换，因为在JSON中是 null
    json_str = re.sub(r'\bNone\b', 'null', json_str)
    
    json_str = json_str.replace("\'“就算见不到又怎样呢，相隔万里我也能爱你” 𝒲𝒽𝓉 𝒾𝒻 𝒸𝒶𝓃\"𝓉 𝓈 𝓎𝓊,𝒶𝓃 𝓈𝓁𝓁 𝓁 𝓎𝓊 𝓉𝒽 𝒶𝓃 𝓂𝒾𝓁 𝓈 𝒶𝓌𝒶𝓎\'", "\"“就算见不到又怎样呢，相隔万里我也能爱你” 𝒲𝒽𝓉 𝒾𝒻 𝒸𝒶𝓃\'𝓉 𝓈 𝓎𝓊,𝒶𝓃 𝓈𝓁𝓁 𝓁 𝓎𝓊 𝓉𝒽 𝒶𝓃 𝓂𝒾𝓁 𝓈 𝒶𝓌𝒶𝓎\"")
    
    return json_str


classifier = SentimentClassifier()

def can_break(user_id, all_coms):
    for json_coms in all_coms:
        coms = []
        if json_coms != '':
            '''
            print(json_coms)
            print("\n\n")
            print(fix_json_format(json_coms))
            print("\n\n")
            '''
            coms = simplejson.loads(fix_json_format(json_coms))
        for com1 in coms:
            if str(com1['user']['id']) == user_id and 'reply_id' in com1.keys():
                for com2 in coms:
                    if com2['id'] == com1['reply_id'] and com2.get('follow_me', False) == False and com2.get('following', False) == False:
                        print('kaifang!')
                        return True
    return False

input_file = 'weibo_data.jsonl'

ps = {}
fpa = open('patients.pickle', 'rb')
ps = pickle.load(fpa)
fpa.close()

final_ps = {}
ff = open('final_ps.json', 'w', encoding='utf-8')

with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        user_data = json.loads(line.strip())
        user_id = list(user_data.keys())[0]
        print('now at:', user_id)
        if user_id not in ps.keys():
            continue
        can_b = can_break(user_id, user_data[user_id]['评论'])
        com_texts = []
        for json_coms in user_data[user_id]['评论']:
            coms = []
            if json_coms != '':
                coms = simplejson.loads(fix_json_format(json_coms))
            coms_t = []
            for com in coms:
                coms_t.append({'text': com['text'], 'user_id': com['user']['id'], 'nickname': com['user']['screen_name'], 'time': com['created_at'], 'id': com['id']})
            com_texts.append(coms_t)
        cris = {}
        for criterion, keywords in sorted(ps[user_id].items()):
            cris[criterion] = list(keywords)
        final_ps[user_id] = {'昵称': user_data[user_id]['昵称'], '正文': [], '评论': com_texts, '状态': cris, '开放态度': can_b}
        #if can_b:
        scores, posis = classifier.get_score(user_data[user_id]['正文'])
        ind = 0
        for text, score in zip(user_data[user_id]['正文'], scores):
            #print(score)
            good = False
            if score > 0:
                good = True
            final_ps[user_id]['正文'].append({'text': text, 'good_to_res': good, 'time': user_data[user_id]['日期'][ind], 'id': user_data[user_id]['id'][ind]})
            ind += 1

json.dump(final_ps, ff, ensure_ascii=False, indent=4)
ff.close()