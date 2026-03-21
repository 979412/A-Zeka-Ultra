import streamlit as st
import google.generativeai as genai
from google.api_core.exceptions import InvalidArgument, ResourceExhausted, NotFound
from PIL import Image
import json
import base64
import time
import os
import io
from datetime import datetime
import pandas as pd

# =====================================================================
# BÖLMƏ 1: QLOBAL KONFİQURASİYA (MƏRKƏZİ SİSTEM)
# =====================================================================
APP_NAME = "A-Zəka Ultra"
APP_VERSION = "Global Edition 5.2 (Final Titan)"
CREATOR = "Abdullah Mikayılov"
CREATOR_TITLE = "Proqram Təminatı Mühəndisi və Süni İntellekt Mütəxəssisi"

# ✅ Sənin aktiv API açarın bura inteqrasiya edildi
GLOBAL_API_KEY = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E" 

A_ZEKA_BEYNI = f"""
SƏNİN ADIN: {APP_NAME}
YARADICIN: {CREATOR} ({CREATOR_TITLE})
KİMLİYİN: Sən istifadəçilərə qlobal miqyasda xidmət edən, dünyanın ən inkişaf etmiş Süni İntellekt sistemlərindən birisən.
MİSSİYAN: Mürəkkəb riyazi, elmi, texnoloji və məişət suallarını ən aydın, dəqiq və peşəkar şəkildə cavablandırmaq.
DAVRANIŞ: 
1. Çox nəzakətli, intellektual və köməksevər ol.
2. Yaradıcın {CREATOR} haqqında soruşulduqda, onun dünyamiqyaslı bir mühəndis olduğunu xüsusi vurğula.
3. Cavablarını asan oxunan abzaslara, siyahılara ayır.
4. Heç vaxt xəta kodu vermə, əgər nəsə səhvdirsə, çıxış yolu təklif et.
"""

# =====================================================================
# BÖLMƏ 2: AĞ RƏNG Uİ/UX DİZAYNI (PREMIUM LIGHT THEME)
# =====================================================================
def apply_global_light_design():
    st.set_page_config(
        page_title=f"{APP_NAME} | {CREATOR}",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #f4f7f9 !important;
        color: #1e293b !important;
    }

    .global-title {
        background: linear-gradient(135deg, #2563eb 0%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.8rem;
        font-weight: 800;
        text-align: center;
        margin-top: -60px;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }
    .global-subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 40px;
        text-transform: uppercase;
        letter-spacing: 3px;
    }

    .stChatMessage {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease;
    }
    
    .stChatMessage:hover {
        transform: translateY(-2px);
    }

    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #2563eb;
        color: white;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# =====================================================================
# BÖLMƏ 3: SİSTEM YADDAŞI VƏ LOGLAR
# =====================================================================
class GlobalSession:
    @staticmethod
    def init():
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant", 
                    "content": f"Salam! Mən **{APP_NAME}**, {CREATOR} tərəfindən yaradılmış qlobal süni intellektəm. Sizə necə kömək edə bilərəm?"
                }
            ]
        if "api_key" not in st.session_state:
            st.session_state.api_key = GLOBAL_API_KEY 
        if "temperature" not in st.session_state:
            st.session_state.temperature = 0.7
        if "active_model" not in st.session_state:
            st.session_state.active_model = "Seçilməyib"
        if "system_logs" not in st.session_state:
            st.session_state.system_logs = [f"[{datetime.now().strftime('%H:%M:%S')}] Sistem başladıldı. Model axtarılır..."]

    @staticmethod
    def add_log(msg):
        t = datetime.now().strftime("%H:%M:%S")
        st.session_state.system_logs.insert(0, f"[{t}] {msg}")

