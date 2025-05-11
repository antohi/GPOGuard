import streamlit as app

app.set_page_config(page_title="GPOGuard", layout="centered")

col1, col2, col3= app.columns(3)
with col2:
    app.markdown(f"## :blue[{"[GPO GUARD]"}]")

col5, col4, col6 = app.columns(3)
with col4:
    app.markdown("### [SCAN SELECTION]")

custom = app.button("🔍 Run Custom Scan", use_container_width=True)





