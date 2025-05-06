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
        self.settings_and_values = set_and_val

    def get_gpo_setings_and_values(self, gpo):
        gpo_set_and_val = {}
        with open(gpo, 'r') as f:
            for eachLine in f.readlines():
                if " = " in eachLine:
                    formatted = eachLine.strip().split(" = ")
                    gpo_set_and_val[formatted[0]] = formatted[1]

        self.gpo_settings_and_values = gpo_set_and_val


    def check_gpo_compliance(self):
        for setting in self.gpo_settings_and_values.keys():
            if setting in self.settings_and_values.keys():
                if self.settings_and_values[setting] == self.gpo_settings_and_values[setting]:
                    print(f"{setting}: COMPLIANT")
                else:
                    print(f"{setting}: NOT COMPLIANT")



