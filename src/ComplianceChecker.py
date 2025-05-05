import csv


class ComplianceChecker:

    def create_NIST800_baseline(self, baseline_csv):
        settings_and_values = {}

        line = 0
        with open(baseline_csv, 'r') as f:
            for eachLine in f.readlines():
                if line > 0:
                    formatted = eachLine.split(",")
                    settings_and_values[formatted[0]] = formatted[1]
                line += 1
        print("Setting:", settings_and_values.keys(), settings_and_values.values())

