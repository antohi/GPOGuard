import streamlit as app

app.set_page_config(page_title="GPOGuard", layout="centered")

# [GPO Guard] Title
col1, col2, col3= app.columns(3)
with col2:
    app.markdown(f"## :blue[{"[GPO GUARD]"}]")

# Scan selection heading
col5, col4, col6 = app.columns(3)
with col4:
    app.markdown("### [SCAN SELECTION]")

# Custom scan w/ GPO and baseline exports uploads
custom = app.button("🔍 Run Custom Scan", use_container_width=True)

# Preset industry layouts laid evenly
col7, col8, col9, col10,col11 = app.columns(5)
with col7:
    app.button("🏥 Healthcare (HIPAA)")
with col9:
    app.button("💳 Finance (PCI-DSS)")
with col11:
    app.button("🏢 Enterprise (NIST)")





