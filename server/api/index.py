from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import qianfan
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
import json

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = '/tmp'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def parse_pdf(file_path):
    """解析PDF文件"""
    reader = PdfReader(file_path)
    text_content = ""
    for page in reader.pages:
        text_content += page.extract_text()
    return text_content

def get_ai_response(text_content):
    """获取AI解读结果"""
    chat_client = qianfan.ChatCompletion(
        ak=os.getenv('QIANFAN_AK'),
        sk=os.getenv('QIANFAN_SK')
    )
    
    response = chat_client.do(
        messages=[{
            "role": "user",
            "content": f"作为一名专业的全科医生，请帮我解读这份体检报告，报告内容如下：{text_content}"
        }],
        model="ERNIE-Speed-128K",
        temperature=0.1,
        stream=True
    )
    return response

@app.route('/api/uploadReport', methods=['POST'])
def handle_upload():
    """处理文件上传"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        file_path = None
        try:
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            text_content = parse_pdf(file_path)
            
            def generate():
                try:
                    for chunk in get_ai_response(text_content):
                        if 'result' in chunk:
                            data = {
                                'result': chunk['result'],
                                'is_end': chunk.get('is_end', False)
                            }
                            yield f"data: {json.dumps(data)}\n\n"
                finally:
                    if file_path and os.path.exists(file_path):
                        os.remove(file_path)

            return Response(
                generate(),
                mimetype='text/event-stream',
                headers={
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive'
                }
            )

        except Exception as e:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Invalid request'}), 400

def handler(event, context):
    return app(event, context) 