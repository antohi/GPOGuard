import subprocess
import os

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
