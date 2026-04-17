import streamlit as st
import cv2
import tempfile
import numpy as np
from ultralytics import YOLO
from PIL import Image

# ─── 1. تصميم مَهْد الحنون (Sage & Beige) ────────────────────────────────────────
st.set_page_config(page_title="Mahd — مهد", page_icon="🌙", layout="wide")

MAHD_STYLE = """
<style>
    .stApp { background-color: #FDFBF7; }
    h1, h2, h3, p { color: #4A4A4A; font-family: 'Arial', sans-serif; }
    div.stButton > button {
        background-color: #8DB580 !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        height: 3em; width: 100%; font-weight: bold;
    }
    [data-testid="stSidebar"] { background-color: #f4f1ea !important; }
    .metric-card {
        background-color: white; padding: 20px; border-radius: 15px;
        border: 1px solid #E0E0E0; text-align: center;
    }
</style>
"""
st.markdown(MAHD_STYLE, unsafe_allow_html=True)

# ─── 2. نظام الدخول السريع (Master Password) ──────────────────────────────────
def check_password():
    if "password_correct" not in st.session_state:
        st.markdown('<div style="text-align:center; padding-top:50px;">', unsafe_allow_html=True)
        st.markdown('<h1>مَهْد 🌙</h1>', unsafe_allow_html=True)
        pwd = st.text_input("أدخل الرمز السري للدخول", type="password")
        if st.button("دخول →"):
            if pwd == st.secrets.get("APP_SECRET", "mahd2026"):
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("الرمز غير صحيح")
        return False
    return True

# ─── 3. تحميل الموديلات ────────────────────────────────────────────────────────
@st.cache_resource
def load_mahd_models():
    try:
        body_model = YOLO("body_best.pt")
        face_model = YOLO("face_best.pt")
        return body_model, face_model
    except Exception as e:
        st.error(f"خطأ في تحميل الموديلات: تأكد من وجود الملفات في GitHub. الخطأ: {e}")
        return None, None

# ─── 4. المحتوى والنفقيشن ──────────────────────────────────────────────────────
if check_password():
    body_model, face_model = load_mahd_models()
    
    with st.sidebar:
        st.markdown('<h2 style="color: #8DB580; text-align:center;">مَهْد</h2>', unsafe_allow_html=True)
        page = st.radio("القائمة:", ["🏠 الرئيسية", "📹 تحليل الفيديو", "🔔 سجل التنبيهات"])
        if st.button("تسجيل الخروج"):
            del st.session_state["password_correct"]
            st.rerun()

    if page == "🏠 الرئيسية":
        st.markdown('<h2 style="color: #8DB580;">أهلاً بك يا محمد!</h2>', unsafe_allow_html=True)
        st.write("ملخص حالة طفلك لهذا اليوم:")
        col1, col2 = st.columns(2)
        with col1: st.markdown('<div class="metric-card"><h3>حالة النوم</h3><h2 style="color:#8DB580;">آمن</h2></div>', unsafe_allow_html=True)
        with col2: st.markdown('<div class="metric-card"><h3>التنبيهات</h3><h2 style="color:#8DB580;">0</h2></div>', unsafe_allow_html=True)

    elif page == "📹 تحليل الفيديو":
        st.markdown('<h2 style="color: #8DB580;">رصد الحركة والوضعية</h2>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("ارفع فيديو الطفل", type=["mp4", "mov", "avi"])
        
        if uploaded_file and body_model:
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(uploaded_file.read())
            
            if st.button("بدء المعالجة الذكية 🚀"):
                cap = cv2.VideoCapture(tfile.name)
                # مجهّز لعرض الصور المتحركة بالبوكسات
                st_frame = st.empty() 
                
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret: break
                    
                    # تسريع: نحلل فريم واحد كل 5 فريمات
                    if int(cap.get(cv2.CAP_PROP_POS_FRAMES)) % 5 == 0:
