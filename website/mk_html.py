import json
#from googletrans import Translator
from jinja2 import Template
from dateutil import parser
import re

today = "09-03"
yesday = "09-02"

# 设置开关
USE_DIRECT_JSON = True

# 选择要读入的文件
input_file = 'final_ps_direct_use.json' if USE_DIRECT_JSON else 'final_ps.json'

# 初始化翻译器
#translator = Translator()

# 读取JSON文件
with open('final_ps.json', 'r', encoding='utf-8') as file:
    original_data = json.load(file)

# 如果使用直接使用的JSON文件，额外读取
if USE_DIRECT_JSON:
    with open('final_ps_direct_use.json', 'r', encoding='utf-8') as file:
        direct_data = json.load(file)

# 读取状态映射文件
with open('status_mapping.json', 'r', encoding='utf-8') as file:
    status_mapping = json.load(file)

# 函数：翻译文本，带有错误处理和重试机制
def translate_text(text, src='zh-cn', dest='en'):
    try:
        #translation = translator.translate(text, src=src, dest=dest)
        #return translation.text
        return ""
    except Exception as e:
        print(f"Error translating text: {text}. Error: {e}")
        # 如果翻译失败，返回原文本
        return text

# 函数：格式化发帖时间
def format_post_time(time_str):
    dt = parser.isoparse(time_str)
    return dt.strftime("%B %d, %Y at %I:%M %p")

# 将转义字符替换为对应的可视化表示
def escape_text(text):
    return text.replace('\n', '\\n').replace('\t', '\\t')

# 函数：高亮关键词并添加英文注释
def highlight_keywords(text, criteria_keywords, status_mapping):
    for category, keywords in criteria_keywords.items():
        for keyword in keywords:
            if keyword in text:
                text = text.replace(keyword, f"<span class='highlight'>{keyword} ({status_mapping[keyword]})</span>")
    return text

# 预处理数据
data = direct_data if USE_DIRECT_JSON else original_data

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

for user_id, user_info in data.items():
    combined_posts = []
    for i, (post, comments) in enumerate(zip(user_info["正文"], user_info["评论"])):
        if USE_DIRECT_JSON:
            # 直接使用已经翻译好的内容和原始时间
            post_text_en = escape_text(post["text_en"])
            post_time = original_data[user_id]["正文"][i]["time"]
        else:
            # 进行翻译
            post_text_en = escape_text(translate_text(post["text"]))
            post_time = post["time"]
        
        # 高亮关键词
        post_text = highlight_keywords(escape_text(post["text"]), criteria_keywords, status_mapping)
        
        if post_text_en.endswith("(值得回复)"):
            post_text_en = post_text_en[:-len("(值得回复)")] + "<span class='worth-reply'>(Worth Reply)</span>"
        
        translated_comments = []
        for j, comment in enumerate(comments):
            if USE_DIRECT_JSON:
                comment_text_en = escape_text(comment["text_en"])
                comment_time = original_data[user_id]["评论"][i][j]["time"]
            else:
                comment_text_en = escape_text(translate_text(comment["text"]))
                comment_time = comment["time"]
            
            # 高亮关键词
            comment_text = highlight_keywords(escape_text(comment["text"]), criteria_keywords, status_mapping)
            
            comment_id = original_data[user_id]["评论"][i][j]["id"]
            
            if "前" in comment_time or "刚" in comment_time:
                comment_time = today
            elif "昨" in comment_time:
                comment_time = yesday
            
            translated_comments.append({
                "text": comment_text,
                "text_en": comment_text_en,
                "time": comment_time,
                "user_id": comment["user_id"],
                "nickname": comment["nickname"],
                "id": comment_id
            })
        combined_posts.append({
            "text": post_text,
            "text_en": post_text_en,
            "time": format_post_time(post_time),
            "good_to_res": post["good_to_res"] if not USE_DIRECT_JSON else None,
            "comments": translated_comments,
            "id": original_data[user_id]["正文"][i]["id"]
        })
    user_info["combined_posts"] = combined_posts

# 替换状态中的内容
for user_id, user_info in data.items():
    translated_status = {}
    for key, values in user_info["状态"].items():
        translated_key = status_mapping.get(key, key)
        translated_values = [status_mapping.get(value, value) for value in values]
        translated_status[translated_key] = translated_values
    user_info["状态"] = translated_status

