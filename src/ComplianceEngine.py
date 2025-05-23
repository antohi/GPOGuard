import json

from AIEngine import *

class ComplianceEngine:
    def __init__(self):
        self.control_filter = None
        self.control_filter_status = False

        self.controls_compliant = 0
        self.controls_non_compliant = 0
        self.all_checked = 0
        self.output_results = []

        self.ai_enabled = False
        self.ai = AIRemediation()

    # Core function of the project, checks what controls are compliant and non-compliant in comparison to baseline.
    def check_compliance(self, parsed_gpo, parsed_baseline, bl_type):
        ai_suggestion = None
        local_results = []

        for setting, baseline_entry in parsed_baseline.items():
            expected, framework, cid, desc, severity, category = baseline_entry
            actual = parsed_gpo.get(setting) if parsed_gpo.get(setting) else "MISSING"

            if self.control_filter_status and cid != self.control_filter: # If Control Filter is on and cid does not match filter, skip
                continue

            if actual == expected:
                status = "COMPLIANT"
                self.controls_compliant += 1
                ai_suggestion = None
            else:
                status = "NON-COMPLIANT"
                if self.ai_enabled:
                    ai_suggestion = self.ai.get_ai_suggestions(cid, desc) # Retrieve AI suggestion if non-compliant
                self.controls_non_compliant += 1

            record = { # Creates record dictionary to add to local results
                "baseline": bl_type,
                "setting": setting,
                "expected": expected,
                "actual": actual,
                "status": status,
                "framework": framework,
                "control_id": cid,
                "description": desc,
                "severity": severity,
                "category": category,
                "ai_suggestion": ai_suggestion or "N/A"
            }

            local_results.append(record)
            self.all_checked += 1

        self.output_results.extend(local_results) # Adds to 'global' results for report downloads
        return local_results

    # Applies control filter, if no control id used, filter is cleared.
    def apply_control_filter(self, control_id=None):
        if control_id:
            self.control_filter = control_id
            self.control_filter_status = True
        else:
            self.control_filter = None
            self.control_filter_status = False

    # Prints stats of total controls checked, total compliant, and total non-compliant
    def get_stats(self) -> list:
        stats = [self.all_checked, self.controls_compliant, self.controls_non_compliant]
        return stats


    # Resets stats back to 0 for next scan
    def reset_stats(self):
        self.all_checked = 0
        self.controls_compliant = 0
        self.controls_non_compliant = 0

    # Enables ai
    def set_ai(self, enabled: bool):
        self.ai_enabled = enabled

    # Logs compliance check results to csv doc
    def log_results(self):
        try:
            csv_path = "../reports/compliance_report.csv"
            # CSV
            with open(csv_path, 'w') as f:
                f.write(
                    "Baseline,SettingName,ExpectedValue,ActualValue,Framework,ControlID,Description,Severity,Category,AISuggestion\n")
                for rec in self.output_results:
                    f.write(
                        f"{rec['baseline']},{rec['setting']},"
                        f"{rec['expected']},{rec['actual']},"
                        f"{rec['framework']},{rec['control_id']},"
                        f"\"{rec['description']}\",{rec['severity']},{rec['category']},{rec['ai_suggestion']}\n"
                    )
        except Exception as e:
            return "[!] ERROR: Unable to write CSV compliance report: " + str(e)

        try:
            # JSON
            json_path = "../reports/compliance_report.json"
            with open(json_path, 'w') as f:
                json.dump(self.output_results, f, indent=2)
        except Exception as e:
            return "[!] ERROR: Unable to write JSON compliance report: " + str(e)