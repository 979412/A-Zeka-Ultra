import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .stChatMessage { border-radius: 12px; border: 1px solid #e2e8f0; background-color: #f8fafc !important; }
    .main-title { color: #2563eb; text-align: center; font-weight: 800; font-size: 3rem; margin-top: -50px; }
    [data-testid="stSidebar"] { background-color: #f1f5f9 !important; border-right: 1px solid #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# --- 2. BEYİN SİSTEMİ (İNADKAR REJİM) ---
API_KEY = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E"
genai.configure(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. PANEL ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>⚙️ Panel</h2>", unsafe_allow_html=True)
    st.info(f"Yaradıcı: Abdullah Mikayılov\nStatus: Aktiv")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra</h1>", unsafe_allow_html=True)

# Çat tarixçəsi
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. GİRİŞ VƏ ÇOXLU MODEL YOXLANIŞI ---
prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Zəhmət olmasa bu mediaya bax."
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
        res_area = st.empty()
        full_res = ""
        
        # BURA DİQQƏT: Əgər biri işləməsə, o birini yoxlayır
        models_to_try = ['gemini-1.5-flash', 'gemini-pro']
        success = False
        
        for m_name in models_to_try:
            try:
                model = genai.GenerativeModel(m_name)
                input_data = [user_text] + imgs if imgs else [user_text]
                
                response = model.generate_content(input_data, stream=True)
                
                for chunk in response:
                    if chunk.text:
                        full_res += chunk.text
                        res_area.markdown(full_res + "▌")
                
                res_area.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
                success = True
                break # Uğurlu oldusa, dövrədən çıx
                
            except Exception as e:
                # 404 xətası olsa, səssizcə növbəti modeli yoxla
                if "404" in str(e) or "not found" in str(e).lower():
                    continue
                else:
                    st.error(f"Xəta: {str(e)}")
                    break
        
        if not success:
            st.error("⚠️ Təəssüf ki, Google hələ də bu API açarı üçün modelləri tam aktivləşdirməyib. 5 dəqiqə gözləyib yenidən yoxlayın.")
