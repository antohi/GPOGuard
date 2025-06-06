import textwrap
from ComplianceEngine import ComplianceEngine
from GPOParser import *
from BaselineParser import *
from GPOExtractor import *
from colorama import Fore, Style, init


init(autoreset=True)

# Prints results w/ Colorama to display effectively
def print_results(results, stats):
    for result in results:
        if result["status"] == "COMPLIANT":
            status = f"{Fore.GREEN}{result["status"]}{Style.RESET_ALL}"
        else:
            status = f"{Fore.RED}{result["status"]}{Style.RESET_ALL}"

        print(f"{Fore.LIGHTWHITE_EX}{result["setting"]}:{Style.RESET_ALL} {status}"
              f"\n{Fore.LIGHTWHITE_EX}Expected:{Style.RESET_ALL} {result['expected']}"
              f"\n{Fore.LIGHTWHITE_EX}Actual:{Style.RESET_ALL} {result['actual']}"
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
    print("\nPlease choose an option:")
    print("Please select a GPO file to check for compliance (/data directory)"
          "\n\nFiles in /data/gpo_files directory:")
    print(list_files("../data/gpo_files"))  # Prints files in directory using list function
    return input("> ") # Returns user chosen gpo file

# Sends baseline and gpo files to flask server
def upload_to_flask(gpo_path, bl_path):
    try:
        with open(gpo_path, 'rb') as gpo_file, open(bl_path, 'rb') as bl_file:
            files = {
                "gpo_file": (os.path.basename(gpo_path), gpo_file, "text/plain"),
                "baseline_file": (os.path.basename(bl_path), bl_file, "text/csv")
            }
            response = requests.post("http://127.0.0.1:5000/upload", files=files)
            return response.json()
    except Exception as e:
        print(f"[!] Upload failed: {e}")
        return None

# Asks user to select a baseline file to scan GPO file against
def bl_files_selection():
    print("\nPlease select a compliance baseline (/data directory)"
          "\nFiles in /data directory:")
    print(list_files("../data/baseline_files"))  # Prints files in data directory using list function
    return input("> ")

# Checks if user would like to use a control filter
def control_filter(ce):
    cf = input("\nControl ID Filter [Ex. \"IA-5\" | Leave blank if none]: ")
    if cf != "":  # If user entered a CF
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
def run_ui(ce, bp, gp):
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
                gpo_path = gpo_file_selection()
                bl_path = bl_files_selection()
                '''
                bl_parsed = bp.parse_bl(f"../data/baseline_files/{bl_file}")
                gp_parsed = gp.parse_gpo(f"../data/gpo_files/{gpo_file}")
                '''
                paths = upload_to_flask(f"../data/gpo_files/{gpo_path}", f"../data/baseline_files/{bl_path}")
                control_filter(ce)
                print(f"\n{Fore.LIGHTYELLOW_EX}[CUSTOM GPO COMPLIANCE RESULTS]{Style.RESET_ALL}")
                print("---")
                gpo_parsed = gp.parse_gpo(paths["gpo_file"])
                bl_parsed = bp.parse_bl(paths["baseline_file"])
                results = ce.check_compliance(gpo_parsed, bl_parsed, "Custom")

                print_results(results, ce.get_stats())
                post_result_choice = post_scan_menu()
                post_scan_reset(ce)
            if post_result_choice == "3":
                exit = True

        elif choice == "2":  # Main Menu option #2 Healthcare GPO Compliance Checker
            post_result_choice = "1"
            while post_result_choice == "1":
                print(f"\n{Fore.YELLOW}=[Healthcare GPO Compliance]={Style.RESET_ALL}")
                gpo_path = gpo_file_selection()
                paths = upload_to_flask(f"../data/gpo_files/{gpo_path}", f"../data/baseline_files/healthcare_baseline.csv")
                control_filter(ce)

                print(f"\n{Fore.LIGHTYELLOW_EX}[HEALTHCARE GPO COMPLIANCE RESULTS]{Style.RESET_ALL}")
                print("---")
                gpo_parsed = gp.parse_gpo(paths["gpo_file"])
                bl_parsed = bp.parse_bl(paths["baseline_file"])
                results = ce.check_compliance(gpo_parsed, bl_parsed, "Healthcare")

                print_results(results, ce.get_stats())
                post_result_choice = post_scan_menu()
                post_scan_reset(ce)
            if post_result_choice == "3":
                exit = True
        elif choice == "3":  # Main Menu option #3 Finance GPO Compliance Checker
            post_result_choice = "1"
            while post_result_choice == "1":
                print(f"\n{Fore.YELLOW}=[Finance GPO Compliance]={Style.RESET_ALL}")
                gpo_path = gpo_file_selection()
                paths = upload_to_flask(f"../data/gpo_files/{gpo_path}", f"../data/baseline_files/finance_baseline.csv")
                control_filter(ce)

                print(f"\n{Fore.LIGHTYELLOW_EX}[FINANCE GPO COMPLIANCE RESULTS]{Style.RESET_ALL}")
                print("---")
                gpo_parsed = gp.parse_gpo(paths["gpo_file"])
                bl_parsed = bp.parse_bl(paths["baseline_file"])
                results = ce.check_compliance(gpo_parsed, bl_parsed, "Finance")

                print_results(results, ce.get_stats())
                post_result_choice = post_scan_menu()
                post_scan_reset(ce)
            if post_result_choice == "3":
                exit = True
        elif choice == "4":  # Main Menu option #4 Enterprise GPO Compliance Checker
            post_result_choice = "1"
            while post_result_choice == "1":
                print(f"\n{Fore.YELLOW}=[Enterprise GPO Compliance]={Style.RESET_ALL}")
                gpo_path = gpo_file_selection()
                paths = upload_to_flask(f"../data/gpo_files/{gpo_path}", f"../data/baseline_files/enterprise_baseline.csv")
                control_filter(ce)

                print(f"\n{Fore.LIGHTYELLOW_EX}[ENTERPRISE GPO COMPLIANCE RESULTS]{Style.RESET_ALL}")
                print("---")
                gpo_parsed = gp.parse_gpo(paths["gpo_file"])
                bl_parsed = bp.parse_bl(paths["baseline_file"])
                results = ce.check_compliance(gpo_parsed, bl_parsed, "Enterprise")

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

def main():
    ce = ComplianceEngine()
    ce.set_ai(True)
    bp = BaselineParser()
    gp = GPOParser()
    run_ui(ce, bp, gp)

if __name__ == "__main__":
    main()




