import os
import argparse
import textwrap

from ComplianceEngine import ComplianceEngine
from GPOParser import *
from BaselineParser import *
from colorama import Fore, Style, init
from FileUpload import *


init(autoreset=True)

def print_results(results, stats):
    for result in results:
        if result["status"] == "COMPLIANT":
            status = f"{Fore.GREEN}{result["status"]}{Style.RESET_ALL}"
        else:
            status = f"{Fore.RED}{result["status"]}{Style.RESET_ALL}"

        print(f"{Fore.LIGHTWHITE_EX}{result["setting"]}:{Style.RESET_ALL} {status}"
              f"\n{Fore.LIGHTWHITE_EX}Severity:{Style.RESET_ALL} {result["severity"]}"
              f"\n{Fore.LIGHTWHITE_EX}Description:{Style.RESET_ALL} {result["description"]}"
              f"\n{Fore.LIGHTMAGENTA_EX}AI Suggestion:{Style.RESET_ALL} {textwrap.fill(result["ai_suggestion"], width=80)}")
        print("---")
    print(f"{Fore.LIGHTWHITE_EX}\n[Controls Stats]{Style.RESET_ALL}"
          f"\nChecked: {Fore.WHITE}{stats[0]}{Style.RESET_ALL} | Compliant: {Fore.GREEN}{stats[1]}{Style.RESET_ALL} | "
          f"Non-Compliant: {Fore.RED}{stats[2]}{Style.RESET_ALL}")

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
def control_filter(ce):
    cf = input("\nControl ID Filter [Ex. \"IA-5\" | Leave blank if none]: ")
    if control_filter != "":  # If user entered a CF
        ce.apply_control_filter(cf)

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
def run_ui(ce, bp, gp, gpoe):
    gpoe.run_powershell("Get-Process | Select-Object -First 3")
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
                bl_parsed = bp.parse_bl(f"../data/baseline_files/{bl_file}")
                gp_parsed = gp.parse_gpo(f"../data/gpo_files/{gpo_file}")
                control_filter(ce)

                print(f"\n{Fore.LIGHTYELLOW_EX}[CUSTOM GPO COMPLIANCE RESULTS]{Style.RESET_ALL}")
                print("---")
                results = ce.check_compliance(gp_parsed, bl_parsed, "Custom")
                print_results(results, ce.get_stats())

                post_result_choice = post_scan_menu()
                post_scan_reset(ce)
            if post_result_choice == "3":
                exit = True
        elif choice == "2":  # Main Menu option #2 Healthcare GPO Compliance Checker
            post_result_choice = "1"
            while post_result_choice == "1":
                print(f"\n{Fore.YELLOW}=[Healthcare GPO Compliance]={Style.RESET_ALL}")
                gpo_file = gpo_file_selection()
                bl_parsed = bp.parse_bl(f"../data/baseline_files/healthcare_baseline.csv")
                gp_parsed = gp.parse_gpo(f"../data/gpo_files/{gpo_file}")
                control_filter(ce)

                print(f"\n{Fore.LIGHTYELLOW_EX}[HEALTHCARE GPO COMPLIANCE RESULTS]{Style.RESET_ALL}")
                print("---")
                results = ce.check_compliance(gp_parsed, bl_parsed, "Healthcare")
                print_results(results, ce.get_stats())

                post_result_choice = post_scan_menu()
                post_scan_reset(ce)
            if post_result_choice == "3":
                exit = True
        elif choice == "3":  # Main Menu option #3 Finance GPO Compliance Checker
            post_result_choice = "1"
            while post_result_choice == "1":
                print(f"\n{Fore.YELLOW}=[Finance GPO Compliance]={Style.RESET_ALL}")
                gpo_file = gpo_file_selection()
                bl_parsed = bp.parse_bl(f"../data/baseline_files/finance_baseline.csv")
                gp_parsed = gp.parse_gpo(f"../data/gpo_files/{gpo_file}")
                control_filter(ce)

                print(f"\n{Fore.LIGHTYELLOW_EX}[FINANCE GPO COMPLIANCE RESULTS]{Style.RESET_ALL}")
                print("---")
                results = ce.check_compliance(gp_parsed, bl_parsed, "Finance")
                print_results(results, ce.get_stats())

                post_result_choice = post_scan_menu()
                post_scan_reset(ce)
            if post_result_choice == "3":
                exit = True
        elif choice == "4":  # Main Menu option #4 Enterprise GPO Compliance Checker
            post_result_choice = "1"
            while post_result_choice == "1":
                print(f"\n{Fore.YELLOW}=[Enterprise GPO Compliance]={Style.RESET_ALL}")
                gpo_file = gpo_file_selection()
                bl_parsed = bp.parse_bl(f"../data/baseline_files/enterprise_baseline.csv")
                gp_parsed = gp.parse_gpo(f"../data/gpo_files/{gpo_file}")
                control_filter(ce)

                print(f"\n{Fore.LIGHTYELLOW_EX}[ENTERPRISE GPO COMPLIANCE RESULTS]{Style.RESET_ALL}")
                print("---")
                results = ce.check_compliance(gp_parsed, bl_parsed, "Enterprise")
                print_results(results, ce.get_stats())

                post_result_choice = post_scan_menu()
                post_scan_reset(ce)
            if post_result_choice == "3":
                exit = True
        elif choice == "5":
            exit = True
        else:  # If menu option is invalid
            print("[!] INVALID MENU OPTION\n")

    ce.log_results()  # Logs results after all scans are finished
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
    ce = ComplianceEngine()
    ce.set_ai(True)
    bp = BaselineParser()
    gp = GPOParser()
    gpoe = GPOExtractor()
    run_ui(ce, bp, gp, gpoe)

if __name__ == "__main__":
    main()




