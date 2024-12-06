from flask import Flask, request, jsonify, render_template
from test_api import get_chat, res_to_post

app = Flask(__name__)

# 首页路由，返回 HTML 文件
@app.route('/')
def index():
    return render_template('index.html')

# 处理前端传来的请求，调用get_chat获取默认回复
@app.route('/get_reply', methods=['POST'])
def get_reply():
    data = request.json
    identity = data['identity']
    post_content = data['post_content']
    
    # 调用get_chat函数
    default_reply = get_chat(identity, post_content)
    
    return jsonify({
        'default_reply': default_reply
    })

# 处理前端传来的响应请求，调用res_to_post函数发送回复
@app.route('/send_response', methods=['POST'])
def send_response():
    data = request.json
    identity = data['identity']
    post_id = data['post_id']
    reply_content = data['reply_content']
    
    # 调用res_to_post函数
    res_to_post(identity, post_id, reply_content)
    
    return jsonify({
        'status': 'success'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)