from flask import Flask, request, jsonify
import os

from BaselineParser import BaselineParser
from GPOParser import GPOParser
from ComplianceEngine import ComplianceEngine
# http://127.0.0.1:5000
app = Flask(__name__)
upload_folder = 'uploads'
os.makedirs(upload_folder, exist_ok=True)
app.config['UPLOAD_FOLDER'] = upload_folder

@app.route('/')
def home():
    return "GPOGuard Flask is running"

# Sets up gpo and baseline file uploads from user computer
@app.route('/upload', methods=['POST'])
def upload():
    gpo_file = request.files['gpo_file']
    baseline_file = request.files['baseline_file']

    gpo_path = os.path.join(app.config['UPLOAD_FOLDER'], gpo_file.filename)
    baseline_path = os.path.join(app.config['UPLOAD_FOLDER'], baseline_file.filename)

    gpo_file.save(gpo_path)
    baseline_file.save(baseline_path)

    return jsonify({
        "gpo_file": os.path.abspath(gpo_path),
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

if __name__ == '__main__':
    app.run(debug=True)