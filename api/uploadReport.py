from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from langchain_community.llms import QianfanLLMEndpoint
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyMuPDFLoader
import uuid

app = Flask(__name__)

# 配置文件上传路径
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 配置千帆API密钥
os.environ["QIANFAN_AK"] = 'm5eAEwmGKUji6YJ9s4YZSXdp'
os.environ["QIANFAN_SK"] = '8VOq5CA9pV5FaqcGCLChHagvZ95XeQ8X'

@app.route('/api/uploadReport', methods=['POST'])
def upload_report():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        # 生成唯一的报告ID
        report_id = str(uuid.uuid4())
        
        # 保存上传的文件
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, f"{report_id}_{filename}")
        file.save(file_path)

        try:
            # 初始化大语言模型
            llm = QianfanLLMEndpoint(model="ERNIE-Speed-128K", temperature=0.1)

            # 解析PDF文件
            loader = PyMuPDFLoader(file_path)
            documents = loader.load()

            # 创建提示模板
            chat_template = ChatPromptTemplate.from_messages([
                ("system", "你是一名专业的全科医生，需要对体检报告进行权威解读"),
                ("human", "医生，请帮我解读下我的体检报告，报告内容如下：{reports}"),
            ])

            # 生成解读结果
            output = chat_template.invoke({'reports': documents})
            result = llm.invoke(output)

            # 保存解读结果
            with open(os.path.join(UPLOAD_FOLDER, f"{report_id}_result.txt"), 'w') as f:
                f.write(result)

            return jsonify({
                'reportId': report_id,
                'message': 'Upload successful'
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 