# HTML模板
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weibo Data Analysis for Academic Research on Depression</title>
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            margin: 20px;
            background-color: #f9f9f9;
            color: #333;
            line-height: 1.6;
        }
        h1 {
            text-align: center;
            color: #444;
            margin-bottom: 20px;
            font-size: 2.5em;
            letter-spacing: 1px;
        }
        .update-time {
            text-align: center;
            color: #777;
            margin-bottom: 40px;
            font-size: 1.2em;
        }
        .user {
            margin-bottom: 20px;
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        .user:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        .user-header {
            font-weight: bold;
            cursor: pointer;
            margin-bottom: 10px;
            font-size: 1.5em;
            color: #0056b3;
        }
        .user-details {
            display: none;
            margin-top: 10px;
        }
        .post {
            margin-bottom: 15px;
            padding-top: 10px;
        }
        .comments {
            margin-left: 20px;
        }
        .comment {
            margin-bottom: 10px;
        }
        .translation {
            font-style: italic;
            color: grey;
        }
        .time {
            color: grey;
            font-size: small;
        }
        .id {
            color: brown;
            font-size: small;
        }
        .status, .open-attitude {
            margin-top: 10px;
            margin-bottom: 10px;
        }
        .status span, .open-attitude span {
            display: block;
            margin-top: 5px;
            color: #4B0082; /* Indigo color */
            font-weight: bold;
        }
        .status strong, .open-attitude strong {
            color: #dc3545;
            font-size: 1.2em;
        }
        .ice-break-container {
            margin-top: 10px;
            margin-bottom: 10px;
        }
        .ice-break-button {
            margin-top: 10px;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            background-color: #0056b3;
            color: #fff;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .ice-break-button:hover {
            background-color: #003d80;
        }
        .identity-buttons {
            display: none;
            flex-wrap: wrap;
            margin-top: 10px;
        }
        .identity-button {
            padding: 10px 20px;
            margin: 5px;
            border: none;
            border-radius: 5px;
            background-color: #007BFF;
            color: #fff;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .identity-button:hover {
            background-color: #0056b3;
        }
        .identity-button.clicked {
            background-color: #FF4500; /* High contrast color */
        }
        .worth-reply {
            color: #FF4500;
            font-weight: bold;
            font-family: 'Courier New', Courier, monospace;
        }
        .highlight {
            background-color: yellow;
            font-weight: bold;
        }
        .search-container {
            text-align: center;
            margin-bottom: 20px;
        }
        .search-box {
            padding: 10px;
            width: 300px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-right: 10px;
        }
        .search-button {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            background-color: #0056b3;
            color: #fff;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .search-button:hover {
            background-color: #003d80;
        }
        .modal {
            display: none;
            position: fixed;
            z-index: 1;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.4);
            justify-content: center;
            align-items: center;
        }
        .modal-content {
            background-color: #fefefe;
            margin: auto;
            padding: 20px;
            border: 1px solid #888;
            width: 80%;
            max-width: 800px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }
        .modal-close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        }
        .modal-close:hover,
        .modal-close:focus {
            color: #000;
            text-decoration: none;
            cursor: pointer;
        }
        .try-comment-modal {
            display: none;
            position: fixed;
            z-index: 1;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.4);
            justify-content: center;
            align-items: center;
        }
        .try-comment-modal-content {
            background-color: #fefefe;
            margin: auto;
            padding: 20px;
            border: 1px solid #888;
            width: 80%;
            max-width: 800px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }
        .try-comment-modal-close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        }
        .try-comment-modal-close:hover,
        .try-comment-modal-close:focus {
            color: #000;
            text-decoration: none;
            cursor: pointer;
        }
        .try-comment-content {
            max-height: 300px;
            overflow-y: auto;
        }
        .reply-button {
            border: 1px dashed #A52A2A; /* 设置边框宽度为1像素，样式为虚线，颜色为棕色 */
            background: transparent;
            cursor: pointer;
            margin-right: 10px;
            transition: transform 0.3s; /* 添加过渡效果，使缩放更加平滑 */
        }
        .reply-button:hover {
            transform: scale(1.4); /* 鼠标悬停时缩放到原来的1.4倍 */
            border-width: 3px; /* 鼠标悬停时将边框宽度变为3像素 */
            border-style: solid; /* 鼠标悬停时将边框样式变为实线 */
            border-color: orange; /* 鼠标悬停时将边框颜色变为橙色 */
        }
        .reply-button img {
            width: 24px;
            height: 24px;
        }
    </style>
    <script>
        var clickedButtons = [];

        function toggleDetails(userId) {
            var details = document.getElementById('details-' + userId);
            if (details.style.display === 'none' || details.style.display === '') {
                details.style.display = 'block';
            } else {
                details.style.display = 'none';
            }
        }

        function toggleIceBreakButtons(postId) {
            var buttons = document.getElementById('ice-break-buttons-' + postId);
            if (buttons.style.display === 'none' || buttons.style.display === '') {
                buttons.style.display = 'flex';
            } else {
                buttons.style.display = 'none';
            }
        }

        async function handleIdentityButtonClick(button, postId, postContent) {
            button.classList.add('clicked');
            var buttonText = button.textContent;
            try {
                // 调用test_api的get_chat函数
                const response = await fetch('/get_reply', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        identity: buttonText,
                        post_content: postContent
                    }),
                });
                const data = await response.json();
                const defaultReply = data.default_reply;

                // 更新弹窗的内容
                var modal = document.getElementById('reply-modal');
                modal.querySelector('.default-reply').textContent = 'default_reply: ' + defaultReply;
                modal.querySelector('.my-reply').value = '';
                modal.querySelector('.response-button').setAttribute('data-post-id', postId);
                modal.querySelector('.response-button').setAttribute('data-identity', buttonText);
                modal.querySelector('.response-button').setAttribute('data-default-reply', defaultReply);

                modal.style.display = 'flex';
            } catch (error) {
                alert('Error occurred while getting the reply.');
            }
        }

        async function sendResponse(button) {
            var postId = button.getAttribute('data-post-id');
            var identity = button.getAttribute('data-identity');
            var defaultReply = button.getAttribute('data-default-reply');
            var myReply = document.querySelector('.my-reply').value;

            var finalReply = myReply || defaultReply;

            try {
                // 调用test_api的res_to_post函数
                const response = await fetch('/send_response', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        identity: identity,
                        post_id: postId,
                        reply_content: finalReply
                    }),
                });
                const data = await response.json();
                if (data.status === 'success') {
                    alert('Reply sent!');
                } else {
                    alert('Error sending the reply.');
                }
            } catch (error) {
                alert('Error occurred while sending the reply.');
            }
        }
        
        function closeReplyModal() {
            document.getElementById('reply-modal').style.display = 'none';
        }

        function performSearch() {
            var keyword = document.getElementById('keyword-searcher').value.toLowerCase();
            if (keyword) {
                var data = {{ data | tojson | safe }};
                var resultsContainer = document.getElementById('modal-results-container');
                resultsContainer.innerHTML = ''; // 清空之前的搜索结果

                var postsFound = false;
                var commentsFound = false;

                for (var userId in data) {
                    var user = data[userId];

                    user.combined_posts.forEach(function(post) {
                        if (post.text.toLowerCase().includes(keyword) || post.text_en.toLowerCase().includes(keyword)) {
                            if (!postsFound) {
                                var postsHeader = document.createElement('h2');
                                postsHeader.textContent = 'Posts';
                                resultsContainer.appendChild(postsHeader);
                                postsFound = true;
                            }
                            var postElement = document.createElement('div');
                            postElement.className = 'post';
                            postElement.innerHTML = `
                                <strong>${user["昵称"]} (${userId})</strong>
                                <div>${highlightKeywords(post.text)}</div>
                                <div class="time">Time: ${post.time}</div>
                                <div class="translation">Translation: ${post.text_en}</div>
                                <div class="id">
                                    Post ID: ${post.id}
                                    <br>
                                    <a href="https://weibo.com/detail/${post.id}" target="_blank">Visit Post</a>
                                </div>
                            `;
                            resultsContainer.appendChild(postElement);
                        }

                        post.comments.forEach(function(comment) {
                            if (comment.text.toLowerCase().includes(keyword) || comment.text_en.toLowerCase().includes(keyword)) {
                                if (!commentsFound) {
                                    var commentsHeader = document.createElement('h2');
                                    commentsHeader.textContent = 'Comments';
                                    resultsContainer.appendChild(commentsHeader);
                                    commentsFound = true;
                                }
                                var commentElement = document.createElement('div');
                                commentElement.className = 'comment';
                                commentElement.innerHTML = `
                                    <strong>${comment.nickname} (${comment.user_id}):</strong>
                                    <div>${highlightKeywords(comment.text)}</div>
                                    <div class="time">Time: ${comment.time}</div>
                                    <div class="translation">Translation: ${comment.text_en}</div>
                                `;
                                resultsContainer.appendChild(commentElement);
                            }
                        });
                    });
                }

                if (!postsFound && !commentsFound) {
                    resultsContainer.innerHTML = '<p>No results found for "' + keyword + '".</p>';
                }

                // 显示弹窗
                document.getElementById('search-modal').style.display = 'flex';
            }
        }

        function performIdSearch() {
            var id = document.getElementById('id-searcher').value.toLowerCase();
            if (id) {
                var data = {{ data | tojson | safe }};
                var resultsContainer = document.getElementById('modal-results-container');
                resultsContainer.innerHTML = ''; // 清空之前的搜索结果

                var postFound = false;
                var commentFound = false;

                for (var userId in data) {
                    var user = data[userId];

                    user.combined_posts.forEach(function(post) {
                        if (post.id.toString() === id) {
                            if (!postFound) {
                                var postsHeader = document.createElement('h2');
                                postsHeader.textContent = 'Post';
                                resultsContainer.appendChild(postsHeader);
                                postFound = true;
                            }
                            var postElement = document.createElement('div');
                            postElement.className = 'post';
                            postElement.innerHTML = `
                                <strong>${user["昵称"]} (${userId})</strong>
                                <div>${highlightKeywords(post.text)}</div>
                                <div class="time">Time: ${post.time}</div>
                                <div class="translation">Translation: ${post.text_en}</div>
                                <div class="id">
                                    Post ID: ${post.id}
                                    <br>
                                    <a href="https://weibo.com/detail/${post.id}" target="_blank">Visit Post</a>
                                </div>
                            `;
                            resultsContainer.appendChild(postElement);
                        }

                        post.comments.forEach(function(comment) {
                            if (comment.id.toString() === id) {
                                if (!commentFound) {
                                    var commentsHeader = document.createElement('h2');
                                    commentsHeader.textContent = 'Comment';
                                    resultsContainer.appendChild(commentsHeader);
                                    commentFound = true;
                                }
                                var commentElement = document.createElement('div');
                                commentElement.className = 'comment';
                                commentElement.innerHTML = `
                                    <strong>${comment.nickname} (${comment.user_id}):</strong>
                                    <div>${highlightKeywords(comment.text)}</div>
                                    <div class="time">Time: ${comment.time}</div>
                                    <div class="translation">Translation: ${comment.text_en}</div>
                                    <div class="id">Comment ID: ${comment.id}</div>
                                `;
                                resultsContainer.appendChild(commentElement);
                            }
                        });
                    });
                }

                if (!postFound && !commentFound) {
                    resultsContainer.innerHTML = '<p>No results found for ID "' + id + '".</p>';
                }

                // 显示弹窗
                document.getElementById('search-modal').style.display = 'flex';
            }
        }

        function closeModal() {
            document.getElementById('search-modal').style.display = 'none';
        }

        function highlightKeywords(text) {
            var criteria_keywords = {
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
            };

            var status_mapping = {{ status_mapping | tojson | safe }};

            for (var category in criteria_keywords) {
                criteria_keywords[category].forEach(function(keyword) {
                    var regex = new RegExp(keyword, 'g');
                    text = text.replace(regex, `<span class='highlight'>${keyword} (${status_mapping[keyword]})</span>`);
                });
            }
            return text;
        }

    </script>
