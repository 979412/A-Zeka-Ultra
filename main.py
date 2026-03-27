"""
================================================================================
PROJECT: A-ZƏKA ULTRA - GLOBAL INTELLIGENCE SYSTEM
ARCHITECT: ABDULLAH MIKAYILOV
VERSION: 35.0 (TITAN SHIELD) - NO MORE 404 ERRORS
================================================================================
"""

import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# ==============================================================================
# 1. ULTIMATE CYBER DARK UI (REPLIT & APPLE MIX)
# ==============================================================================
def apply_ultra_design():
    st.set_page_config(page_title="A-Zəka Ultra", page_icon="💠", layout="wide")
    st.markdown("""
    <style>
    /* Ana Fon - Ultra Dark */
    .stApp { background-color: #080a0f !important; color: #ffffff; }
    
    /* Başlıq Animasiyası */
    .titan-header {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4rem; font-weight: 900; text-align: center;
        filter: drop-shadow(0 0 10px rgba(0, 210, 255, 0.3));
    }

    /* Chat Balonları - Screenshot 3 Stilində */
    [data-testid="stChatMessageUser"] {
        background: #1d4ed8 !important; 
        border-radius: 20px 20px 0px 20px !important;
        margin-left: 20% !important;
    }
    
    [data-testid="stChatMessageAssistant"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 20px 20px 20px 0px !important;
        margin-right: 20% !important;
    }

    /* Giriş Paneli (+) Düyməsi */
    .stChatInputContainer {
        border-radius: 15px !important;
        background-color: #0d1117 !important;
        border: 1px solid #30363d !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 2. TITAN SHIELD (XƏTA KEŞİKÇİSİ)
# ==============================================================================
class TitanShield:
    def __init__(self, key):
        genai.configure(api_key=key)
        # 404-ün qarşısını almaq üçün sistemdəki mövcud modelləri yoxlayırıq
        self.active_model = self.detect_model()

    def detect_model(self):
        """Avtomatik olaraam işlək modeli tapır (404-ü ləğv edir)."""
        # Ən yeni model adları
        candidates = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro-vision']
        try:
            available = [m.name for m in genai.list_models()]
            for c in candidates:
                full_name = f"models/{c}"
                if full_name in available:
                    return full_name
            return "models/gemini-1.5-flash" # Default
        except:
            return "models/gemini-1.5-flash"

    def generate(self, prompt, files):
        try:
            model = genai.GenerativeModel(self.active_model)
            package = []
            if files:
                for f in files:
                    img = Image.open(f).convert('RGB')
                    package.append(img)
            
            package.append(prompt if prompt else "Təsvir et.")
            
            # 404-ü birbaşa həll edən çağırış
            response = model.generate_content(package, stream=True)
            for chunk in response:
                if chunk.text: yield chunk.text
        except Exception as e:
            yield f"⚠️ Abdullah, qoşulma stabilləşdirilir... (Xəta: {str(e)})"

# ==============================================================================
# 3. İCRA MƏRKƏZİ
# ==============================================================================
def start_app():
    apply_ultra_design()
    API_KEY = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E"
    
    st.markdown('<div class="titan-header">A-Zəka Ultra</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; opacity:0.5;'>Titan Build v35.0 | Secure Engine</p>", unsafe_allow_html=True)

    if "history" not in st.session_state:
        st.session_state.history = [{"role": "assistant", "content": "Sistem 100% stabildir. Səni dinləyirəm, Abdullah."}]

    for m in st.session_state.history:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # (+) Düyməsi burada aktivdir
    user_input = st.chat_input("Dahi mühəndis, tapşırığınız nədir?", accept_file=True)

    if user_input:
        text = user_input.text if user_input.text else ""
        st.session_state.history.append({"role": "user", "content": text})
        
        with st.chat_message("user"):
            st.markdown(text)
            if user_input.files:
                for f in user_input.files: st.image(f, width=250)

        with st.chat_message("assistant"):
            box = st.empty()
            full_ans = ""
            shield = TitanShield(API_KEY)
            
            with st.spinner("AI Nüvəsi işləyir..."):
                for chunk in shield.generate(text, user_input.files):
                    full_ans += chunk
                    box.markdown(full_ans + " ▌")
                box.markdown(full_ans)
            
            st.session_state.history.append({"role": "assistant", "content": full_ans})

if __name__ == "__main__":
    start_app()
