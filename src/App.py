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

# [GPO Guard] Title

app.markdown(
    """<h1 style='color:#387ADF; white-space: nowrap; text-align: center;'>[GPO GUARD]</h1>""",
    unsafe_allow_html=True
)

# Scan selection heading
app.markdown("### [SCAN SELECTION]")


# Custom scan w/ GPO and baseline exports uploads
custom = app.button("🔍Custom Scan", use_container_width=True)
if "custom_scan" not in app.session_state:
    app.session_state.custom_scan = False

if custom:
    app.session_state.custom_scan = True

# Preset industry layouts laid evenly
col7, col8, col9, col10,col11 = app.columns(5)
with col7:
    app.button("💉 Healthcare (HIPAA)")
with col9:
    app.button("💸 Finance (PCI-DSS)")
with col11:
    app.button("💼 Enterprise (NIST)")

if app.session_state.custom_scan:
    # Baseline and GPO uploads
    app.markdown("### [FILE UPLOAD]")
    baseline_file = app.file_uploader("Upload Baseline CSV", type=["csv"])
    gpo_file = app.file_uploader("Upload GPO .txt Export", type=["txt"])

    scan = app.button("[SCAN]", use_container_width=True)
    if gpo_file and baseline_file:
        if scan:
            with tempfile.NamedTemporaryFile(delete=False, suffix="csv") as bf_temp:
                bf_temp.write(baseline_file.read())
                bf_path = bf_temp.name

            with tempfile.NamedTemporaryFile(delete=False, suffix="txt") as gpo_temp:
                gpo_temp.write(gpo_file.read())
                gpo_path = gpo_temp.name
            try:
                """
                app.write("Reading GPO file...")
                cc.get_gpo_settings_and_values(gpo_path)

                app.write("Reading baseline CSV...")
                cc.get_bl_settings_and_values(bf_path)

                app.write("Running compliance check...")
                cc.check_gpo_compliance()

                app.write("Compliance check complete.")
                cc.get_stats()

                app.markdown("### [SCAN RESULTS]")
                """
                for rec in cc.output_results:
                    app.markdown(f"**{rec['setting']}** - {rec['status']}")
                    with app.expander("Details"):
                        app.write(f"**Expected:** {rec['expected']}")
                        app.write(f"**Actual:** {rec['actual']}")
                        app.write(f"**Severity:** {rec['severity']}")
                        app.write(f"**AI Suggestion:** {rec['ai_suggestion']}")
            except Exception as e:
                app.error(f"❌ Scan failed: {e}")
