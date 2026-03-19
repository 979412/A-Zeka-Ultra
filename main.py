import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. ULTRA MODERN İNTERFEYS ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background: white; }
    .main-title { 
        color: #2563eb; text-align: center; font-weight: 900; 
        font-size: 3.5rem; margin-top: -60px;
    }
    .stChatMessage { border-radius: 15px; background: #f1f5f9 !important; border: none !important; }
    .stChatInputContainer { border-top: 2px solid #2563eb !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. GÜCLÜ API BAĞLANTISI ---
API_KEY = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E"
genai.configure(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. PANEL ---
with st.sidebar:
    st.title("🚀 A-Zəka Pro")
    st.success("Yaradıcı: Abdullah Mikayılov")
    st.write("Sistem: 1.0s Cavab Rejimi")
    if st.button("🗑️ Tarixçəni Sil", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra</h1>", unsafe_allow_html=True)

# Çat Tarixçəsi
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. ANALİZ VƏ ANLIQ CAVAB MEXANİZMİ ---
prompt = st.chat_input("Sualını bura yaz, Abdullah...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        res_area = st.empty()
        full_res = ""
        
        # Saniyəlik keçid sistemi
        # Ən sürətli modeldən başlayaraq yoxlayır
        brain_models = ['gemini-1.5-flash', 'gemini-pro']
        
        found = False
        for m_name in brain_models:
            if found: break
            try:
                # Modeli çağırırıq
                model = genai.GenerativeModel(m_name)
                
                # Cavabı parçalarla (stream) gətiririk ki, donmasın
                response = model.generate_content(prompt, stream=True)
                
                for chunk in response:
                    if chunk.text:
                        full_res += chunk.text
                        res_area.markdown(full_res + "▌")
                
                res_area.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
                found = True
            except:
                # Əgər model "naz" eləsə, Abdullah heç nə görmür, sistem növbəti modeli yoxlayır
                continue
        
        if not found:
            res_area.error("Hazırda Google-un bütün beyinləri məşğuldur. Zəhmət olmasa 10 saniyə sonra yenidən cəhd et.")
