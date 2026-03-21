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
APP_VERSION = "Global Edition 5.1 (Titan)"
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
    }

    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        transition: all 0.3s ease;
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
        if "system_logs" not in st.session_state:
            st.session_state.system_logs = [f"[{datetime.now().strftime('%H:%M:%S')}] Sistem Titan v5.1 rejimində başladıldı."]

    @staticmethod
    def add_log(msg):
        t = datetime.now().strftime("%H:%M:%S")
        st.session_state.system_logs.insert(0, f"[{t}] {msg}")

# =====================================================================
# BÖLMƏ 4: SÜNİ İNTELLEKT MÜHƏRRİKİ (404 VƏ 400 DÜZƏLİŞLƏRİ)
# =====================================================================
class AzekaEngine:
    def __init__(self, api_key, temperature):
        self.api_key = api_key
        self.temperature = temperature
        self.is_ready = False
        
        if self.api_key and len(self.api_key) > 20:
            try:
                genai.configure(api_key=self.api_key)
                self.is_ready = True
                # 🔥 BURADA DÜZƏLİŞ EDİLDİ: 'models/' prefiksi əlavə olundu
                self.model = genai.GenerativeModel(
                    model_name='models/gemini-1.5-flash',
                    system_instruction=A_ZEKA_BEYNI,
                    generation_config=genai.types.GenerationConfig(
                        temperature=self.temperature,
                    )
                )
            except Exception as e:
                GlobalSession.add_log(f"Konfiqurasiya xətası: {str(e)}")

    def generate(self, prompt, images=None):
        if not self.is_ready:
            yield "XƏTA: Sistem daxili API açarı ilə əlaqə qura bilmədi."
            return

        try:
            content_payload = [prompt]
            if images:
                content_payload.extend(images)
            
            response = self.model.generate_content(content_payload, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text

        except NotFound:
            yield "🆘 XƏTA 404: 'gemini-1.5-flash' modeli tapılmadı. Zəhmət olmasa sistem administratoru Abdullah ilə əlaqə saxlayın."
        except InvalidArgument:
            yield "❌ XƏTA 400: Daxil edilmiş API açarı etibarsızdır."
        except ResourceExhausted:
            yield "⏳ XƏTA 429: Limit dolub, az sonra yenidən yoxlayın."
        except Exception as e:
            yield f"⚠️ Gözlənilməz Xəta: {str(e)}"

# =====================================================================
# BÖLMƏ 5: İNTERFEYS KOMPONENTLƏRİ
# =====================================================================
def build_sidebar():
    with st.sidebar:
        st.markdown(f"<h2 style='text-align: center;'>👑 {APP_NAME}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>Müəllif: <b>{CREATOR}</b></p>", unsafe_allow_html=True)
        st.divider()

        st.markdown("### 🔐 Sistem Bağlantısı")
        if len(st.session_state.api_key) > 20:
            st.success("✅ Qlobal Şəbəkəyə Qoşuldu")
        else:
            st.error("❌ API Açarı Tapılmadı")

        st.divider()
        st.markdown("### ⚙️ Beyin Tənzimləmələri")
        st.session_state.temperature = st.slider("Yaradıcılıq", 0.0, 1.0, 0.7)

        st.divider()
        if st.button("🗑️ Söhbəti Təmizlə"):
            st.session_state.messages = [st.session_state.messages[0]]
            st.rerun()

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.caption(f"Versiya: {APP_VERSION}")

# =====================================================================
# BÖLMƏ 6: ƏSAS TƏTBİQ MƏNTİQİ
# =====================================================================
def main():
    apply_global_light_design()
    GlobalSession.init()
    build_sidebar()

    st.markdown(f"<div class='global-title'>{APP_NAME}</div>", unsafe_allow_html=True)
    st.markdown("<div class='global-subtitle'>Qlobal Ağıl Mərkəzi</div>", unsafe_allow_html=True)

    tab_chat, tab_analytics, tab_about = st.tabs(["💬 Canlı Söhbət", "📊 Sistem Vəziyyəti", "ℹ️ Layihə Haqqında"])

    with tab_chat:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        prompt = st.chat_input("Sualınızı yazın...", accept_file=True)

        if prompt:
            user_text = prompt.text if prompt.text else "Görüntünü analiz et."
            uploaded_imgs = []
            if prompt.files:
                for file in prompt.files:
                    uploaded_imgs.append(Image.open(file))

            st.session_state.messages.append({"role": "user", "content": user_text})
            
            with st.chat_message("user"):
                st.markdown(user_text)

            with st.chat_message("assistant"):
                res_box = st.empty()
                full_text = ""
                with st.spinner("Düşünürəm..."):
                    engine = AzekaEngine(GLOBAL_API_KEY, st.session_state.temperature)
                    for chunk in engine.generate(user_text, uploaded_imgs):
                        full_text += chunk
                        res_box.markdown(full_text + " ▌")
                    res_box.markdown(full_text)
                    st.session_state.messages.append({"role": "assistant", "content": full_text})
                    GlobalSession.add_log("Yeni cavab generasiya edildi.")

    with tab_analytics:
        st.markdown("### 📈 Sistem Metrikləri")
        c1, c2, c3 = st.columns(3)
        c1.metric("Mesaj Sayı", len(st.session_state.messages))
        c2.metric("Status", "Online")
        c3.metric("Nüvə", "Gemini 1.5 Flash")
        st.code("\n".join(st.session_state.system_logs[:15]))

    with tab_about:
        st.info(f"Yaradıcı: {CREATOR_TITLE}\nBu sistem Titan Edition protokoluna uyğun olaraq Abdullah Mikayılov tərəfindən kodlaşdırılmışdır.")

if __name__ == "__main__":
    main()
