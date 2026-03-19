import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. DİZAYN VƏ AYARLAR ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .stChatMessage { border-radius: 12px; border: 1px solid #e2e8f0; background-color: #f8fafc !important; margin-bottom: 10px; }
    .main-title { color: #2563eb; text-align: center; font-weight: 800; font-size: 3rem; margin-top: -50px; }
    [data-testid="stSidebar"] { background-color: #f1f5f9 !important; border-right: 1px solid #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# --- 2. BEYİN VƏ YADDAŞ ---
API_KEY = "AIzaSyBiPhToQs_WMs_qtY_seJxhCEVd2r1Y7yk"
genai.configure(api_key=API_KEY)

# İşləyən modeli yaddaşda saxlayırıq ki, hər dəfə sıfırlanmasın
if "active_model" not in st.session_state:
    st.session_state.active_model = 'gemini-1.5-pro'

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. YAN PANEL ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>⚙️ Panel</h2>", unsafe_allow_html=True)
    st.info("Yaradıcı: Abdullah Mikayılov\nStatus: Ultra Aktiv")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra</h1>", unsafe_allow_html=True)

# Çat tarixçəsi
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. GİRİŞ VƏ AVTOMATİK MODEL SEÇİMİ ---
prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu şəkli analiz et."
    imgs = []
    
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=400)
            imgs.append(img)

    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        res_placeholder = st.empty()
        
        # Bu hissə "Avto-Pilot"dur. Bir model işləməsə digərinə səssizcə keçir.
        models_to_try = [st.session_state.active_model, 'gemini-1.5-flash', 'gemini-pro']
        success = False
        
        for m_name in models_to_try:
            try:
                model = genai.GenerativeModel(m_name)
                request_content = [user_text] + imgs if imgs else [user_text]
                
                response = model.generate_content(request_content, stream=True)
                
                full_res = ""
                for chunk in response:
                    if chunk.text:
                        full_res += chunk.text
                        res_placeholder.markdown(full_res + "▌")
                
                res_placeholder.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
                
                # Uğurlu oldusa, bu modeli daimi yaddaşa yaz və axtarışı dayandır
                st.session_state.active_model = m_name 
                success = True
                break 
                
            except Exception as e:
                # Əgər "not found" (404) xətasıdırsa, heç nə demə, növbəti modeli yoxla
                if "404" in str(e) or "not found" in str(e).lower():
                    continue 
                else:
                    st.error(f"Xəta baş verdi: {str(e)}")
                    success = True
                    break
                    
        if not success:
            st.error("Google serverləri hazırda bu API üçün heç bir modeli tanımadı.")
