"""
====================================================================================================
A-ZƏKA ULTRA - ADVANCED NEURAL BRIDGE
MÜHƏNDİS: ABDULLAH MİKAYILOV
SİSTEM: DARK MATTER UI & DIRECT API CONNECTION
====================================================================================================
"""

import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# ==================================================================================================
# 1. CORE CONFIGURATION & SECURITY
# ==================================================================================================
class SystemConfig:
    APP_NAME = "A-Zəka Ultra"
    VERSION = "Build 9.0.0 (Dark Core)"
    # Abdullah, əgər sistem yenə xəta versə, bu API açarını Google AI Studio-dan yenisi ilə əvəzlə!
    API_KEY = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E"
    PRIMARY_MODEL = "gemini-1.5-flash"

# ==================================================================================================
# 2. PREMIUM DARK UI (ŞƏKİL 3-DƏKİ DİZAYN)
# ==================================================================================================
def render_dark_ui():
    st.set_page_config(page_title=SystemConfig.APP_NAME, page_icon="🌌", layout="wide")
    st.markdown("""
    <style>
    /* Qlobal Qara Fon */
    .stApp {
        background-color: #0b0f19 !important;
        color: #e2e8f0;
    }
    
    /* Başlıq və Loqo */
    .cyber-title {
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem; font-weight: 800; letter-spacing: -1px;
    }
    
    /* Mesaj Qutuları (İstifadəçi - Göy, Bot - Tünd qara) */
    [data-testid="stChatMessageUser"] {
        background-color: #2563eb !important;
        border-radius: 15px 15px 0px 15px !important;
        color: white !important;
        border: none !important;
    }
    
    [data-testid="stChatMessageAssistant"] {
        background-color: #1e293b !important;
        border-radius: 15px 15px 15px 0px !important;
        border: 1px solid #334155 !important;
        color: #f8fafc !important;
    }

    /* Giriş Paneli (+) Düyməsi üçün */
    .stChatInputContainer {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================================================================================================
# 3. DIRECT NEURAL CONNECTION (TƏMİZ VƏ SÜRƏTLİ ƏLAQƏ)
# ==================================================================================================
class BrainConnection:
    def __init__(self):
        genai.configure(api_key=SystemConfig.API_KEY)
        self.model = genai.GenerativeModel(SystemConfig.PRIMARY_MODEL)

    def generate_insight(self, prompt, images):
        """Məlumatı birbaşa Google serverlərinə göndərir və cavabı alır."""
        try:
            payload = []
            if images:
                for f in images:
                    img = Image.open(f).convert('RGB')
                    payload.append(img)
            
            final_prompt = prompt if prompt else "Bu vizualı dərindən analiz et."
            payload.append(final_prompt)
            
            # Streaming bağlantısı
            response = self.model.generate_content(payload, stream=True)
            for chunk in response:
                if chunk.text: yield chunk.text
                
        except Exception as e:
            # ƏGƏR XƏTA OLARSA, DƏQİQ SƏBƏBİNİ EKRANA YAZACAQ
            error_msg = str(e)
            yield f"🆘 **CRITICAL API ERROR:** Abdullah, qoşulma baş tutmadı.\n\n**Xətanın rəsmi səbəbi:** `{error_msg}`\n\n*Həll yolu:* API açarını yeniləyin və ya 'requirements.txt' faylının düzgün olduğuna əmin olun."

# ==================================================================================================
# 4. ƏSAS İCRA (MAIN LOOP)
# ==================================================================================================
def main():
    render_dark_ui()
    
    # Başlıq
    st.markdown(f'<div class="cyber-title">{SystemConfig.APP_NAME}</div>', unsafe_allow_html=True)
    st.caption("Online | Secure Connection Established")
    
    # Söhbət Tarixçəsi
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Salam. Necə kömək edə bilərəm?"}]

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # İstifadəçi Girişi (+ düyməsi burada aktivdir)
    user_input = st.chat_input("Sualınızı bura yazın...", accept_file=True)

    if user_input:
        text = user_input.text if user_input.text else ""
        st.session_state.messages.append({"role": "user", "content": text})
        
        with st.chat_message("user"):
            st.markdown(text)
            if user_input.files:
                for f in user_input.files:
                    st.image(f, width=300)

        with st.chat_message("assistant"):
            res_box = st.empty()
            full_res = ""
            brain = BrainConnection()
            
            with st.spinner("Analiz edilir..."):
                for chunk in brain.generate_insight(text, user_input.files):
                    full_res += chunk
                    res_box.markdown(full_res + " ▌")
                res_box.markdown(full_res)
            
            st.session_state.messages.append({"role": "assistant", "content": full_res})

if __name__ == "__main__":
    main()
