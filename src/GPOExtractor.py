import subprocess
import os
import requests


class GPOExtractor:
    def __init__(self, export_path, flask_url):
        self.export_path = export_path
        self.flask_url = flask_url

    # Uses subprocess to extract GPO report
    def extract_gpo(self):
        try:
            cmd = ["powershell.exe", "-Command", f'Get-GPOReport -All -ReportType Xml -Path "{self.export_path}"']
            subprocess.run(cmd, check=True)
            print(f"[+] GPO file exported to {self.export_path}")
        except Exception as e:
            print(f"[!] Failed to export GPO file: {e}")

    # Sends extracted GPO file to flask api
    def send_gpo_to_flask(self, bl_path):
        try:
            files = {
                "gpo_file": open(self.export_path, 'rb'),
                'baseline_file': open(bl_path, 'rb')
            }
            result = requests.post(f"{self.flask_url}/upload", files=files)
            return result.json()
        except Exception as e:
            print(f"[!] Upload error: {e}")

    # Runs flask app to display results
    def run_scan(self, gpo_path, baseline_path):
        res = requests.post(f"{self.flask_url}/scan", json={
            "gpo_path": gpo_path,
            "baseline_path": baseline_path
        })
        if res.status_code == 200:
            print("[+] Scan Results:")
            print(res.json())
        else:
            print("[!] Scan failed:", res.text)