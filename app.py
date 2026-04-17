import streamlit as st
import cv2
import tempfile
import time
import numpy as np
from ultralytics import YOLO

# ─── 1. تصميم هوية مَهْد (Sage & Beige) ────────────────────────────────────────
st.set_page_config(page_title="Mahd — مهد", page_icon="🌙", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #FDFBF7; }
    h1, h2, h3, p { color: #4A4A4A; font-family: 'Arial', sans-serif; }
    div.stButton > button {
        background-color: #8DB580 !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        height: 3.5em; width: 100%; font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #7A9D6E !important; }
    [data-testid="stSidebar"] { background-color: #f4f1ea !important; }
    .metric-card {
        background-color: white; padding: 25px; border-radius: 15px;
        border: 1px solid #E1D7C6; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ─── 2. نظام الدخول بالرمز السري ───────────────────────────────────────────
def check_password():
    if "password_correct" not in st.session_state:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div style="text-align:center; padding-top:50px;">', unsafe_allow_html=True)
            st.markdown('<h1 style="font-size: 3em;">مَهْد 🌙</h1>', unsafe_allow_html=True)
            st.markdown('<p style="color: #8DB580; font-size: 1.2em;">نظام الذكاء الاصطناعي لحماية الرضع</p>', unsafe_allow_html=True)
            
            pwd = st.text_input("أدخل الرمز السري للدخول", type="password")
            if st.button("دخول إلى المنصة"):
                if pwd == st.secrets.get("APP_SECRET", "mahd2026"):
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("⚠️ الرمز غير صحيح، حاول مرة أخرى")
            return False
    return True

# ─── 3. تحميل الموديلات (Cached) ─────────────────────────────────────────────
@st.cache_resource
def load_mahd_models():
    try:
        # تأكد أن هذه الملفات مرفوعة في المجلد الرئيسي على GitHub
        body_model = YOLO("body_best.pt")
        face_model = YOLO("face_best.pt")
        return body_model, face_model
    except Exception as e:
        st.error(f"⚠️ فشل تحميل الموديلات. تأكد من وجود الملفات .pt بجانب الكود. {e}")
        return None, None

# ─── 4. التطبيق الرئيسي والنفقيشن ──────────────────────────────────────────────
if check_password():
    body_model, face_model = load_mahd_models()
    
    # القائمة الجانبية الأنيقة
    with st.sidebar:
        st.markdown('<h2 style="color: #8DB580; text-align:center;">القائمة</h2>', unsafe_allow_html=True)
        page = st.radio("", ["🏠 الرئيسية", "📹 تحليل الفيديو", "🔔 سجل التنبيهات"])
        st.write("---")
        if st.button("تسجيل الخروج"):
            del st.session_state["password_correct"]
            st.rerun()

    # --- صفحة الرئيسية ---
    if page == "🏠 الرئيسية":
        st.markdown('<h2 style="color: #8DB580;">أهلاً بك يا محمد!</h2>', unsafe_allow_html=True)
        st.write("إحصائيات المراقبة اليومية لمشروع مَهْد:")
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown('<div class="metric-card"><h3>حالة الرضيع</h3><h2 style="color:#8DB580;">آمن ✅</h2></div>', unsafe_allow_html=True)
        with col2: st.markdown('<div class="metric-card"><h3>تنبيهات نشطة</h3><h2 style="color:#E67E22;">0</h2></div>', unsafe_allow_html=True)
        with col3: st.markdown('<div class="metric-card"><h3>جودة النوم</h3><h2 style="color:#8DB580;">98%</h2></div>', unsafe_allow_html=True)

    # --- صفحة تحليل الفيديو (النسخة الانسيابية السلسة) ---
    elif page == "📹 تحليل الفيديو":
        st.markdown('<h2 style="color: #8DB580;">تحليل الفيديو والرصد اللحظي</h2>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("ارفع فيديو لمراقبة الطفل", type=["mp4", "mov", "avi"])
        
        if uploaded_file and body_model:
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(uploaded_file.read())
            
            if st.button("بدء المعالجة الذكية 🚀"):
                cap = cv2.VideoCapture(tfile.name)
                st_frame = st.empty() # مكان عرض "الفيديو" المتحدث
                
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret: break
                    
                    # 💡 سر الانسيابية: معالجة فريم كل 2 فريمات (توازن بين السرعة والحركة)
                    if int(cap.get(cv2.CAP_PROP_POS_FRAMES)) % 2 == 0:
                        
                        # تصغير الصورة لزيادة سرعة الـ Rendering في المتصفح
                        frame_resized = cv2.resize(frame, (640, 480))
                        img_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
                        
                        # تشغيل الموديل ورسم البوكس
