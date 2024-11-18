from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import qianfan
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF

app = Flask(__name__)
CORS(app)

# 配置上传文件夹
UPLOAD_FOLDER = '/tmp'  # Vercel 只允许写入 /tmp 目录
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/uploadReport', methods=['POST'])
def handle_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            # 保存文件
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            # 解析PDF
            doc = fitz.open(file_path)
            text_content = ""
            for page in doc:
                text_content += page.get_text()
            doc.close()

            # 创建千帆客户端
            chat_client = qianfan.ChatCompletion(
                ak=os.getenv('QIANFAN_AK'),
                sk=os.getenv('QIANFAN_SK')
            )

            def generate():
                response = chat_client.do(
                    messages=[{
                        "role": "user",
                        "content": f"作为一名专业的全科医生，请帮我解读这份体检报告，报告内容如下：{text_content}"
                    }],
                    model="ERNIE-Speed-128K",
                    temperature=0.1,
                    stream=True
                )

                for chunk in response:
                    if 'result' in chunk:
                        yield f"data: {chunk['result']}\n\n"

            return Response(
                generate(),
                mimetype='text/event-stream',
                headers={
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive'
                }
            )

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Invalid request'}), 400

def handler(event, context):
    return app(event, context) 