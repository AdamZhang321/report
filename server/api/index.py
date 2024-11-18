from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# 添加服务器目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.uploadReport import upload_report, stream_report

app = Flask(__name__)
CORS(app)

# 配置上传文件夹
UPLOAD_FOLDER = '/tmp'  # Vercel 只允许写入 /tmp 目录
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/uploadReport', methods=['POST'])
def handle_upload():
    return upload_report()

@app.route('/api/stream-report', methods=['GET'])
def handle_stream():
    return stream_report()

# Vercel 需要这个处理函数
def handler(event, context):
    return app(event, context) 