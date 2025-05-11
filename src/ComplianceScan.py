import csv
import logging
from logging import info
import json

class ComplianceScan:
    def __init__(self): # Global variables used to store baseline and gpo settings and info
        self.bl_settings_and_values = {}
        self.gpo_settings_and_values = {}
        self.baseline_type = "Custom"
        self.output_results = []
        self.control_filter = None
        self.control_filter_status = False

        self.controls_checked = 0
        self.controls_compliant = 0
        self.controls_non_compliant = 0

    def set_baseline_type(self, baseline_type):
        self.baseline_type = baseline_type

    # Retrieves settings and information from baseline file
    def get_bl_settings_and_values(self, baseline_csv):
        try:
            with open(baseline_csv, mode='r') as b:
                reader = csv.DictReader(b)
                for row in reader:
                    setting = row['SettingName'].strip()
                    info = [row['ExpectedValue'].strip(), row['Framework'].strip(), row['ControlID'].strip(), row['Description'].strip(), row['Severity'].strip(), row['Category'].strip()]
                    self.bl_settings_and_values[setting] = info
        except Exception as e:
            print(f"[!] ERROR: Unable to read baseline file. Exception: {e}")

    # Retrieves settings and information from GPO file
    def get_gpo_settings_and_values(self, gpo):
        gpo_set_and_val = {}
        try:
            with open(gpo, 'r') as f:
                for eachLine in f.readlines():
                    if " = " in eachLine:
                        formatted = eachLine.strip().split(" = ")
                        gpo_set_and_val[formatted[0]] = formatted[1]

            self.gpo_settings_and_values = gpo_set_and_val
        except Exception as e:
            print(f"[!] ERROR: Unable to read GPO file. Exception: {e}")

    # Checks compliance between baseline and gpo files
    def check_gpo_compliance(self):
        local_results = []
        for setting, actual in self.gpo_settings_and_values.items():
            if setting in self.bl_settings_and_values:
                expected, framework, cid, desc, severity, category = self.bl_settings_and_values[setting]
                if self.get_control_filter_status() == True:
                    if cid != self.get_control_filter():
                        continue
                if actual == expected:
                    status = "COMPLIANT"
                    self.controls_compliant += 1
                else:
                    status = "NOT COMPLIANT"
                    self.controls_non_compliant += 1
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
                self.controls_checked += 1

                print(f"{setting}: {status}\nSeverity: {severity}\nDescription: {desc}\n---")
                local_results.append(record)
        self.output_results.extend(local_results)

    # Logs compliance check results to csv doc
    def log_results(self):
        try:
            csv_path = "../reports/compliance_report.csv"
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
        except Exception as e:
            print(f"[!] ERROR: Unable to write report CSV file. Exception: {e}")
            logging.error(f"[!] ERROR: Unable to write report CSV file. Exception: {e}")

        try:
            # JSON
            json_path = "../reports/compliance_report.json"
            with open(json_path, 'w') as f:
                json.dump(self.output_results, f, indent=2)
        except Exception as e:
            print(f"[!] ERROR: Unable to write report JSON file. Exception: {e}")
            logging.error(f"[!] ERROR: Unable to write report JSON file. Exception: {e}")

    # Sets self.control_filter_status class variable to True
    def set_control_filter_status(self, status):
        self.control_filter_status = status

    # Sets self.control_filter to the control to be filtered by
    def set_control_filter(self, control_filter):
        self.control_filter = control_filter

    # Returns boolean self.control_filter_status
    def get_control_filter_status(self):
        return self.control_filter_status

    # Returns what the control filter is in self.control_filter
    def get_control_filter(self):
        return self.control_filter

    # Resets control filter
    def reset_filter(self):
        self.control_filter_status = False
        self.control_filter = None

    # Prints stats of total controls checked, total compliant, and total non-compliant
    def get_stats(self):
        print(f"\n[Controls Stats]"
              f"\nChecked: {self.controls_checked} | Compliant: {self.controls_compliant} | Non-Compliant: {self.controls_non_compliant}")

    # Resets stats back to 0 for next scan
    def reset_stats(self):
        self.controls_checked = 0
        self.controls_compliant = 0
        self.controls_non_compliant = 0






