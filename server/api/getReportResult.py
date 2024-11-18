from flask import jsonify, request, current_app
import os

def get_report_result():
    report_id = request.args.get('reportId')
    if not report_id:
        return jsonify({'error': 'Report ID is required'}), 400

    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
    result_path = os.path.join(UPLOAD_FOLDER, f"{report_id}_result.txt")
    
    try:
        with open(result_path, 'r', encoding='utf-8') as f:
            result = f.read()
        return jsonify({'result': result})
    except FileNotFoundError:
        return jsonify({'error': 'Report not found'}), 404 