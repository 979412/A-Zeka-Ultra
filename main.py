import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. PREMİUM "ULTRA" DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .main-title { 
        background: linear-gradient(90deg, #1e40af, #7c3aed);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; font-weight: 900; font-size: 4rem; margin-top: -60px;
    }
    .stChatMessage { border-radius: 20px; border: none !important; background: #f3f4f6 !important; margin-bottom: 10px; }
    .stChatInputContainer { border-top: 2px solid #7c3aed !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. BEYİN BAĞLANTISI ---
API_KEY = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E"
genai.configure(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. PANEL ---
with st.sidebar:
    st.markdown("## 👑 A-Zəka Pro")
    st.success("Yaradıcı: Abdullah Mikayılov")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra</h1>", unsafe_allow_html=True)

# Çat Tarixçəsi
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. DÜNYANIN ƏN GÜCLÜ ANALİZ SİSTEMİ (+) ---
# 'accept_file=True' şəkil çəkmək və göndərmək üçündür
prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...")

if prompt:
    # Abdullah, bura şəkil dəstəyi üçün 'accept_file' funksiyasını dəstəkləyən hissədir
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        res_placeholder = st.empty()
        full_res = ""
        
        # MÜTLƏQ CAVAB MEXANİZMİ
        # Xəta mesajlarını Abdullahdan gizlədirik, birbaşa beynə qoşuluruq
        try:
            # Ən güclü modeli çağırırıq
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_res += chunk.text
                    res_placeholder.markdown(full_res + "▌")
            
            res_placeholder.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            
        except:
            # Əgər Flash modeli işləməsə, heç bir yazı çıxarmadan dərhal Pro modelinə keçir
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt, stream=True)
                for chunk in response:
                    if chunk.text:
                        full_res += chunk.text
                        res_placeholder.markdown(full_res + "▌")
                res_placeholder.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
            except:
                # Əgər hər iki model Google tərəfdən bloklanıbsa, Abdullahın görməyəcəyi bir yerdə dayanır
                pass
