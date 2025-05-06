from ComplianceChecker import ComplianceChecker
import os
def list(folder):
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

exit = False

while exit == False:
    print("===[GPOGuard]===\n")
    print("=[MENU]=\n")
    print("[1] GPO Compliance Checker\n")
    choice = input("> ")

    if choice == "1":
        print("Please select a GPO file to check for compliance (/data directory)"
              "\nFiles in /data directory:")
        print(list("../data"))
        choice = input("> ")

    else:
        print("[!] INVALID MENU OPTION\n")




"""

cc = ComplianceChecker()

cc.get_bl_settings_and_values("../data/compliance_baseline.csv")
cc.get_gpo_settings_and_values("../data/lab_policy_compliant.txt")

cc.check_gpo_compliance()

"""