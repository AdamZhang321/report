from flask import request, jsonify, current_app, Response, stream_with_context
from werkzeug.utils import secure_filename
import os
from langchain_community.llms import QianfanLLMEndpoint
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyMuPDFLoader
import uuid
import qianfan
import json

# 全局变量存储最新的文件路径
current_file_path = None

def upload_report():
    global current_file_path
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            # 保存文件
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # 保存文件路径供流式处理使用
            current_file_path = file_path
            
            return jsonify({'message': 'File uploaded successfully'})

        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({'error': str(e)}), 500

def stream_report():
    global current_file_path
    if not current_file_path:
        return jsonify({'error': 'No file uploaded'}), 400

    try:
        # 创建千帆客户端
        chat_client = qianfan.ChatCompletion(
            ak=os.getenv('QIANFAN_AK'),
            sk=os.getenv('QIANFAN_SK')
        )

        # 解析PDF文件
        loader = PyMuPDFLoader(current_file_path)
        documents = loader.load()
        text_content = "\n".join([doc.page_content for doc in documents])

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
                    data = {
                        "result": chunk['result'],
                        "is_end": chunk.get('is_end', False)
                    }
                    yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

        return Response(
            stream_with_context(generate()),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'X-Accel-Buffering': 'no',
                'Content-Type': 'text/event-stream'
            }
        )

    except Exception as e:
        print(f"Error in stream_report: {str(e)}")
        return jsonify({'error': str(e)}), 500