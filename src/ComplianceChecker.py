import csv

class ComplianceChecker:
    def __init__(self):
        self.bl_settings_and_values = {}
        self.gpo_settings_and_values = {}


    def get_settings_and_values(self, baseline_csv):
        set_and_val = {}
        line = 0
        with open(baseline_csv, 'r') as f:
            for eachLine in f.readlines():
                if line > 0:
                    formatted = eachLine.strip().split(",")
                    set_and_val[formatted[0]] = formatted[1]
                line += 1
        self.bl_settings_and_values = set_and_val

    def get_gpo_settings_and_values(self, gpo):
        gpo_set_and_val = {}
        with open(gpo, 'r') as f:
            for eachLine in f.readlines():
                if " = " in eachLine:
                    formatted = eachLine.strip().split(" = ")
                    gpo_set_and_val[formatted[0]] = formatted[1]

        self.gpo_settings_and_values = gpo_set_and_val


    def check_gpo_compliance(self):
        export_results = {}
        for setting in self.gpo_settings_and_values.keys():
            if setting in self.bl_settings_and_values.keys():
                if self.bl_settings_and_values[setting] == self.gpo_settings_and_values[setting]:
                    export_results[setting] = "COMPLIANT"
                    print(f"{setting}: COMPLIANT")
                else:
                    print(f"{setting}: NOT COMPLIANT")
                    export_results[setting] = "NOT COMPLIANT"

        return self.log_results(export_results)

    def log_results(self, output_results):
        with open("../data/compliance_report.csv", 'w') as cr:
            cr.write("SettingName,Status\n")
            for setting in output_results.keys():
                cr.write(f"{setting},{output_results[setting]}\n")


