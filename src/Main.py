from ComplianceChecker import ComplianceChecker
import os
def list(folder):
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

exit = False
cc = ComplianceChecker()

print("===[GPOGuard]===")
while exit == False:
    print("\n=[MENU]=")
    print("[1] GPO Compliance Checker\n")
    choice = input("> ")

    if choice == "1":
        post_result_choice = "1"
        while post_result_choice == "1":
            print("\n=[GPO Compliance Checker]=")
            print("[FILE SELECTION]")
            print("Please select a GPO file to check for compliance (/data directory)"
                  "\n\nFiles in /data directory:")
            print(list("../data"))
            gpo_file = input("> ")

            print("\nPlease select a compliance baseline (/data directory)"
                  "\nFiles in /data directory:")
            print(list("../data"))
            baseline_file = input("> ")
            cc.get_bl_settings_and_values(f"../data/{baseline_file}")
            cc.get_gpo_settings_and_values(f"../data/{gpo_file}")

            print("\n[COMPLIANCE RESULTS]")
            cc.check_gpo_compliance()
            print("\n[1] Check another file for compliance")
            print("[2] Main Menu")

            post_result_choice = input("> ")

    else:
        print("[!] INVALID MENU OPTION\n")

