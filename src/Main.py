import os
import argparse
from ComplianceScan import ComplianceScan
from colorama import Fore, Style, init
init(autoreset=True)

# Lists files in directory
def list_files(folder):
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

# Asks user to select a file to use for their GPO scan
def gpo_file_selection():
    print(f"{Fore.LIGHTWHITE_EX}[FILE SELECTION]{Style.RESET_ALL}")
    print("Please select a GPO file to check for compliance (/data directory)"
          "\n\nFiles in /data/gpo_files directory:")
    print(list_files("../data/gpo_files"))  # Prints files in directory using list function
    return input("> ") # Returns user chosen gpo file

# Asks user to select a baseline file to scan GPO file against
def bl_files_selection():
    print("\nPlease select a compliance baseline (/data directory)"
          "\nFiles in /data directory:")
    print(list_files("../data/baseline_files"))  # Prints files in data directory using list function
    return input("> ")

# Checks if user would like to use a control filter
def control_filter(cc):
    cf = input("\nControl ID Filter [Ex. \"IA-5\" | Leave blank if none]: ")
    if control_filter != "":  # If user entered a CF
        cc.apply_control_filter(cf)

# Main menu of app
def main_menu():
        print(f"\n{Fore.CYAN}=[MAIN MENU]={Style.RESET_ALL}")  # Main Menu options
        print("[1] Custom GPO Compliance")
        print("[2] Healthcare GPO Compliance (HIPAA 164.312(b) + NIST 800‑53 AU‑2)")
        print("[3] Finance GPO Compliance (PCI‑DSS 8.2.3 + NIST 800‑53 IA‑5)")
        print("[4] Enterprise GPO Compliance (NIST 800-53)")
        print("[5] Exit")
        return input("> ")

# Menu where user can select an option after a scan is completed
def post_scan_menu():
    print(f"\n{Fore.LIGHTWHITE_EX}[MENU]{Style.RESET_ALL}")  # Post-menu where user can break loop or scan another doc for compliance
    print("[1] Again (same baseline)"
          "\n[2] Main Menu"
          "\n[3] Exit")
    return input("> ")

# Resets filters and scan stats
def post_scan_reset(cc):
    cc.apply_control_filter()
    cc.reset_stats()

