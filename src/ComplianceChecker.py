import csv
from logging import info
import json

class ComplianceChecker:
    def __init__(self): # Global variables used to store baseline and gpo settings and info
        self.bl_settings_and_values = {}
        self.gpo_settings_and_values = {}
        self.baseline_type = "Custom"
        self.output_results = []

    def set_baseline_type(self, baseline_type):
        self.baseline_type = baseline_type

    # Retrieves settings and information from baseline file
    def get_bl_settings_and_values(self, baseline_csv):
        with open(baseline_csv, mode='r') as b:
            reader = csv.DictReader(b)
            for row in reader:
                setting = row['SettingName'].strip()
                info = [row['ExpectedValue'].strip(), row['Framework'].strip(), row['ControlID'].strip(), row['Description'].strip(), row['Severity'].strip(), row['Category'].strip()]
                self.bl_settings_and_values[setting] = info

    # Retrieves settings and information from GPO file
    def get_gpo_settings_and_values(self, gpo):
        gpo_set_and_val = {}
        with open(gpo, 'r') as f:
            for eachLine in f.readlines():
                if " = " in eachLine:
                    formatted = eachLine.strip().split(" = ")
                    gpo_set_and_val[formatted[0]] = formatted[1]

        self.gpo_settings_and_values = gpo_set_and_val

    # Checks compliance between baseline and gpo files
    def check_gpo_compliance(self):
        local_results = []
        for setting, actual in self.gpo_settings_and_values.items():
            if setting in self.bl_settings_and_values:
                expected, framework, cid, desc, severity, category = self.bl_settings_and_values[setting]
                if actual == expected:
                    status = "COMPLIANT"
                else:
                    status = "NOT COMPLIANT"
                record = {
                    "baseline": self.baseline_type,
                    "setting": setting,
                    "expected": expected,
                    "actual": actual,
                    "status": status,
                    "framework": framework,
                    "control_id": cid,
                    "description": desc,
                    "severity": severity,
                    "category": category
                }

                print(f"{setting}: {status} (Severity: {severity}) | Description: {desc}")
                local_results.append(record)
        self.output_results.extend(local_results)

    # Logs compliance check results to csv doc
    def log_results(self):
        csv_path = "../reports/compliance_report.csv"
        json_path = "../reports/compliance_report.json"

        # CSV
        with open(csv_path, 'w') as f:
            f.write(
                "Baseline,SettingName,ExpectedValue,ActualValue,Framework,ControlID,Description,Severity,Category\n")
            for rec in self.output_results:
                f.write(
                    f"{rec['baseline']},{rec['setting']},"
                    f"{rec['expected']},{rec['actual']},"
                    f"{rec['framework']},{rec['control_id']},"
                    f"\"{rec['description']}\",{rec['severity']},{rec['category']}\n"
                )

        # JSON
        with open(json_path, 'w') as f:
            json.dump(self.output_results, f, indent=2)


