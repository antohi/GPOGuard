from flask import Flask, request, jsonify
import os

from src.BaselineParser import BaselineParser
from src.GPOParser import GPOParser
from src.ComplianceEngine import ComplianceEngine

app = Flask(__name__)

@app.route('/')
def home():
    return "GPOGuard Flask is running"

if __name__ == '__main__':
    app.run(debug=True)

upload_folder = 'uploads'
os.makedirs(upload_folder, exist_ok=True)
app.config['UPLOAD_FOLDER'] = upload_folder

# Sets up gpo and baseline file uploads from user computer
@app.route('/upload', methods=['POST'])
def upload():
    gpo_file = request.files['gpo_file']
    baseline_file = request.files['baseline_file']

    gpo_path = os.path.join(app.config['UPLOAD_FOLDER'], gpo_file.filename)
    baseline_path = os.path.join(app.config['UPLOAD_FOLDER'], baseline_file.filename)

    gpo_file.save(gpo_path)
    baseline_file.save(baseline_path)

    return jsonify({"gpo_path": gpo_path, "baseline_path": baseline_path})


# Sets up scanning and parsing of the provided GPO and BL file paths
@app.route('/gpo', methods=['POST'])
def scan():
    data = request.get_json()
    gpo_path = data.get("gpo_path")
    baseline_path = data.get("baseline_path")

    ce = ComplianceEngine()
    gpop = GPOParser.parse_gpo(gpo_path)
    blp = BaselineParser.parse_bl(baseline_path)
    ce.check_compliance(gpop, blp, "Custom")

    return jsonify(ce.output_results)

