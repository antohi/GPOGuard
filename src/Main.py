from ComplianceChecker import ComplianceChecker

cc = ComplianceChecker()

cc.get_settings_and_values("../data/compliance_baseline.csv")
cc.get_gpo_settings_and_values("../data/lab_policy_compliant.txt")

cc.check_gpo_compliance()

