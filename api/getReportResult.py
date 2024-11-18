from flask import jsonify, request
import os

@app.route('/api/getReportResult', methods=['GET'])
def get_report_result():
    report_id = request.args.get('reportId')
    if not report_id:
        return jsonify({'error': 'Report ID is required'}), 400

    result_path = os.path.join(UPLOAD_FOLDER, f"{report_id}_result.txt")
    
    try:
        with open(result_path, 'r') as f:
            result = f.read()
        return jsonify({'result': result})
    except FileNotFoundError:
        return jsonify({'error': 'Report not found'}), 404 