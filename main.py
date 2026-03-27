import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import time

# --- KONFİQURASİYA VƏ TƏHLÜKƏSİZLİK ---
# API açarını burada qeyd edirik (Məxfi saxlayın)
API_KEY = "AIzaSyC3ze9DV5zdqFViVGs4vvxdvvkV5Eo-ptk"
genai.configure(api_key=API_KEY)

# --- SƏHİFƏ DİZAYNI (PREMIUM UI) ---
st.set_page_config(page_title="Global AI Intelligence", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    .main-title { font-size: 50px; font-weight: 800; background: -webkit-linear-gradient(#00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%); color: white; border: none; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0px 5px 15px rgba(79, 172, 254, 0.4); }
    .premium-btn>button { background: linear-gradient(90deg, #FFD700 0%, #FFA500 100%); color: black; font-weight: bold; border: 2px solid #FFD700; }
    .status-card { padding: 20px; border-radius: 15px; background: #161b22; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- ƏSAS İNTELLEKT MƏNTİQİ ---
class VisionaryAI:
    def __init__(self):
        self.model_flash = genai.GenerativeModel('gemini-1.5-flash')
        self.model_pro = genai.GenerativeModel('gemini-1.5-pro')

    def process_request(self, prompt, image=None):
        try:
            if image:
                response = self.model_flash.generate_content([prompt, image])
            else:
                response = self.model_pro.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Xəta baş verdi: {str(e)}"

ai_engine = VisionaryAI()

# --- İNTERFEYS QURULUŞU ---
st.markdown('<h1 class="main-title">GLOBAL AI INTELLIGENCE</h1>', unsafe_allow_html=True)
st.write("<p style='text-align: center;'>Dünya səviyyəli süni intellekt platformasına xoş gəldiniz.</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1.5, 1], gap="large")

with col1:
    st.markdown("### 🧠 İntellekt Mərkəzi")
    user_prompt = st.text_area("Sualınızı və ya tapşırığınızı daxil edin:", placeholder="Məsələn: Bu şəkli analiz et və ya mənə biznes plan yaz...", height=200)
    
    uploaded_file = st.file_uploader("🖼️ Analiz üçün şəkil yükləyin (Opsional)", type=['png', 'jpg', 'jpeg'])
    
    if st.button("ANALİZ ET VƏ QAZAN"):
        if user_prompt:
            with st.spinner('Süni İntellekt neyron şəbəkələrini işə salır...'):
                if uploaded_file:
                    try:
                        img = Image.open(uploaded_file)
                        result = ai_engine.process_request(user_prompt, img)
                        st.image(uploaded_file, caption='Yüklənən şəkil', use_column_width=True)
                        st.markdown(f"### ✨ Nəticə:\n{result}")
                    except Exception as e:
                        st.error(f"Şəkil analizində xəta: {e}")
                else:
                    result = ai_engine.process_request(user_prompt, None)
                    st.markdown(f"### ✨ Nəticə:\n{result}")
        else:
            st.error("Zəhmət olmasa bir mətn daxil edin!")

with col2:
    st.markdown("### 📊 Layihə Paneli")
    with st.container():
        st.markdown('<div class="status-card">', unsafe_allow_html=True)
        st.metric("Gözlənilən Gəlir", "$100,000", "+$15,400")
        st.metric("Sistem Statusu", "Aktiv", "Xətasız")
        st.progress(85, text="Məşhurluq Səviyyəsi")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 💰 Monetizasiya")
    st.info("Hazırda layihə SaaS modeli üçün hazırlanır. Tam ödəniş sistemini bağlamaq üçün Lemon Squeezy-dən ödəniş linkini koda yerləşdirməliyik.")
    
    # PUL QAZANMA DÜYMƏSİ
    # Gələcəkdə bura öz Lemon Squeezy linkinizi kopyalayacaqsınız:
    # payment_url = "https://sizin-lemon-linkiniz.lemonsqueezy.com/checkout"
    
    st.markdown("<h3>Premium Planlara Qoşulun</h3>", unsafe_allow_html=True)
    if st.button("Premium Al - $19/ay", key="payment_btn", type="primary"):
        # Bu düyməyə basanda istifadəçini ödəniş linkinə yönləndirəcək (Gələcəkdə)
        st.success("Ödəniş düyməsi yerləşdirildi. İndi Lemon Squeezy linkini gözləyirik.")
        # Hazırda istifadəçi yönləndirilmir, çünki link yoxdur.
        # Linki kopyalamaq üçün aşağıdakı sətirdəki # işarəsini silin:
        # st.markdown(f'<a href="{payment_url}" target="_blank">Ödəniş Edin</a>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<br><hr><p style='text-align: center; opacity: 0.5;'>© 2026 AI Intelligence Project. Bütün hüquqlar qorunur.</p>", unsafe_allow_html=True)
