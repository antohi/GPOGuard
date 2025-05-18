import json
import os
import tempfile

import requests
import streamlit as app
from BaselineParser import BaselineParser
from GPOParser import GPOParser
import io
import pandas as p
from ComplianceEngine import ComplianceEngine

ce = ComplianceEngine()
ce.set_ai(True)
bp = BaselineParser()
gp = GPOParser()

# CSS for some styling changes
app.set_page_config(page_title="GPOGuard", layout="centered")
app.markdown("""
    <style>

        /* Change all markdown header colors */
        h3, h4, h5, h6 {
            color: #df9d38 !important;
            font-family: monospace;
            text-align: center;
        }   

        /* Change button text color */
        .stButton button {
            text-align: center;
            color: white !important;
            background-color: #214985 !important;
            border-radius: 12px;
            font-weight: bold;
        }

        /* Change button hover effect */
        .stButton button:hover {
            background-color: #2c61b2 !important;
            color: #ffffff !important;
            transition: 0.2s;
            border: 2px solid #2C74B3 !important;  /* Optional: Hover border */

        }



        /* Adjust layout background (optional) */
        .stApp {
            background-color: #101010;
        }
    </style>
""", unsafe_allow_html=True)


# Calls proper ComplianceScan class methods to run logic, displays results
def run_scan(gpo_path, bf_path, bl_type):
    try:
        gp_parsed = gp.parse_gpo(gpo_path)
        bp_parsed = bp.parse_bl(bf_path)
        results = ce.check_compliance(gp_parsed, bp_parsed, bl_type)

        app.markdown("### [SCAN RESULTS]")
        for rec in results:
            status = f":green[{rec['status']}]" if rec['status'] == "COMPLIANT" else f":red[{rec['status']}]"
            app.markdown(f"**{rec['setting']}** - {status}")
            with app.expander("More Information"):
                app.write(f":orange[**Expected:**] {rec['expected']}")
                app.write(f":orange[**Actual:**] {rec['actual']}")
                app.write(f":orange[**Severity:**] {rec['severity']}")
                app.write(f":blue[**AI Suggestion:**] {rec['ai_suggestion']}")
        download_csv_json()
    except Exception as e:
        app.error(f"❌ Scan failed: {e}")


# Download option to either a csv or json file at the end of scan
def download_csv_json():
    app.markdown("### [EXPORTS]")
    df = p.DataFrame(ce.output_results)

    # CSV Download
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    app.download_button(
        label="⬇️ Export CSV",
        data=csv_buffer.getvalue(),
        file_name="gpo_compliance_results.csv",
        mime="text/csv",
        use_container_width=True
    )

    # JSON Download
    json_buffer = io.StringIO()
    json.dump(ce.output_results, json_buffer, indent=2)
    app.download_button(
        label="⬇️ Export JSON",
        data=json_buffer.getvalue(),
        file_name="gpo_compliance_results.json",
        mime="application/json",
        use_container_width=True
    )

# Uploads files to flask server
def upload_to_flask(gpo_path, bl_path):
    gpo_path.seek(0)
    bl_path.seek(0)
    files = {
        "gpo_file": (gpo_path.name, gpo_path.read(), "text/plain"),
        "baseline_file": (bl_path.name, bl_path.read(), "text/csv")
    }

    response = requests.post("http://127.0.0.1:5000/upload", files=files)
    return response.json()