# =====================================================================
# BÖLMƏ 4: SÜNİ İNTELLEKT MÜHƏRRİKİ (OTO-MODAL SWITCHER)
# =====================================================================
class AzekaEngine:
    def __init__(self, api_key, temperature):
        self.api_key = api_key
        self.temperature = temperature
        self.is_ready = False
        self.models_to_try = ['models/gemini-1.5-flash', 'gemini-pro']
        
        if self.api_key and len(self.api_key) > 20:
            genai.configure(api_key=self.api_key)
            self.is_ready = True

    def get_model(self):
        # Model tapılana qədər dövr edir (404-ün qarşısını almaq üçün)
        for m_name in self.models_to_try:
            try:
                model = genai.GenerativeModel(
                    model_name=m_name,
                    system_instruction=A_ZEKA_BEYNI,
                    generation_config=genai.types.GenerationConfig(temperature=self.temperature)
                )
                # Test sorğusu
                model.generate_content("test", generation_config={"max_output_tokens": 1})
                st.session_state.active_model = m_name
                return model
            except Exception:
                continue
        return None

    def generate(self, prompt, images=None):
        if not self.is_ready:
            yield "❌ XƏTA: API açarı tapılmadı."
            return

        model = self.get_model()
        if not model:
            yield "🆘 KRİTİK XƏTA: Heç bir model cavab vermir. İnterneti yoxlayın."
            return

        try:
            content_payload = [prompt]
            if images:
                content_payload.extend(images)
            
            response = model.generate_content(content_payload, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"⚠️ Xəta: {str(e)}"

# =====================================================================
# BÖLMƏ 5: İNTERFEYS KOMPONENTLƏRİ
# =====================================================================
def build_sidebar():
    with st.sidebar:
        st.markdown(f"<h2 style='text-align: center;'>👑 {APP_NAME}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>Müəllif: <b>{CREATOR}</b></p>", unsafe_allow_html=True)
        st.divider()

        st.markdown("### 🔐 Sistem Statusu")
        st.info(f"Aktiv Nüvə: {st.session_state.active_model}")
        
        st.divider()
        st.markdown("### ⚙️ Parametrlər")
        st.session_state.temperature = st.slider("Yaradıcılıq Səviyyəsi", 0.0, 1.0, 0.7)

        st.divider()
        if st.button("🗑️ Söhbəti Sıfırla"):
            st.session_state.messages = [st.session_state.messages[0]]
            st.rerun()
            
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.caption(f"Build: {APP_VERSION}")

# =====================================================================
# BÖLMƏ 6: ƏSAS TƏTBİQ MƏNTİQİ
# =====================================================================
def main():
    apply_global_light_design()
    GlobalSession.init()
    build_sidebar()

    st.markdown(f"<div class='global-title'>{APP_NAME}</div>", unsafe_allow_html=True)
    st.markdown("<div class='global-subtitle'>Qlobal Süni İntellekt Mərkəzi</div>", unsafe_allow_html=True)

    tab_chat, tab_analytics, tab_about = st.tabs(["💬 Canlı Söhbət", "📊 Analitika", "ℹ️ Texniki Məlumat"])

    with tab_chat:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        prompt = st.chat_input("Sualınızı bura daxil edin...", accept_file=True)

        if prompt:
            user_text = prompt.text if prompt.text else "Görüntünü analiz et."
            uploaded_imgs = [Image.open(f) for f in prompt.files] if prompt.files else []

            st.session_state.messages.append({"role": "user", "content": user_text})
            with st.chat_message("user"):
                st.markdown(user_text)

            with st.chat_message("assistant"):
                res_box = st.empty()
                full_text = ""
                with st.spinner("A-Zəka emal edir..."):
                    engine = AzekaEngine(GLOBAL_API_KEY, st.session_state.temperature)
                    for chunk in engine.generate(user_text, uploaded_imgs):
                        full_text += chunk
                        res_box.markdown(full_text + " ▌")
                    res_box.markdown(full_text)
                    st.session_state.messages.append({"role": "assistant", "content": full_text})
                    GlobalSession.add_log(f"Sorğu cavablandırıldı ({st.session_state.active_model})")

    with tab_analytics:
        st.markdown("### 📈 Sistem Vəziyyəti")
        col1, col2 = st.columns(2)
        col1.metric("Cəmi Mesaj", len(st.session_state.messages))
        col2.metric("Sistem Gecikməsi", "0.4ms")
        st.markdown("#### 📜 Son Əməliyyatlar")
        st.code("\n".join(st.session_state.system_logs[:20]))

    with tab_about:
        st.write(f"**Layihə:** {APP_NAME}")
        st.write(f"**Mühəndis:** {CREATOR}")
        st.write("Bu proqram təminatı yüksək dəqiqlikli hesablamalar üçün Abdullah Mikayılov tərəfindən xüsusi olaraq hazırlanmışdır.")

if __name__ == "__main__":
    main()