# Starts UI loop
def run_ui(cc):
    print(f"{Fore.LIGHTBLUE_EX}----------------"
          f"\n===[GPOGuard]==="
          f"\n----------------{Style.RESET_ALL}")
    exit = False
    while exit == False:  # UI Continues until exit is True
        choice = main_menu()
        if choice == "1":  # Main Menu option #1 Custom GPO Compliance
            post_result_choice = "1"  # Users can keep scanning for compliance until 2 is entered in post menu
            while post_result_choice == "1":
                print(f"\n{Fore.YELLOW}=[Custom GPO Compliance Checker]={Style.RESET_ALL}")
                gpo_file = gpo_file_selection()
                bl_file = bl_files_selection()
                cc.get_bl_settings_and_values(f"../data/baseline_files/{bl_file}")
                cc.get_gpo_settings_and_values(f"../data/gpo_files/{gpo_file}")
                control_filter(cc)
                print(f"\n{Fore.LIGHTYELLOW_EX}[CUSTOM GPO COMPLIANCE RESULTS]{Style.RESET_ALL}")
                print("---")
                cc.check_gpo_compliance()
                cc.get_stats()
                post_result_choice = post_scan_menu()
                post_scan_reset(cc)
            if post_result_choice == "3":
                exit = True
        elif choice == "2":  # Main Menu option #2 Healthcare GPO Compliance Checker
            post_result_choice = "1"
            while post_result_choice == "1":
                print(f"\n{Fore.YELLOW}=[Healthcare GPO Compliance]={Style.RESET_ALL}")
                gpo_file = gpo_file_selection()
                cc.set_baseline_type("Healthcare")
                cc.get_bl_settings_and_values(f"../data/baseline_files/healthcare_baseline.csv")
                cc.get_gpo_settings_and_values(f"../data/gpo_files/{gpo_file}")
                control_filter(cc)
                print(f"\n{Fore.LIGHTYELLOW_EX}[HEALTHCARE GPO COMPLIANCE RESULTS]{Style.RESET_ALL}")
                print("---")
                cc.check_gpo_compliance()
                cc.get_stats()
                post_result_choice = post_scan_menu()
                post_scan_reset(cc)
            if post_result_choice == "3":
                exit = True
        elif choice == "3":  # Main Menu option #3 Finance GPO Compliance Checker
            post_result_choice = "1"
            while post_result_choice == "1":
                print(f"\n{Fore.YELLOW}=[Finance GPO Compliance]={Style.RESET_ALL}")
                gpo_file = gpo_file_selection()
                cc.set_baseline_type("Finance")
                cc.get_bl_settings_and_values(f"../data/baseline_files/finance_baseline.csv")
                cc.get_gpo_settings_and_values(f"../data/gpo_files/{gpo_file}")
                control_filter(cc)
                print(f"\n{Fore.LIGHTYELLOW_EX}[FINANCE GPO COMPLIANCE RESULTS]{Style.RESET_ALL}")
                print("---")
                cc.check_gpo_compliance()
                cc.get_stats()
                post_result_choice = post_scan_menu()
                post_scan_reset(cc)
            if post_result_choice == "3":
                exit = True
        elif choice == "4":  # Main Menu option #4 Enterprise GPO Compliance Checker
            post_result_choice = "1"
            while post_result_choice == "1":
                print(f"\n{Fore.YELLOW}=[Enterprise GPO Compliance]={Style.RESET_ALL}")
                gpo_file = gpo_file_selection()
                cc.set_baseline_type("Enterprise")
                cc.get_bl_settings_and_values(f"../data/baseline_files/enterprise_baseline.csv")
                cc.get_gpo_settings_and_values(f"../data/gpo_files/{gpo_file}")
                control_filter(cc)
                print(f"\n{Fore.LIGHTYELLOW_EX}[ENTERPRISE GPO COMPLIANCE RESULTS]{Style.RESET_ALL}")
                print("---")
                cc.check_gpo_compliance()
                cc.get_stats()
                post_result_choice = post_scan_menu()
                post_scan_reset(cc)
            if post_result_choice == "3":
                exit = True
        elif choice == "5":
            exit = True
        else:  # If menu option is invalid
            print("[!] INVALID MENU OPTION\n")

    cc.log_results()  # Logs results after all scans are finished
    pass

def run_args_mode(cc, args):
    # Pick baseline_path
    if args.framework == "custom":
        if not args.baseline:
            raise SystemExit("[!] ERROR: --baseline is required with --framework custom")
        baseline_path = args.baseline
        cc.set_baseline_type("Custom")
    else:
        baseline_map = {
            "healthcare": "data/baseline_files/healthcare_baseline.csv",
            "finance":    "data/baseline_files/finance_baseline.csv",
            "enterprise": "data/baseline_files/enterprise_baseline.csv"
        }
        baseline_path = baseline_map[args.framework]
        cc.set_baseline_type(args.framework.capitalize())

    # Load args & run
    cc.get_bl_settings_and_values(baseline_path)
    cc.get_gpo_settings_and_values(args.gpo)
    cc.check_gpo_compliance()
    cc.log_results()

def main():
    parser = argparse.ArgumentParser(
        description="GPOGuard: audit AD GPO exports against a compliance baseline."
    )
    parser.add_argument(
        "-f","--framework",
        choices=["custom","healthcare","finance","enterprise"],
        help="Built-in baseline to use"
    )
    parser.add_argument(
        "-b","--baseline",
        help="Path to a custom baseline CSV (if --framework custom)."
    )
    parser.add_argument(
        "-g","--gpo",
        help="Path to your GPO .txt file."
    )
    args = parser.parse_args()

    cc = ComplianceScan()
    if args.framework and args.gpo:
        run_args_mode(cc, args)
    else:
        run_ui(cc)

if __name__ == "__main__":
    main()