'''
# Extract GPO config via PowerShell
def gpo_extraction():
    app.markdown("### [GPO Extraction]")
    if app.button("🧪 Auto Extract and Scan", use_container_width=True):
        with app.spinner("Extracting GPO and running compliance scan..."):
            try:
                extract_url = "http://127.0.0.1:5000/extract_and_upload"
                baseline_path = "../data/baseline_files/compliance_baseline.csv"

                results = requests.post(extract_url, files={"bl_path": baseline_path})
                if results.status_code == 200:
                    json_result = results.json()

                    scan_result = requests.post("http://127.0.0.1:5000/scan", json={
                        "gpo_path": json_result["gpo_path"],
                        "baseline_path": json_result["baseline_path"]
                    })

                    if scan_result.status_code == 200:
                        results = scan_result.json()
                        app.success("Scan complete.")
                        app.markdown("### [SCAN RESULTS]")
                        for rec in results:
                            status = f":green[{rec['status']}" if rec['status'] == "COMPLIANT" else f":red[{rec['status']}]"
                            app.markdown(f"**{rec['setting']}** - {status}")
                            with app.expander("More Information"):
                                app.write(f":orange[**Expected:**] {rec['expected']}")
                                app.write(f":orange[**Actual:**] {rec['actual']}")
                                app.write(f":orange[**Severity:**] {rec['severity']}")
                                app.write(f":blue[**AI Suggestion:**] {rec['ai_suggestion']}")
                    else:
                        app.error(f"Scan failed: {scan_result.text}")
                else:
                    app.error(f"Extraction/upload failed: {results.text}")

            except Exception as e:
                app.error(f"Unexpected error: {e}")

'''
# [GPO Guard] Title
app.markdown(
    """<h1 style='color:#387ADF; white-space: nowrap; text-align: center;'>[GPO GUARD]</h1>""",
    unsafe_allow_html=True
)

# Scan selection heading
app.markdown("### [SCAN SELECTION]")

if "scan_mode" not in app.session_state:
    app.session_state.scan_mode = None

# Custom scan w/ GPO and baseline exports uploads
if app.button("🔍Custom Scan", use_container_width=True):
    app.session_state.scan_mode = "custom"

# Preset industry layouts laid evenly
col7, col8, col9, col10, col11 = app.columns(5)
with col7:
    if app.button("💉 Healthcare (HIPAA)"):
        app.session_state.scan_mode = "healthcare"
with col9:
    if app.button("💸 Finance (PCI-DSS)"):
        app.session_state.scan_mode = "finance"
with col11:
    if app.button("💼 Enterprise (NIST)"):
        app.session_state.scan_mode = "enterprise"

# # Start custom scan logic if custom scan button selected
if app.session_state.scan_mode == "custom":
    app.markdown("### [FILE UPLOAD]")
    baseline_file = app.file_uploader("Upload Baseline CSV", type=["csv"])
    gpo_file = app.file_uploader("Upload GPO .txt Export", type=["txt"])
    if gpo_file and baseline_file and app.button("[SCAN]", use_container_width=True):
        with app.spinner("Uploading to Flask and scanning..."):
            try:
                paths = upload_to_flask(gpo_file, baseline_file)
                run_scan(paths["gpo_file"], paths["baseline_file"], "Custom")
            except Exception as e:
                app.error(f"❌ Upload/Scan failed: {e}")

# Start healthcare logic if healthcare button selected
elif app.session_state.scan_mode == "healthcare":
    app.markdown("### [FILE UPLOAD]")
    gpo_file = app.file_uploader("Upload GPO .txt Export", type=["txt"])
    if gpo_file and app.button("[SCAN]", use_container_width=True):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as gpo_temp:
            gpo_temp.write(gpo_file.read())
            gpo_path = gpo_temp.name
        run_scan(gpo_path, "../data/baseline_files/healthcare_baseline.csv", "Healthcare")

# Start finance logic if finance button selected
elif app.session_state.scan_mode == "finance":
    app.markdown("### [FILE UPLOAD]")
    gpo_file = app.file_uploader("Upload GPO .txt Export", type=["txt"])
    if gpo_file and app.button("[SCAN]", use_container_width=True):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as gpo_temp:
            gpo_temp.write(gpo_file.read())
            gpo_path = gpo_temp.name
        run_scan(gpo_path, "../data/baseline_files/finance_baseline.csv", "Finance")

# Start enterprise logic if enterprise button selected
elif app.session_state.scan_mode == "enterprise":
    app.markdown("### [FILE UPLOAD]")
    gpo_file = app.file_uploader("Upload GPO .txt Export", type=["txt"])
    if gpo_file and app.button("[SCAN]", use_container_width=True):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as gpo_temp:
            gpo_temp.write(gpo_file.read())
            gpo_path = gpo_temp.name
        run_scan(gpo_path, "../data/baseline_files/enterprise_baseline.csv", "Enterprise")