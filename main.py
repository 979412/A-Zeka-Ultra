import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .main-title { color: #2563eb; text-align: center; font-weight: 800; font-size: 3rem; margin-top: -50px; }
    .stChatMessage { border-radius: 10px; border: 1px solid #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# --- 2. API VƏ MODEL (SƏNİN YENİ KEYİN) ---
API_KEY = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E"
genai.configure(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. PANEL ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>⚙️ Panel</h2>", unsafe_allow_html=True)
    st.info("Yaradıcı: Abdullah Mikayılov")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra</h1>", unsafe_allow_html=True)

# Çat tarixçəsi
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. SUAL YAZMA YERİ (HEÇ VAXT İTMİR) ---
prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...")

if prompt:
    # İstifadəçi mesajını göstər
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Cavab hazırlığı
    with st.chat_message("assistant"):
        res_area = st.empty()
        full_res = ""
        
        # Ən stabil modeli birbaşa işlədirik
        try:
            # 1.5 Flash hələ aktiv deyilsə, Gemini-Pro-ya keçid edir
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt, stream=True)
            except:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_res += chunk.text
                    res_area.markdown(full_res + "▌")
            
            res_area.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            
        except Exception as e:
            st.error("Google sistemi hələ də aktivləşməyib. 5 dəqiqə gözləyib səhifəni yeniləyin.")
