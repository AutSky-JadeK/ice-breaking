import json
import re
import pickle

# 扩充后的判断依据关键词表及其名字
criteria_keywords = {
    "确诊信息": ["诊断", "确诊", "确诊结果", "病例单", "诊断结果", "确定诊断", "诊断书"],
    "疾病类型": ["转双相", "抑郁症", "强迫症", "精神病", "焦虑症", "玉米症", "双相情感障碍",
                "躁郁症", "强迫性障碍", "精神疾病", "焦虑障碍", "双相障碍"],
    "与病有关": ["得病", "犯病", "发病", "治病", "生病", "病友", "病因", "患病", "病发", "疾病"],
    "医院检查": ["复诊", "复查", "医院检查", "检查", "回诊", "再检查"],
    "用药情况": ["吃药", "开药", "拿药", "吞药", "停药", "换药", "断药", "同款药", "分药器",
                "多少颗药", "加大药量", "服药", "用药", "药片", "药丸", "药物"],
    "药物名称": ["舍曲林", "艾司西酞普兰", "安非他酮", "盐酸帕罗西汀", "佐匹克隆", "劳拉西泮",
                "富马酸喹硫平", "盐酸舍曲林", "帕罗西汀", "安眠药", "米氮平", "碳酸锂",
                "司唑仑", "阿戈美拉汀", "抗抑郁药", "镇静药", "安定"],
    "病情恶化": ["治不好", "病情反复", "无法治愈", "反复发作", "病情加重", "病情恶化"],
    "医院相关": ["某医院", "某院区", "询问去哪里看病", "住院", "出院", "精神科", "医生", "护士",
                "专家", "咨询师", "医院", "门诊", "病房", "治疗中心", "康复中心"],
    "生活影响": ["休学", "停学", "请假", "休息"]
}

def analyze_sentence(sentence):
    results = {}
    marked_sentence = sentence
    for criterion, keywords in criteria_keywords.items():
        for keyword in keywords:
            if keyword in sentence:
                marked_sentence = re.sub(
                    keyword,
                    f"[{criterion}: {keyword}]",
                    marked_sentence
                )
                if criterion not in results:
                    results[criterion] = set()
                results[criterion].add(keyword)
    return results, marked_sentence

def process_user(user_nickname, user_speeches):
    combined_results = {}
    marked_sentences = []
    for sentence in user_speeches['正文']:
        sentence_results, marked_sentence = analyze_sentence(sentence)
        marked_sentences.append(marked_sentence)
        for criterion, keywords in sentence_results.items():
            if criterion not in combined_results:
                combined_results[criterion] = set()
            combined_results[criterion].update(keywords)
    return combined_results, marked_sentences

def main():
    input_file = 'weibo_data.jsonl'
    output_file = 'weibo_detect.txt'
    patient_file = 'patients.pickle'
    fpa = open(patient_file, 'wb')
    
    users = []
    id_to_nickname = {}
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            user_data = json.loads(line.strip())
            for user_id, speeches in user_data.items():
                users.append((user_id, speeches))
                id_to_nickname[user_id] = speeches['昵称']
    
    processed_results = []
    criteria_count = {i: 0 for i in range(10)}
    
    ps = {}
    for i, (user_id, speeches) in enumerate(users):
        print(f"Processing user {i + 1}/{len(users)}: {user_id}")
        user_results, marked_sentences = process_user(user_id, speeches)
        criteria_matched_count = len(user_results)
        if criteria_matched_count >= 2:
            ps[user_id] = user_results
        criteria_count[criteria_matched_count] += 1
        processed_results.append((user_id, user_results, marked_sentences))
    
    pickle.dump(ps, fpa)
    fpa.close()
    
    processed_results.sort(key=lambda x: len(x[1]), reverse=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for user_id, results, marked_sentences in processed_results:
            f.write(f"用户昵称: {id_to_nickname[user_id]}\n")
            f.write(f"符合的判断依据数量: {len(results)}\n")
            f.write("符合的判断依据及关键词:\n")
            for criterion, keywords in sorted(results.items()):
                f.write(f"  {criterion}: {', '.join(keywords)}\n")
            f.write("用户发言及关键词标记:\n")
            for marked_sentence in marked_sentences:
                f.write(f"  {marked_sentence}\n")
                f.write("-" * 50 + "\n")
            f.write("\n" + "="*50 + "\n\n" + "\n" + "="*50 + "\n\n" + "\n" + "="*50 + "\n\n")
        
        f.write("符合0~9条依据的用户数量统计:\n")
        for i in range(10):
            f.write(f"符合{i}条依据的用户数: {criteria_count[i]}\n")

if __name__ == "__main__":
    main()