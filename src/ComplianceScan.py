import csv
import logging
from logging import info
import json
from AIRemediation import AIRemediation
import textwrap
from colorama import Fore, Style, init
init(autoreset=True)

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

        self.ai = AIRemediation

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
            print(f"{Fore.LIGHTRED_EX}[!] ERROR:{Style.RESET_ALL} Unable to read GPO file. Exception: {e}")

    # Checks compliance between baseline and gpo files
    def check_gpo_compliance(self):
        ai_suggestion = None
        local_results = []
        for setting, actual in self.gpo_settings_and_values.items():
            if setting in self.bl_settings_and_values:
                expected, framework, cid, desc, severity, category = self.bl_settings_and_values[setting]
                if self.control_filter_status == True and cid != self.get_control_filter():
                    continue
                if actual == expected:
                    status = f"{Fore.GREEN}COMPLIANT{Style.RESET_ALL}"
                    self.controls_compliant += 1
                    ai_suggestion = None
                else:
                    status = f"{Fore.RED}NON-COMPLIANT{Style.RESET_ALL}"
                    self.controls_non_compliant += 1
                    ai_suggestion = self.ai.get_ai_suggestions(cid, desc) # If not compliant, get AI suggestion
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

                print(f"{Fore.LIGHTWHITE_EX}{setting}:{Style.RESET_ALL} {status}"
                      f"\n{Fore.LIGHTWHITE_EX}Severity:{Style.RESET_ALL} {severity}"
                      f"\n{Fore.LIGHTWHITE_EX}Description:{Style.RESET_ALL} {desc}")
                if ai_suggestion is not None: # If AI suggestion exists, print it
                    print(f"\n{Fore.LIGHTMAGENTA_EX}AI Suggestion:{Style.RESET_ALL} {textwrap.fill(ai_suggestion, width=80)}")
                print("---")
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

    # Applies control filter, if no control id used, filter is cleared.
    def apply_control_filter(self, control_id=None):
        if control_id:
            self.control_filter = control_id
            self.control_filter_status = True
        else:
            self.control_filter = None
            self.control_filter_status = False

    # Returns what the control filter is in self.control_filter
    def get_control_filter(self):
        return self.control_filter

    # Resets control filter
    def reset_filter(self):
        self.control_filter_status = False
        self.control_filter = None

    # Prints stats of total controls checked, total compliant, and total non-compliant
    def get_stats(self):
        print(f"{Fore.LIGHTWHITE_EX}\n[Controls Stats]{Style.RESET_ALL}"
              f"\nChecked: {Fore.LIGHTWHITE_EX}{self.controls_checked}{Style.RESET_ALL} | Compliant: {Fore.GREEN}{self.controls_compliant}{Style.RESET_ALL} | Non-Compliant: {Fore.RED}{self.controls_non_compliant}{Style.RESET_ALL}")

    # Resets stats back to 0 for next scan
    def reset_stats(self):
        self.controls_checked = 0
        self.controls_compliant = 0
        self.controls_non_compliant = 0






