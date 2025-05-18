from flask import Flask, request, jsonify
import os

from BaselineParser import BaselineParser
from GPOParser import GPOParser
from ComplianceEngine import ComplianceEngine
from GPOExtractor import GPOExtractor
# http://127.0.0.1:5000
app = Flask(__name__)

gpo_upload_folder = 'gpo_uploads'
bl_upload_folder = 'bl_uploads'
os.makedirs(gpo_upload_folder, exist_ok=True)
app.config['GPO_UPLOAD_FOLDER'] = gpo_upload_folder
app.config['BL_UPLOAD_FOLDER'] = bl_upload_folder


@app.route('/')
def home():
    return "GPOGuard Flask is running"

# Sets up gpo upload from user computer
@app.route('/gpo_uploads', methods=['POST'])
def gpo_upload():
    gpo_file = request.files['gpo_file']
    gpo_path = os.path.join(app.config['GPO_UPLOAD_FOLDER'], gpo_file.filename)
    gpo_file.save(gpo_path)

    return jsonify({
        "gpo_file": os.path.abspath(gpo_path),
    })

# Sets up bl upload from user computer
@app.route('/bl_uploads', methods=['POST'])
def bl_upload():
    baseline_file = request.files['baseline_file']
    baseline_path = os.path.join(app.config['BL_UPLOAD_FOLDER'], baseline_file.filename)
    baseline_file.save(baseline_path)

    return jsonify({
        "baseline_file": os.path.abspath(baseline_path)
    })

# Sets up scanning and parsing of the provided GPO and BL file paths
@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    gpo_path = data.get("gpo_path")
    baseline_path = data.get("baseline_path")

    ce = ComplianceEngine()
    gpop = GPOParser.parse_gpo(gpo_path)
    blp = BaselineParser.parse_bl(baseline_path)
    ce.check_compliance(gpop, blp, "Custom")
    return jsonify(ce.output_results)

@app.route('/extract_and_upload', methods=['POST'])
def extract_and_upload():
    baseline_path = request.form.get("baseline_path")
    extractor = GPOExtractor()
    export_status = extractor.extract_gpo()

    upload_response = extractor.send_gpo_to_flask()
    if "gpo_file" not in upload_response:
        return jsonify({"error": "Upload failed", "detail": upload_response}), 500

    scan_result = extractor.run_scan(upload_response["gpo_file"], baseline_path)
    return jsonify(scan_result)


if __name__ == '__main__':
    app.run(debug=True)