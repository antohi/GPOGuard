# GPOGuard
Python CLI tool for auto GPO compliance checks. Supports custom imported baselines as well pre-made industry specific baselines such as:
- **Healthcare** (HIPAA 164.312(b) + NIST 800‑53 AU‑2)  
- **Finance** (PCI‑DSS 8.2.3 + NIST 800‑53 IA‑5)  
- **Enterprise** (NIST 800‑53)

## Features
- Load any CSV baseline mapping GPO settings to expected values, framework, control IDs, descriptions, severity, and category.  
- Parse a GPO file for settings.  
- Compare actual vs expected, print pass/fail with severity & description.  
- Generate a detailed CSV audit report (`compliance_report.csv`)  

## How to Use
### 1. Clone the repo
```bash
git clone https://github.com/yourusername/GPOGuard.git
cd GPOGuard
