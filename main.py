import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
from datetime import datetime

# =====================================================================
# 1. BEYİN VƏ SİSTEM KONFİQURASİYASI
# =====================================================================
APP_NAME = "A-Zəka Ultra"
VERSION = "Titan 12.0 ProMax"
CREATOR = "Abdullah Mikayılov"
API_KEY = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E"

SYSTEM_INSTRUCTION = f"""
Sən {APP_NAME}-san. Yaradıcın dahi mühəndis {CREATOR}-dur. 
Sən dünyanın ən sürətli və vizual zəkası ən yüksək olan süni intellektisən.
Şəkilləri analiz edərkən son dərəcə detallı və peşəkar ol. Qısa, lakin dolğun cavablar ver.
"""

# =====================================================================
# 2. PREMIUM GLASSMORPHISM DİZAYN (CSS)
# =====================================================================
def inject_premium_css():
    st.set_page_config(page_title=APP_NAME, page_icon="💎", layout="wide")
    st.markdown("""
    <style>
    /* Qlobal Fon */
    .stApp {
        background: radial-gradient(circle at top left, #f8fafc, #e2e8f0);
        font-family: 'SF Pro Display', -apple-system, sans-serif;
    }
    
    /* Başlıq Dizaynı */
    .ultra-title {
        background: linear-gradient(135deg, #1e3a8a 0%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4.5rem; font-weight: 900; text-align: center;
        letter-spacing: -2px; margin-bottom: 0px; padding-top: 20px;
    }
    .ultra-subtitle {
        text-align: center; color: #64748b; font-size: 1.2rem; font-weight: 500;
        margin-bottom: 40px; letter-spacing: 1px;
    }
    
    /* Söhbət Qutuları (Glassmorphism Effekti) */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 24px !important;
        padding: 20px !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.05);
        margin-bottom: 20px;
    }
    
    /* Chat Input (Daxil etmə paneli) */
    .stChatInputContainer {
        border-radius: 30px !important;
        background: white !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08) !important;
        border: 2px solid #e2e8f0 !important;
        padding: 5px !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# =====================================================================
# 3. DAHİ VISION NÜVƏSİ (SƏHVƏ DAVAMLI)
# =====================================================================
class UltraVisionCore:
    def __init__(self, temp_value):
        # API Bağlantısını təmin edirik
        genai.configure(api_key=API_KEY)
        # Mütləq ən stabil vision modelini seçirik
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=SYSTEM_INSTRUCTION
        )
        self.temp = temp_value

    def analyze_and_respond(self, prompt_text, file_list):
        try:
            # Modelə gedəcək məlumat paketi
            payload = []
            
            # Əgər istifadəçi '+' düyməsi ilə şəkil yükləyibsə, onu paketə əlavə et
            if file_list:
                for file in file_list:
                    # Şəkli oxuyub yaddaşa alırıq
                    image = Image.open(file)
                    # Əgər şəkil çox böyükdürsə rəng rejimini tənzimləyirik ki, çökməsin
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    payload.append(image)
            
            # Sualı da paketə əlavə edirik
            payload.append(prompt_text)
            
            # Təhlükəsizlik və sürət üçün Streaming (Axın) ilə cavab alırıq
            response = self.model.generate_content(
                payload, 
                stream=True,
                generation_config=genai.types.GenerationConfig(temperature=self.temp)
            )
            
            # Cavabı hissə-hissə ekrana qaytarırıq (Donmanın qarşısını alır)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            # Xəta baş verərsə, sistemi çökdürmür, səbəbini mühəndisə deyir
            error_msg = str(e)
            if "API_KEY" in error_msg or "400" in error_msg:
                yield "⚠️ Xəta: API açarı etibarsızdır və ya şəbəkə problemi var."
            else:
                yield f"🆘 Kritik Sistem Xətası: {error_msg}. Zəhmət olmasa Replit terminalında kitabxanaları yeniləyin."

# =====================================================================
# 4. ƏSAS İNTERFEYS (UI & MƏNTİQ)
# =====================================================================
def main():
    inject_premium_css()
    
    # Söhbət tarixçəsini yadda saxlamaq üçün Session State
    if "memory" not in st.session_state:
        st.session_state.memory = [{"role": "assistant", "content": "Sistem aktivdir. Salam dahi yaradıcım! Mətn yaza və ya '+' düyməsi ilə mənə şəkil göstərə bilərsən."}]

    # --- YAN PANEL (SIDEBAR) ---
    with st.sidebar:
        st.markdown(f"<h2 style='color:#1e3a8a; text-align:center;'>⚙️ İdarəetmə Paneli</h2>", unsafe_allow_html=True)
        st.divider()
        st.write(f"**Yaradıcı Mühəndis:** {CREATOR}")
        st.write(f"**Versiya:** {VERSION}")
        
        # İntellekt səviyyəsini (Yaradıcılığı) tənzimləmək
        temperature_setting = st.slider("İntellekt Dərəcəsi", min_value=0.0, max_value=1.0, value=0.7, step=0.1, help="0: Dəqiq və riyazi, 1: Yaradıcı və sərbəst")
        
        st.divider()
        if st.button("🗑️ Yaddaşı Təmizlə", use_container_width=True):
            st.session_state.memory = [st.session_state.memory[0]]
            st.rerun()

    # --- ƏSAS EKRAN ---
    st.markdown(f"<div class='ultra-title'>{APP_NAME}</div>", unsafe_allow_html=True)
    st.markdown("<div class='ultra-subtitle'>Global Neural Architecture</div>", unsafe_allow_html=True)

    # Keçmiş mesajları ekrana çap etmək
    for message in st.session_state.memory:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- GİRİŞ PANeli (ŞƏKİL DƏSTƏYİ İLƏ) ---
    # Ən vacib sətir: accept_file=True yazılan yerin solunda '+' düyməsi yaradır
    user_query = st.chat_input("Dahi mühəndis, sualını və ya şəklini daxil et...", accept_file=True)

    if user_query:
        # 1. İstifadəçinin sorğusunu emal et
        text_content = user_query.text if user_query.text else "Bu təsvirin dərindən analizini apar."
        
        # İstifadəçi mesajını yaddaşa yaz və ekranda göstər
        st.session_state.memory.append({"role": "user", "content": text_content})
        
        with st.chat_message("user"):
            st.markdown(text_content)
            # Əgər şəkil yüklənibsə, ekranda kiçik ölçüdə göstər
            if user_query.files:
                for file in user_query.files:
                    st.image(file, width=250, caption="Analiz üçün sistemə ötürüldü")

        # 2. Süni İntellektin cavabını yarat
        with st.chat_message("assistant"):
            response_container = st.empty()
            accumulated_response = ""
            
            # Nüvəni işə salırıq
            ai_core = UltraVisionCore(temp_value=temperature_setting)
            
            start_time = time.time()
            
            with st.spinner("A-Zəka məlumatları emal edir..."):
                # Cavabı axın (stream) şəklində alırıq
                for text_chunk in ai_core.analyze_and_respond(text_content, user_query.files):
                    accumulated_response += text_chunk
                    # Kursor effekti (▌) ilə ekrana yazdırırıq
                    response_container.markdown(accumulated_response + " ▌")
                
            # Analiz bitəndə kursoru silib təmiz mətni veririk
            response_container.markdown(accumulated_response)
            
            process_time = round(time.time() - start_time, 2)
            st.caption(f"⚡ Məlumat işləndi: {process_time} saniyə")
            
            # Botun cavabını yaddaşa yaz
            st.session_state.memory.append({"role": "assistant", "content": accumulated_response})

if __name__ == "__main__":
    main()
