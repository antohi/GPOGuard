# GPOGuard

## Data Files
+ `compliance_baseline.csv`: Defines required baseline settings mapped to NIST 800-53 controls, used to evaluate policy compliance.
+ `lab_policy_compliant.txt`: Exported security policy from Active Directory lab that shows a compliant configuration.
+ `lab_policy_noncompliant.txt`: Modified export used to simulate policy misconfigurations and test detection logic.

## Source Code
+ `ComplianceChecker.py`: Maps compliance_baseline.csv into a dictionary in order to check if GPOs have a compliant configuration.
+ `Main.py`: User Interface of the program.
