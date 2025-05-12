import os
import tempfile

import streamlit as app
from ComplianceScan import ComplianceScan

cc = ComplianceScan()

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
def run_scan(gpo_path, bf_path):
    try:
        cc.get_gpo_settings_and_values(gpo_path)
        cc.get_bl_settings_and_values(bf_path)
        cc.check_gpo_compliance(ui_mode=True)
        cc.get_stats()

        app.markdown("### [SCAN RESULTS]")
        for rec in cc.output_results:
            status = f":green[{rec['status']}]" if rec['status'] == "COMPLIANT" else f":red[{rec['status']}]"
            app.markdown(f"**{rec['setting']}** - {status}")
            with app.expander("More Information"):
                app.write(f":orange[**Expected:**] {rec['expected']}")
                app.write(f":orange[**Actual:**] {rec['actual']}")
                app.write(f":orange[**Severity:**] {rec['severity']}")
                app.write(f":blue[**AI Suggestion:**] {rec['ai_suggestion']}")
    except Exception as e:
        app.error(f"❌ Scan failed: {e}")

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
col7, col8, col9, col10,col11 = app.columns(5)
with col7:
    if app.button("💉 Healthcare (HIPAA)"):
        app.session_state.scan_mode = "healthcare"
with col9:
    if app.button("💸 Finance (PCI-DSS)"):
        app.session_state.scan_mode = "finance"
with col11:
    if app.button("💼 Enterprise (NIST)"):
        app.session_state.scan_mode = "enterprise"

if app.session_state.scan_mode == "custom":
    app.markdown("### [FILE UPLOAD]")
    baseline_file = app.file_uploader("Upload Baseline CSV", type=["csv"])
    gpo_file = app.file_uploader("Upload GPO .txt Export", type=["txt"])
    if gpo_file and baseline_file and app.button("[SCAN]", use_container_width=True):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as bf_temp:
            bf_temp.write(baseline_file.read())
            bf_path = bf_temp.name
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as gpo_temp:
            gpo_temp.write(gpo_file.read())
            gpo_path = gpo_temp.name
        run_scan(gpo_path, bf_path)

elif app.session_state.scan_mode == "healthcare":
    app.markdown("### [FILE UPLOAD]")
    gpo_file = app.file_uploader("Upload GPO .txt Export", type=["txt"])
    bl_file = "/data/baseline_files/healthcare_baseline.csv"
    if gpo_file and app.button("[SCAN]", use_container_width=True):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as gpo_temp:
            gpo_temp.write(gpo_file.read())
            gpo_path = gpo_temp.name
        run_scan(gpo_path, "../data/baseline_files/healthcare_baseline.csv")