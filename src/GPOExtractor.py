import subprocess
import os
import requests


class GPOExtractor:
    def __init__(self):
        self.export_path = "GPOGuard/gpo_uploads/auto_gpo_export.txt"
        self.flask_url = "127.0.0.1:5000"

    # Uses subprocess to extract GPO report
    def extract_gpo(self):
        try: #### CHANGE TO SECEDIT
            cmd = ["powershell.exe", "-Command", f'Get-GPOReport -All -ReportType Xml -Path "{self.export_path}"']
            subprocess.run(cmd, check=True)
            return f"[+] GPO file exported to {self.export_path}"
        except Exception as e:
            return f"[!] Failed to export GPO file: {e}"

    # Sends extracted GPO file to flask api
    def send_gpo_to_flask(self):
        try:
            files = {
                "gpo_file": open(self.export_path, 'rb')
            }
            response = requests.post(f"http://{self.flask_url}/gpo_uploads", files=files)
            return response.json()
        except Exception as e:
            return f"[!] Upload error: {e}"

    # Runs flask app to display results
    def run_scan(self, gpo_path, baseline_path):
        res = requests.post(f"{self.flask_url}/scan", json={
            "gpo_path": gpo_path,
            "baseline_path": baseline_path
        })
        if res.status_code == 200:
           return res.json()
        else:
            return f"[!] Error: {res.status_code}"