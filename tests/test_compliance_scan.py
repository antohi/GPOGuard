import csv
import json
import os
import pytest
from src.ComplianceScan import ComplianceScan

@pytest.fixture
def sample_baseline_csv(tmp_path):
    p = tmp_path / "baseline.csv"
    p.write_text(
        "SettingName,ExpectedValue,Framework,ControlID,Description,Severity,Category\n"
        "MinLen,8,TEST,ID-1,Test desc,Low,AccessControl\n"
    )
    return str(p)

@pytest.fixture
def sample_gpo_file(tmp_path):
    p = tmp_path / "gpo.txt"
    p.write_text("MinLen = 8\nOtherSetting = 5\n")
    return str(p)

def test_compliance_and_output(tmp_path, sample_baseline_csv, sample_gpo_file):
    cc = ComplianceScan()
    cc.set_baseline_type("Test")
    cc.get_bl_settings_and_values(sample_baseline_csv)
    cc.get_gpo_settings_and_values(sample_gpo_file)

    cc.check_gpo_compliance()

    assert len(cc.output_results) == 1
    rec = cc.output_results[0]
    assert rec["setting"] == "MinLen"
    assert rec["status"] == "COMPLIANT"

    csv_path = tmp_path / "report.csv"
    json_path = tmp_path / "report.json"

    cc._csv_path = str(csv_path)
    cc._json_path = str(json_path)
