import csv


class ComplianceChecker:
    def __init__(self):
        self.settings_and_values = {}

    def get_settings_and_values(self, baseline_csv):
        set_and_val = {}
        line = 0
        with open(baseline_csv, 'r') as f:
            for eachLine in f.readlines():
                if line > 0:
                    formatted = eachLine.split(",")
                    set_and_val[formatted[0]] = formatted[1]
                line += 1
        self.settings_and_values = set_and_val


