
import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import time
from datetime import datetime
from pathlib import Path

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mahd — مهد",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Lazy Imports (cached) ─────────────────────────────────────────────────────
@st.cache_resource
def load_supabase():
    from supabase import create_client, Client
    url  = st.secrets["SUPABASE_URL"]
    key  = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

@st.cache_resource
def load_models():
    from ultralytics import YOLO
    body_model = YOLO("body_best.pt")
    face_model = YOLO("face_best.pt")
    return body_model, face_model

# ─── Global CSS (Mahd Identity) ───────────────────────────────────────────────
THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&display=swap');
:root {
    --bg: #FDFBF7;
    --accent: #8DB580;
    --text-main: #2A2A2A;
    --input-bg: #FFFFFF;
    --border: #D1C7BD;
}
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text-main) !important;
}
input, select, textarea {
    color: var(--text-main) !important; 
    background-color: var(--input-bg) !important;
    border: 2px solid var(--border) !important;
}
.stButton > button {
    background-color: var(--accent) !important;
    color: white !important;
    border-radius: 50px !important;
}
.mahd-card {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 20px;
}
</style>
"""
st.markdown(THEME_CSS, unsafe_allow_html=True)

# ─── Session State ────────────────────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None
if "profile" not in st.session_state:
    st.session_state.profile = None

# ─── Helpers ──────────────────────────────────────────────────────────────────
def log_alert(supabase, user_id: str, baby_name: str, status: str):
    try:
        supabase.table("alerts").insert({
            "user_id": user_id,
            "baby_name": baby_name,
            "status": status,
            "created_at": datetime.utcnow().isoformat(),
        }).execute()
    except Exception as e:
        st.warning(f"Could not log alert: {e}")

# ─── Auth Page ────────────────────────────────────────────────────────────────
def auth_page():
    supabase = load_supabase()
    col_l, col_m, col_r = st.columns([1, 2, 1])
    
    with col_m:
        st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
        st.markdown('<h1>🌙 Mahd · مهد</h1>', unsafe_allow_html=True)
        st.markdown('<p>AI-powered baby sleep safety</p>', unsafe_allow_html=True)
        
        tab_login, tab_signup = st.tabs(["🔑 Sign In", "✨ Sign Up"])

        with tab_login:
            with st.form("login_form"):
                email = st.text_input("Email / البريد الإلكتروني")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Sign In →", use_container_width=True)

            if submitted:
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.user = res.user
                    prof = supabase.table("profiles").select("*").eq("user_id", res.user.id).single().execute()
                    st.session_state.profile = prof.data
                    st.rerun()
                except Exception as e:
                    st.error(f"Login failed: {e}")

        with tab_signup:
            with st.form("signup_form"):
                mother_name = st.text_input("Mother's Name / اسم الأم")
                baby_name = st.text_input("Baby's Name / اسم الطفل")
                email_s = st.text_input("Email (login ID)")
                password_s = st.text_input("Password", type="password")
                submitted_s = st.form_submit_button("Create Account →", use_container_width=True)

            if submitted_s:
                try:
                    res = supabase.auth.sign_up({"email": email_s, "password": password_s})
                    supabase.table("profiles").insert({
                        "user_id": res.user.id,
                        "mother_name": mother_name,
                        "baby_name": baby_name,
                        "email": email_s
                    }).execute()
                    st.success("Account created! You can now sign in.")
                except Exception as e:
                    st.error(f"Sign-up failed: {e}")

# ─── Main Logic ───────────────────────────────────────────────────────────────
def main():
    if st.session_state.user is None:
        auth_page()
    else:
        st.sidebar.title("Mahd Dashboard")
        if st.sidebar.button("Logout"):
            st.session_state.user = None
            st.rerun()
        st.write(f"Welcome back, {st.session_state.profile.get('mother_name')}!")
        # (بقية كود الداشبورد وتحليل الفيديو تضاف هنا كما في النسخة السابقة)

if __name__ == "__main__":
    main()
