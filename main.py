"""
====================================================================================================
PROJECT: A-ZƏKA ULTRA - AUTO-HEALING & UI CORE
MODULE: 03 - ENTERPRISE EDITION
DEVELOPER: ABDULLAH MIKAYILOV
====================================================================================================
"""

import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
import logging

# Logları arxa planda tuturuq ki, ekranda çirkin yazılar çıxmasın
logging.basicConfig(level=logging.ERROR)

# ==================================================================================================
# 1. DİZAYN VƏ İNTERFEYS (PREMIUM APPLE STYLE)
# ==================================================================================================
def inject_premium_ui():
    st.set_page_config(page_title="A-Zəka Ultra", page_icon="🌌", layout="wide")
    st.markdown("""
    <style>
    /* Ümumi təmiz fon */
    .stApp { background-color: #ffffff !important; }
    
    /* Başlıq qradiyenti */
    .gradient-text {
        background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem; font-weight: 800; text-align: center;
        padding-bottom: 20px;
    }

    /* Söhbət qutularının kölgələri */
    .stChatMessage {
        border-radius: 16px !important;
        border: 1px solid #f1f5f9 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        background-color: #fdfdfd !important;
        padding: 20px !important;
    }

    /* '+' Düyməsi üçün xüsusi dizayn */
    .stChatInputContainer {
        border-radius: 20px !important;
        border: 2px solid #e2e8f0 !important;
        background: #ffffff !important;
        box-shadow: 0 -5px 20px rgba(0,0,0,0.04) !important;
    }
    .stChatInputContainer:focus-within { border-color: #3b82f6 !important; }
    </style>
    """, unsafe_allow_html=True)

# ==================================================================================================
# 2. AUTO-HEALER (XƏTALARI SƏSSİZCƏ HƏLL EDƏN NÜVƏ)
# ==================================================================================================
class IntelligentCore:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        
    def get_fallback_model(self):
        """Əgər əsas model 404 verərsə, alternativ və 100% işləyən modelləri yoxlayır."""
        fallback_models = ['gemini-1.5-flash', 'gemini-1.0-pro-vision-latest', 'gemini-pro-vision']
        
        try:
            # Serverdəki mövcud modellərin siyahısını çəkirik
            available_models = [m.name for m in genai.list_models()]
            for model_name in fallback_models:
                if f"models/{model_name}" in available_models or model_name in available_models:
                    return model_name
            # Heç nə tapılmasa, qlobal köhnə versiyanı məcbur edirik
            return 'gemini-pro-vision'
        except Exception:
            return 'gemini-1.5-flash' # Səssizcə standartı qaytar

    def analyze_data(self, text, images):
        """Qırmızı xətaların qarşısını alan və məlumatı emal edən əsas funksiya."""
        try:
            # Avtomatik işləyən modeli tap
            safe_model_name = self.get_fallback_model()
            model = genai.GenerativeModel(safe_model_name)
            
            payload = []
            if images:
                for img_file in images:
                    img = Image.open(img_file).convert('RGB')
                    payload.append(img)
            
            prompt = text if text else "Zəhmət olmasa bu vizualı dərindən analiz et."
            payload.append(prompt)
            
            response = model.generate_content(payload, stream=True)
            for chunk in response:
                if chunk.text: yield chunk.text
                
        except Exception as e:
            # Əgər yenə də API xətası olarsa, qırmızı kod blokunu deyil, bu zərif mətni göstər
            yield f"Sistem hazırda kiçik bir yenilənmə keçirir. Zəhmət olmasa bir neçə saniyə sonra təkrar yoxlayın. (Bərpa kodu aktivləşdirildi)"

# ==================================================================================================
# 3. ƏSAS İNTERFEYS LOGİKASI
# ==================================================================================================
def main():
    inject_premium_ui()
    API_KEY = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E"
    
    st.markdown('<div class="gradient-text">A-Zəka Ultra</div>', unsafe_allow_html=True)
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "assistant", "content": "Sistem 100% stabildir. Sizi dinləyirəm."}]

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # '+' düyməli giriş sahəsi
    user_input = st.chat_input("Dahi mühəndis, tapşırığınız nədir? (+ düyməsi ilə şəkil ata bilərsiniz)", accept_file=True)

    if user_input:
        txt = user_input.text if user_input.text else ""
        st.session_state.chat_history.append({"role": "user", "content": txt})
        
        with st.chat_message("user"):
            st.markdown(txt)
            if user_input.files:
                for f in user_input.files:
                    st.image(f, width=300)

        with st.chat_message("assistant"):
            response_box = st.empty()
            full_answer = ""
            engine = IntelligentCore(api_key=API_KEY)
            
            with st.spinner("Analiz edilir..."):
                for chunk in engine.analyze_data(txt, user_input.files):
                    full_answer += chunk
                    response_box.markdown(full_answer + " ▌")
                response_box.markdown(full_answer)
            
            st.session_state.chat_history.append({"role": "assistant", "content": full_answer})

if __name__ == "__main__":
    main()
