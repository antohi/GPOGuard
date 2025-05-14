from AIEngine import *

class ComplianceEngine:
    def __init__(self, parsed_gpo, parsed_baseline, bl_type):
        self.parsed_gpo = parsed_gpo
        self.parsed_baseline = parsed_baseline
        self.bl_type = bl_type

        self.control_filter = None
        self.control_filter_status = False

        self.controls_compliant = 0
        self.controls_non_compliant = 0
        self.all_checked = 0

        self.ai_enabled = False
        self.ai = AIRemediation()

    def check_compliance(self):
        ai_suggestion = None
        local_results = []
        for setting, actual in self.parsed_gpo.items():
            if setting in self.parsed_baseline:
                expected, framework, cid, desc, severity, category = self.parsed_baseline[setting]
                if self.control_filter_status == True and cid != self.control_filter:
                    continue
                if actual == expected:
                    status = "COMPLIANT"
                    self.controls_compliant += 1
                    ai_suggestion = None
                else:
                    status = "NON-COMPLIANT"
                    if self.ai_enabled:
                        ai_suggestion = self.ai.get_ai_suggestions(cid, desc)
                    self.controls_non_compliant += 1
                record = {
                    "baseline": self.bl_type,
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
                self.all_checked += 1
                local_results.append(record)
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
