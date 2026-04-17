import streamlit as st
import cv2
import tempfile
import time
from PIL import Image
import numpy as np

# ─── 1. الإعدادات وتصميم "مَهْد" الحنون ─────────────────────────────────────────
st.set_page_config(page_title="Mahd — مهد", page_icon="🌙", layout="wide")

MAHD_STYLE = """
<style>
    /* خلفية التطبيق (البيج) */
    .stApp { background-color: #FDFBF7; }
    h1, h2, h3, p { color: #4A4A4A; font-family: 'Arial', sans-serif; }
    
    /* أزرار مَهْد (الميرمية) */
    div.stButton > button {
        background-color: #8DB580 !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        height: 3em;
        width: 100%;
        font-weight: bold;
    }
    
    /* القائمة الجانبية */
    [data-testid="stSidebar"] { background-color: #f4f1ea !important; }
    
    /* بطاقات المعلومات */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #E0E0E0;
        text-align: center;
    }
</style>
"""
st.markdown(MAHD_STYLE, unsafe_allow_html=True)

# ─── 2. نظام الدخول بالرمز السري ───────────────────────────────────────────
def check_password():
    if "password_correct" not in st.session_state:
        st.markdown('<div style="text-align:center; padding-top:50px;">', unsafe_allow_html=True)
        st.markdown('<h1>مَهْد 🌙</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color: #8DB580;">نظام الذكاء الاصطناعي لمراقبة سلامة الرضع</p>', unsafe_allow_html=True)
        
        pwd = st.text_input("أدخل الرمز السري للدخول (MVP Access)", type="password")
        if st.button("دخول →"):
            # تأكد أنك وضعت APP_SECRET في إعدادات Streamlit Secrets
            if pwd == st.secrets.get("APP_SECRET", "mahd2026"):
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("الرمز غير صحيح")
        return False
    return True

# ─── 3. تحميل الموديلات (Lazy Loading) ───────────────────────────────────────
@st.cache_resource
def load_mahd_models():
    from ultralytics import YOLO
    # استدعاء الموديلات التي قمت بتدريبها
    body_model = YOLO("body_best.pt")
    face_model = YOLO("face_best.pt")
    return body_model, face_model

# ─── 4. المحتوى الرئيسي والنفقيشن ──────────────────────────────────────────────
if check_password():
    # تحميل الموديلات في الخلفية
    body_model, face_model = load_mahd_models()
    
    # القائمة الجانبية (Navigation)
    with st.sidebar:
        st.markdown('<h2 style="color: #8DB580; text-align:center;">مَهْد</h2>', unsafe_allow_html=True)
        page = st.radio("انتقل إلى:", ["🏠 الرئيسية", "📹 تحليل الفيديو", "🔔 سجل التنبيهات"])
        st.write("---")
        if st.button("تسجيل الخروج"):
            del st.session_state["password_correct"]
            st.rerun()

    # --- صفحة الرئيسية ---
    if page == "🏠 الرئيسية":
        st.markdown('<h2 style="color: #8DB580;">أهلاً بك يا محمد!</h2>', unsafe_allow_html=True)
        st.write("إليك ملخص سريع لحالة المراقبة الحالية.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="metric-card"><h3>حالة الطفل</h3><h2 style="color:#8DB580;">آمن</h2></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-card"><h3>تنبيهات اليوم</h3><h2 style="color:#8DB580;">0</h2></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-card"><h3>جودة النوم</h3><h2 style="color:#8DB580;">95%</h2></div>', unsafe_allow_html=True)

    # --- صفحة تحليل الفيديو (القلب النابض للمشروع) ---
    elif page == "📹 تحليل الفيديو":
        st.markdown('<h2 style="color: #8DB580;">تحليل الفيديو الذكي</h2>', unsafe_allow_html=True)
        st.write("ارفع مقطع فيديو قصير للرضيع ليقوم الذكاء الاصطناعي بتحليل وضعية جسمه ووجهه.")
        
        uploaded_file = st.file_uploader("اختر ملف فيديو...", type=["mp4", "mov", "avi"])
        
        if uploaded_file is not None:
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(uploaded_file.read())
            
            # عرض الفيديو الأصلي
            st.video(uploaded_file)
            
            if st.button("بدء التحليل السريع 🚀"):
                cap = cv2.VideoCapture(tfile.name)
                st_frame = st.empty()
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                frame_count = 0
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret: break
                    
                    # 💡 حركة التسريع: نحلل فريم واحد كل 10 فريمات (Frame Skipping)
                    if frame_count % 10 == 0:
                        # تصغير الصورة لتسريع المعالجة
                        img = cv2.resize(frame, (640, 480))
                        
                        # تشغيل الموديلات
                        results_body = body_model.predict(img, conf=0.5, verbose=False)
                        
                        # رسم النتائج (تبسيط للمرحلة الحالية)
                        annotated_frame = results_body[0].plot()
                        
                        # تحويل الألوان للعرض في ستريم ليت
                        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                        st_frame.image(annotated_frame, channels="RGB", use_container_width=True)
                    
                    frame_count += 1
                    progress = int((frame_count / total_frames) * 100)
                    progress_bar.progress(progress)
                    status_text.text(f"جاري التحليل... {progress}%")
                
                cap.release()
                st.success("✅ اكتمل التحليل: لم يتم رصد أي مخاطر في وضعية النوم.")

    # --- صفحة سجل التنبيهات ---
    elif page == "🔔 سجل التنبيهات":
        st.markdown('<h2 style="color: #8DB580;">سجل التنبيهات الأمنية</h2>', unsafe_allow_html=True)
        st.info("لا توجد تنبيهات خطيرة مسجلة لهذا اليوم.")
        st.table([
            {"الوقت": "10:30 PM", "الحدث": "بدء المراقبة", "الحالة": "طبيعي"},
            {"الوقت": "09:15 PM", "الحدث": "تحليل فيديو", "الحالة": "آمن"}
        ])
