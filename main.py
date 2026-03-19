import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. PRO DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .stChatMessage { border-radius: 12px; border: 1px solid #e2e8f0; background-color: #f8fafc !important; }
    .main-title { color: #2563eb; text-align: center; font-weight: 800; font-size: 3rem; margin-top: -50px; }
    [data-testid="stSidebar"] { background-color: #f1f5f9 !important; border-right: 1px solid #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# --- 2. AYARLAR VƏ KEY ---
API_KEY = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E"
genai.configure(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. YAN PANEL ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>⚙️ Panel</h2>", unsafe_allow_html=True)
    st.info("Yaradıcı: Abdullah Mikayılov\nStatus: Sistem Hazırdır")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra</h1>", unsafe_allow_html=True)

# Tarixçəni göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. GİRİŞ VƏ MƏNTİQ ---
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
        
        # Bu siyahıdakı modelləri tək-tək sınaqdan keçirir
        models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
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
                break
            except Exception:
                continue # Əgər 404 xətası verərsə, növbəti modelə keçir
        
        if not success:
            st.error("Google serverləri hələ də API-nı aktivləşdirməyib. Zəhmət olmasa 10 dəqiqə sonra səhifəni yeniləyin.")
