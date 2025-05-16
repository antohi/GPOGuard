from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "GPOGuard Flask is running"

if __name__ == '__main__':
    app.run(debug=True)

upload_folder = 'uploads'
os.makedirs(upload_folder, exist_ok=True)
app.config['UPLOAD_FOLDER'] = upload_folder

def upload():
    gpo_file = request.files['gpo_file']
    baseline_file = request.files['baseline_file']

    gpo_path = os.path.join(app.config['UPLOAD_FOLDER'], gpo_file.filename)
    baseline_path = os.path.join(app.config['UPLOAD_FOLDER'], baseline_file.filename)

    gpo_file.save(gpo_path)
    baseline_file.save(baseline_path)

    return jsonify({"gpo_path": gpo_path, "baseline_path": baseline_path})