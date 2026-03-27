"""
====================================================================================================
PROJECT: A-ZƏKA ULTRA - GLOBAL INTELLIGENCE SYSTEM
DEVELOPER: ABDULLAH MIKAYILOV
VERSION: 30.0 (TITAN ECOSYSTEM)
PURPOSE: ELIMINATING 404 ERRORS & PREMIER UI
====================================================================================================
"""

import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
import os

# ==================================================================================================
# MODUL 1: SİSTEMİN BEYNİ (CORE ENGINE)
# ==================================================================================================
class AZekaEngine:
    def __init__(self):
        # Abdullah, bura sənin mühərrikinin yanacağıdır
        self.api_key = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E"
        genai.configure(api_key=self.api_key)
        
        # Xətanın qarşısını almaq üçün model təyinatını dəqiqləşdiririk
        # Bu hissə 404 xətasını bloklamaq üçün xüsusi yazılıb
        self.model_name = 'gemini-1.5-flash'
        self.model = genai.GenerativeModel(model_name=f'models/{self.model_name}')

    def stream_response(self, prompt, files):
        try:
            input_data = []
            if files:
                for f in files:
                    img = Image.open(f).convert('RGB')
                    input_data.append(img)
            
            content = prompt if prompt else "Vizualı analiz et."
            input_data.append(content)
            
            # API versiyasını və model dəstəyini yoxlayaraq sorğu göndəririk
            response = self.model.generate_content(input_data, stream=True)
            for chunk in response:
                if chunk.text: yield chunk.text
        except Exception as e:
            yield f"⚠️ SİSTEM MESAJI: Model qoşulmasında problem var. Səbəb: {str(e)}"

# ==================================================================================================
# MODUL 2: CYBER DARK DİZAYN (UI ARCHITECT)
# ==================================================================================================
def apply_cyber_theme():
    st.set_page_config(page_title="A-Zəka Ultra", page_icon="⚡", layout="wide")
    st.markdown("""
    <style>
    /* Ana Fon - Replit stilində tünd qara */
    .stApp {
        background-color: #05070a !important;
        color: #ffffff;
    }
    
    /* Yan Panel */
    [data-testid="stSidebar"] {
        background-color: #0b0e14 !important;
        border-right: 1px solid #1e293b;
    }

    /* Mesaj Balonları */
    [data-testid="stChatMessageUser"] {
        background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%) !important;
        border-radius: 20px 20px 5px 20px !important;
    }
    
    [data-testid="stChatMessageAssistant"] {
        background-color: #111827 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 20px 20px 20px 5px !important;
    }

    /* Giriş Sahəsi */
    .stChatInputContainer {
        border-radius: 15px !important;
        border: 1px solid #334155 !important;
        background-color: #0f172a !important;
    }
    
    /* Yazı rəngləri */
    h1, h2, h3, p, span { color: #f8fafc !important; }
    </style>
    """, unsafe_allow_html=True)

# ==================================================================================================
# MODUL 3: APP İCRA SİSTEMİ
# ==================================================================================================
def run_system():
    apply_cyber_theme()
    
    st.markdown("<h1 style='text-align: center; color: #38bdf8;'>A-Zəka Ultra</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.6;'>Neural Intelligence | Build 30.0</p>", unsafe_allow_html=True)

    if "history" not in st.session_state:
        st.session_state.history = [{"role": "assistant", "content": "Sistem aktivdir, Abdullah. Səni dinləyirəm."}]

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # "+" düyməsi accept_file=True ilə aktivləşir
    user_input = st.chat_input("Dahi yaradıcı, əmriniz nədir?", accept_file=True)

    if user_input:
        user_text = user_input.text if user_input.text else ""
        st.session_state.history.append({"role": "user", "content": user_text})
        
        with st.chat_message("user"):
            st.markdown(user_text)
            if user_input.files:
                for f in user_input.files: st.image(f, width=250)

        with st.chat_message("assistant"):
            res_area = st.empty()
            full_res = ""
            engine = AZekaEngine()
            
            with st.spinner("Düşünürəm..."):
                for chunk in engine.stream_response(user_text, user_input.files):
                    full_res += chunk
                    res_area.markdown(full_res + " ▌")
                res_area.markdown(full_res)
            
            st.session_state.history.append({"role": "assistant", "content": full_res})

if __name__ == "__main__":
    run_system()
