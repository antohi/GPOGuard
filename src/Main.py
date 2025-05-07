from ComplianceChecker import ComplianceChecker
import os
def list(folder):
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))] # Returns files in directory

exit = False
cc = ComplianceChecker()

print("===[GPOGuard]===")
while exit == False: # UI Continues until exit is True
    print("\n=[MAIN MENU]=")# Main Menu options
    print("[1] Custom GPO Compliance")
    print("[2] Healthcare GPO Compliance (HIPAA 164.312(b) + NIST 800‑53 AU‑2)")
    print("[3] Finance GPO Compliance (PCI‑DSS 8.2.3 + NIST 800‑53 IA‑5)")
    print("[4] Enterprise GPO Compliance (NIST 800-53)")
    choice = input("> ")

    if choice == "1": # Main Menu option #1 Custom GPO Compliance
        post_result_choice = "1" # Users can keep scanning for compliance until 2 is entered in post menu
        while post_result_choice == "1":
            print("\n=[Custom GPO Compliance Checker]=")
            print("[FILE SELECTION]")
            print("Please select a GPO file to check for compliance (/data directory)"
                  "\n\nFiles in /data directory:")
            print(list("../data")) # Prints files in directory using list function
            gpo_file = input("> ")

            print("\nPlease select a compliance baseline (/data directory)"
                  "\nFiles in /data directory:")
            print(list("../data")) # Prints files in data directory using list function
            baseline_file = input("> ")
            cc.get_bl_settings_and_values(f"../data/{baseline_file}")
            cc.get_gpo_settings_and_values(f"../data/{gpo_file}")

            print("\n[CUSTOM GPO COMPLIANCE RESULTS]")
            cc.check_gpo_compliance()
            print("\n[MENU]") # Post-menu where user can break loop or scan another doc for compliance
            print("[1] Check another file for compliance")
            print("[2] Main Menu")
            post_result_choice = input("> ")
    if choice == "2":  # Main Menu option #2 Healthcare GPO Compliance Checker
        post_result_choice = "1"
        while post_result_choice == "1":
            print("\n=[Healthcare GPO Compliance]=")
            print("[FILE SELECTION]")
            print("Please select a GPO file to check for compliance (/data directory)"
                  "\n\nFiles in /data directory:")
            print(list("../data"))  # Prints files in directory using list function
            gpo_file = input("> ")

            cc.get_bl_settings_and_values(f"../data/healthcare_baseline.csv")
            cc.get_gpo_settings_and_values(f"../data/{gpo_file}")

            print("\n[HEALTHCARE GPO COMPLIANCE RESULTS]")
            cc.check_gpo_compliance()
            print("\n[MENU]")  # Post-menu where user can break loop or scan another doc for compliance
            print("[1] Check another file for compliance")
            print("[2] Main Menu")
            post_result_choice = input("> ")

    else: # If menu option is invalid
        print("[!] INVALID MENU OPTION\n")

