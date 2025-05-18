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
from GPOExtractor import GPOExtractor

ce = ComplianceEngine()
ce.set_ai(True)
bp = BaselineParser()
gp = GPOParser()
gpe = GPOExtractor()

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
def run_scan(gpo_file, bf_path, bl_type):
    try:
        gp_parsed = gp.parse_gpo(gpo_file)
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

# Uploads preset baselines to flask
def upload_default_bl_to_flask(bl_type):
    # Load the hardcoded baseline file as a file-like object
    with open(f"../data/baseline_files/{bl_type}", "rb") as f:
        baseline_bytes = f.read()
        baseline_file = io.BytesIO(baseline_bytes)
        baseline_file.name = f"{bl_type}"  # Set .name so Flask accepts it

        return baseline_file

# Uploads files to flask server
def upload_to_flask(gpo_file, bl_file):
    gpo_file.seek(0)
    bl_file.seek(0)
    files = {
        "gpo_file": (gpo_file.name, gpo_file.read(), "text/plain"),
        "baseline_file": (bl_file.name, bl_file.read(), "text/csv")
    }

    response = requests.post("http://127.0.0.1:5000/upload", files=files)
    return response.json()

def ps_auto_extract_gpo():
    with app.spinner("Running PowerShell..."):
        extract_status = gpe.extract_gpo()
        app.info(extract_status)
        try:
            file = open(gpe.export_path, 'rb')
            file.name = "auto_gpo_export.txt"  # Needed for Streamlit's internal file handling
            app.session_state.gpo_file = file
            app.session_state.custom_input_mode = "auto"
        except FileNotFoundError:
            app.error("❌ Auto-extracted file not found. Make sure extraction succeeded.")

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
    # Initialize session state variables if not already set
    if "gpo_file" not in app.session_state:
        app.session_state.gpo_file = None
    if "bl_file" not in app.session_state:
        app.session_state.bl_file = None
    if "custom_input_mode" not in app.session_state:
        app.session_state.custom_input_mode = None

    app.markdown("### [SCAN MODE: CUSTOM]")

    # File selection buttons
    col1, col2, col3, col4 = app.columns(4)
    with col2:
        if app.button("Upload GPO File"):
            app.session_state.custom_input_mode = "upload"

    with col3:
        if app.button("Auto Extract GPO"):
            ps_auto_extract_gpo()

    # GPO file upload only if Upload option was selected
    if app.session_state.custom_input_mode == "upload":
        gpo_file = app.file_uploader("Upload GPO .txt Export", type=["txt"])
        if gpo_file:
            app.session_state.gpo_file = gpo_file

    # Baseline uploader
    bl_file = app.file_uploader("Upload Baseline CSV", type=["csv"])
    if bl_file:
        app.session_state.bl_file = bl_file

    # Start scan
    if app.session_state.gpo_file and app.session_state.bl_file and app.button("[SCAN]", use_container_width=True):
        with app.spinner("Uploading to Flask and scanning..."):
            try:
                paths = upload_to_flask(app.session_state.gpo_file, app.session_state.bl_file)
                run_scan(paths["gpo_file"], paths["baseline_file"], "Custom")
            except Exception as e:
                app.error(f"❌ Upload/Scan failed: {e}")

# Start healthcare logic if healthcare button selected
elif app.session_state.scan_mode == "healthcare":
    if "gpo_file" not in app.session_state:
        app.session_state.gpo_file = None
    if "bl_file" not in app.session_state:
        app.session_state.bl_file = None
    if "custom_input_mode" not in app.session_state:
        app.session_state.custom_input_mode = None

    app.markdown("### [SCAN MODE: HEALTHCARE]")
    col1, col2, col3, col4 = app.columns(4)
    with col2:
        if app.button("Upload GPO File"):
            app.session_state.custom_input_mode = "upload"
    with col3:
        if app.button("Auto Extract GPO"):
            ps_auto_extract_gpo()

    # GPO file upload only if Upload option was selected
    if app.session_state.custom_input_mode == "upload":
        gpo_file = app.file_uploader("Upload GPO .txt Export", type=["txt"])
        if gpo_file:
            app.session_state.gpo_file = gpo_file

    # SCAN logic
    if app.session_state.gpo_file and app.button("[SCAN]", use_container_width=True):
        with app.spinner("Uploading to Flask and scanning..."):
            try:
                paths = upload_to_flask(app.session_state.gpo_file,
                                        upload_default_bl_to_flask("healthcare_baseline.csv")
                                        )
                run_scan(paths["gpo_file"], paths["baseline_file"], "Healthcare")
            except Exception as e:
                app.error(f"❌ Upload/Scan failed: {e}")

# Start finance logic if finance button selected
elif app.session_state.scan_mode == "finance":
    app.session_state.gpo_file = None

    app.markdown("### [SCAN MODE: FINANCE]")
    col1, col2, col3, col4 = app.columns(4)
    with col2:
        if app.button("Upload GPO File"):
            app.session_state.gpo_file = app.file_uploader("Upload GPO .txt Export", type=["txt"])
    with col3:
        if app.button("Auto Extract GPO"):
            with app.spinner("Running PowerShell..."):
                extract_status = gpe.extract_gpo()
                app.info(extract_status)
                app.session_state.gpo_file = open(gpe.export_path, 'rb')
                app.session_state.gpo_file.name = "auto_gpo_export.txt"

    # SCAN logic
    if app.session_state.gpo_file and app.button("[SCAN]", use_container_width=True):
        with app.spinner("Uploading to Flask and scanning..."):
            try:
                paths = upload_to_flask(app.session_state.gpo_file,
                                        upload_default_bl_to_flask("finance_baseline.csv"))
                run_scan(paths["gpo_file"], paths["baseline_file"], "Finance")
            except Exception as e:
                app.error(f"❌ Upload/Scan failed: {e}")


# Start enterprise logic if enterprise button selected
elif app.session_state.scan_mode == "enterprise":
    app.session_state.gpo_file = None

    app.markdown("### [SCAN MODE: ENTERPRISE]")
    col1, col2, col3, col4 = app.columns(4)
    with col2:
        if app.button("Upload GPO File"):
            app.session_state.gpo_file = app.file_uploader("Upload GPO .txt Export", type=["txt"])
    with col3:
        if app.button("Auto Extract GPO"):
            with app.spinner("Running PowerShell..."):
                extract_status = gpe.extract_gpo()
                app.info(extract_status)
                app.session_state.gpo_file = open(gpe.export_path, 'rb')
                app.session_state.gpo_file.name = "auto_gpo_export.txt"

    # SCAN logic
    if app.session_state.gpo_file and app.button("[SCAN]", use_container_width=True):
        with app.spinner("Uploading to Flask and scanning..."):
            try:
                paths = upload_to_flask(app.session_state.gpo_file,
                                        upload_default_bl_to_flask("enterprise_baseline.csv"))
                run_scan(paths["gpo_file"], paths["baseline_file"], "Enterprise")
            except Exception as e:
                app.error(f"❌ Upload/Scan failed: {e}")
