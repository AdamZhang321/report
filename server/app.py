from flask import Flask, send_from_directory
from flask_cors import CORS
import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.uploadReport import upload_report, stream_report

app = Flask(__name__, static_folder='../client/dist')
CORS(app)

# 使用绝对路径配置文件上传路径
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 设置全局变量供其他模块使用
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 注册路由
app.route('/api/uploadReport', methods=['POST'])(upload_report)
app.route('/api/stream-report', methods=['GET'])(stream_report)

# 添加静态文件服务
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True) 