</head>
<body>
    <h1>Weibo Data Analysis for Academic Research on Depression</h1>
    <div class="update-time">Last Updated: September 3, 2024</div>
    <div class="search-container">
        <input type="text" id="keyword-searcher" class="search-box" placeholder="Enter keyword">
        <button class="search-button" onclick="performSearch()">Search by Keyword</button>
    </div>
    <div class="search-container">
        <input type="text" id="id-searcher" class="search-box" placeholder="Enter Post ID or Comment ID">
        <button class="search-button" onclick="performIdSearch()">Search by ID</button>
    </div>
    {% for user_id, user in data.items() %}
    <div class="user">
        <div class="user-header" onclick="toggleDetails('{{ user_id }}')">
            <button class="reply-button" onclick="event.stopPropagation(); openReplyModal();">
                <img src="/static/envelope.jpeg" alt="Reply">
            </button>
            ID: {{ user_id }} | Nickname: {{ user["昵称"] }}
        </div>
        <div class="status">
            <strong>Status:</strong>
            {% for key, value in user["状态"].items() %}
                <span>{{ key }} → {{ value | join(", ") }}</span>
            {% endfor %}
        </div>
        <div class="open-attitude">
            <strong>Open Attitude:</strong>
            <span>{{ "Yes" if user["开放态度"] else "No" }}</span>
        </div>
        <div class="user-details" id="details-{{ user_id }}">
            {% for post in user["combined_posts"] %}
            <div class="post">
                <div class="post-text">{{ post['text'] | safe }}</div>
                <div class="time">Time: {{ post['time'] }}</div>
                <div class="translation">Translation: {{ post['text_en'] | safe }}</div>
                <div class="id">
                    Post ID: {{ post['id'] | safe }}
                    <br>
                    <a href="https://weibo.com/detail/{{ post['id'] }}" target="_blank">Visit Post</a>
                </div>
                <div class="ice-break-container">
                    <button onclick="toggleIceBreakButtons('{{ user_id }}-{{ post['time'] }}')" class="ice-break-button">Ice-break with different identities</button>
                    <div class="identity-buttons" id="ice-break-buttons-{{ user_id }}-{{ post['time'] }}">
                        <button class="identity-button" onclick="handleIdentityButtonClick(this, '{{ post['id'] }}', '{{ post['text'] }}')">Psychiatrist</button>
                        <button class="identity-button" onclick="handleIdentityButtonClick(this, '{{ post['id'] }}', '{{ post['text'] }}')">Depressed Patient</button>
                        <button class="identity-button" onclick="handleIdentityButtonClick(this, '{{ post['id'] }}', '{{ post['text'] }}')">Recovered Patient</button>
                        <button class="identity-button" onclick="handleIdentityButtonClick(this, '{{ post['id'] }}', '{{ post['text'] }}')">Normal Person</button>
                        <button class="identity-button" onclick="handleIdentityButtonClick(this, '{{ post['id'] }}', '{{ post['text'] }}')">Psychiatrist (bot)</button>
                        <button class="identity-button" onclick="handleIdentityButtonClick(this, '{{ post['id'] }}', '{{ post['text'] }}')">Depressed Patient (bot)</button>
                        <button class="identity-button" onclick="handleIdentityButtonClick(this, '{{ post['id'] }}', '{{ post['text'] }}')">Recovered Patient (bot)</button>
                        <button class="identity-button" onclick="handleIdentityButtonClick(this, '{{ post['id'] }}', '{{ post['text'] }}')">Normal Person (bot)</button>
                    </div>
                </div>
                <div class="comments">
                    {% for comment in post["comments"] %}
                    <div class="comment">
                        <strong>{{ comment['nickname'] }} ({{ comment['user_id'] }}):</strong> {{ comment['text'] | safe }}
                        <div class="time">Time: {{ comment['time'] }}</div>
                        <div class="translation">Translation: {{ comment['text_en'] | safe }}</div>
                        <div class="id">Comment ID: {{ comment['id'] | safe }}</div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    {% endfor %}
    
    <!-- 搜索结果弹窗 -->
    <div id="search-modal" class="modal">
        <div class="modal-content">
            <span class="modal-close" onclick="closeModal()">&times;</span>
            <div id="modal-results-container"></div>
        </div>
    </div>

    <!-- Reply Modal -->
    <div id="reply-modal" class="modal">
        <div class="modal-content">
            <span class="modal-close" onclick="closeReplyModal()">&times;</span>
            <div class="default-reply"></div>
            <div>
                <label for="my-reply">my_reply:</label>
                <input type="text" class="my-reply" id="my-reply">
            </div>
            <button class="response-button" onclick="sendResponse(this)">response</button>
        </div>
    </div>
</body>
</html>
"""

# 使用模板引擎生成HTML内容
template = Template(html_template)
html_content = template.render(data=data, USE_DIRECT_JSON=USE_DIRECT_JSON, status_mapping=status_mapping)

# 将生成的HTML内容写入文件
with open('index.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

print("HTML文件已生成：index.html")