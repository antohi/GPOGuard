from ComplianceChecker import ComplianceChecker
import os
def list(folder):
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

exit = False
cc = ComplianceChecker()

print("===[GPOGuard]===\n")
while exit == False:
    print("=[MENU]=")
    print("[1] GPO Compliance Checker\n")
    choice = input("> ")

    if choice == "1":
        print("\nPlease select a GPO file to check for compliance (/data directory)"
              "\nFiles in /data directory:")
        print(list("../data"))
        gpo_file = input("> ")

        print("\nPlease select a compliance baseline (/data directory)"
              "\nFiles in /data directory:")
        print(list("../data"))
        baseline_file = input("> ")
        cc.get_bl_settings_and_values(f"../data/{baseline_file}")
        cc.get_gpo_settings_and_values(f"../data/{gpo_file}")

        cc.check_gpo_compliance()


    else:
        print("[!] INVALID MENU OPTION\n")

