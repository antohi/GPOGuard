# GPOGuard 🛡️
Python CLI tool for auto GPO compliance checks. Supports custom imported baselines as well pre-made industry specific baselines such as:
- **Healthcare** (HIPAA 164.312(b) + NIST 800‑53 AU‑2)  
- **Finance** (PCI‑DSS 8.2.3 + NIST 800‑53 IA‑5)  
- **Enterprise** (NIST 800‑53)

## Features
- **Interactive menu** for:
  - Custom baseline vs. any GPO file  
  - Healthcare (HIPAA 164.312(b) + NIST 800-53 AU-2)  
  - Finance (PCI-DSS 8.2.3 + NIST 800-53 IA-5)  
  - Enterprise (NIST 800-53)  
- **Multi-framework support** via per-baseline CSVs  
- **Parsing** of:
  - Baseline CSV → expected values, control IDs, descriptions, severity, category  
  - GPO export (`.txt`) → actual policy settings  
- **Compliance logic** that marks each setting as COMPLIANT / NOT COMPLIANT  
- **Report generation** to:
  - `reports/compliance_report.csv`  
  - `reports/compliance_report.json` 
- **Error handling** around file I/O (file exceptions won’t crash the tool)  
- **Baseline tagging** so you know which framework each row came from

## Screenshots
### Menu
![Menu](screenshots/menu.png)

### GPO Compliance
![Fin](screenshots/custom_to_finance.png)
![Fin](screenshots/again-finance-nc.png)

### JSON and CSV Reports
![JSON](screenshots/compliance_report_json.png)
![JSON](screenshots/compliance_report_csv.png)





