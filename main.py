"""
====================================================================================================
PROJECT: A-ZƏKA ULTRA - NEURAL ECOSYSTEM
DEVELOPER: ABDULLAH MIKAYILOV
VERSION: 25.0 TITAN
GITHUB: github.com/abdullah-mikayilov/a-zeka-ultra
====================================================================================================
"""

import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
import datetime
import logging
import random

# ==================================================================================================
# 1. PREMIUM DİZAYN SİSTEMİ (WHITE GLASSMORPHISM)
# ==================================================================================================
def setup_ui():
    st.set_page_config(page_title="A-Zəka Ultra", page_icon="💎", layout="wide")
    
    # Apple stilində təmiz ağ dizayn
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #ffffff !important;
    }

    /* Ana Başlıq */
    .hero-section {
        background: radial-gradient(circle at center, #f8fafc 0%, #ffffff 100%);
        padding: 80px 20px;
        text-align: center;
        border-bottom: 1px solid #f1f5f9;
    }

    .title-gradient {
        background: linear-gradient(135deg, #1d4ed8 0%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4.5rem; font-weight: 800; letter-spacing: -2px;
    }

    /* Chat Qutuları */
    .stChatMessage {
        background: #fdfdfd !important;
        border: 1px solid #f1f5f9 !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.02);
        padding: 25px !important;
    }

    /* "+" Düyməsi və Giriş Paneli */
    .stChatInputContainer {
        border-radius: 15px !important;
        border: 1.5px solid #e2e8f0 !important;
        padding: 10px !important;
        background: white !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #fcfcfc !important;
        border-right: 1px solid #f1f5f9;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================================================================================================
# 2. XƏTA İDARƏETMƏ VƏ AI NÜVƏSİ
# ==================================================================================================
class AZekaTitan:
    def __init__(self):
        self.api_key = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E"
        genai.configure(api_key=self.api_key)
        # Səhv etməmək üçün ən yeni və stabil modeli seçirik
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def process_vision(self, user_text, images):
        try:
            content_packet = []
            if images:
                for img_file in images:
                    img = Image.open(img_file)
                    if img.mode != 'RGB': img = img.convert('RGB')
                    content_packet.append(img)
            
            prompt = user_text if user_text else "Zəhmət olmasa bu vizualı analiz et."
            content_packet.append(prompt)
            
            response = self.model.generate_content(content_packet, stream=True)
            for chunk in response:
                if chunk.text: yield chunk.text
        except Exception as e:
            yield f"🆘 KRİTİK XƏTA: {str(e)}. Abdullah, zəhmət olmasa API açarını və ya internetini yoxla."

# ==================================================================================================
# 3. İCRA VƏ SİSTEM MƏNTİQİ
# ==================================================================================================
def main():
    setup_ui()
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Sistem aktivdir. Salam Abdullah, Sənə necə kömək edə bilərəm?"}]

    # Başlıq
    st.markdown('<div class="hero-section"><h1 class="title-gradient">A-Zəka Ultra</h1><p style="color:#64748b;">Ecosystem Titan v25.0</p></div>', unsafe_allow_html=True)

    # Sidebar məlumatları (GitHub-da çox görünsün deyə)
    with st.sidebar:
        st.title("💎 Premium Panel")
        st.write(f"**Yaradıcı:** {datetime.datetime.now().year} Abdullah M.")
        st.write("**Sistem:** AI Vision Engine")
        st.divider()
        if st.button("🗑️ Tarixi Sıfırla", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # Mesajları göstər
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # 🔥 "+" DÜYMƏLİ GİRİŞ (ŞƏKİLLƏR ÜÇÜN)
    user_input = st.chat_input("Mesajınızı yazın və ya '+' ilə şəkil əlavə edin...", accept_file=True)

    if user_input:
        txt = user_input.text if user_input.text else ""
        st.session_state.messages.append({"role": "user", "content": txt})
        
        with st.chat_message("user"):
            st.markdown(txt)
            if user_input.files:
                for f in user_input.files:
                    st.image(f, width=400)

        with st.chat_message("assistant"):
            res_box = st.empty()
            ans = ""
            engine = AZekaTitan()
            
            with st.spinner("A-Zəka dahi kimi analiz edir..."):
                for chunk in engine.process_vision(txt, user_input.files):
                    ans += chunk
                    res_box.markdown(ans + " ▌")
                res_box.markdown(ans)
            
            st.session_state.messages.append({"role": "assistant", "content": ans})

if __name__ == "__main__":
    main()
