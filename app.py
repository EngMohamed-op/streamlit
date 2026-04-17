
import streamlit as st
import cv2
import numpy as np
from datetime import datetime

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Mahd — مهد", page_icon="🌙", layout="wide")

# ─── Auth Logic (Secret Code Only) ──────────────────────────────────────────
def check_password():
    """Returns True if the user had the correct password."""
    def password_entered():
        # قارن الرمز المدخل بالرمز الموجود في الـ Secrets
        if st.session_state["password"] == st.secrets["APP_SECRET"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # مسح الرمز من الذاكرة للأمان
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # شاشة الدخول الأولى
        st.markdown('<div style="text-align:center; padding-top:100px;">', unsafe_allow_html=True)
        st.markdown('<h1>🌙 Mahd · مهد</h1>', unsafe_allow_html=True)
        st.text_input("أدخل الرمز السري للدخول", type="password", on_change=password_entered, key="password")
        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.error("⚠️ الرمز السري غير صحيح")
        return False
    else:
        return st.session_state["password_correct"]

# ─── Main App ────────────────────────────────────────────────────────────────
if not check_password():
    st.stop()  # توقف هنا ولا تظهر بقية الكود إلا إذا كان الرمز صحيحاً

# ─── إذا وصل الكود هنا، يعني المستخدم أدخل الرمز الصحيح ───
st.sidebar.success("تم تسجيل الدخول بنجاح ✅")
if st.sidebar.button("تسجيل الخروج"):
    del st.session_state["password_correct"]
    st.rerun()

st.title("لوحة تحكم مَهْد 🌙")
st.write("أهلاً بك يا محمد! الآن يمكنك البدء في مراقبة حركة الطفل.")

# هنا تضع كود رفع الفيديو وتحليله (YOLOv8)
uploaded_file = st.file_uploader("ارفع فيديو مراقبة الطفل هنا", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    st.info("جاري تحليل الفيديو باستخدام موديلات مَهْد الذكية...")
    # كود المعالجة...
