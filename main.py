"""
================================================================================
LAYİHƏ: A-Zəka Ultra - Qlobal Süni İntellekt Mərkəzi
MÜHƏNDİS: Abdullah Mikayılov
PLATFORMA: GitHub / Streamlit
VERSİYA: 15.0 Enterprise Edition
TARİX: Mart, 2026

TƏSVİR: 
Bu sistem dünyanın ən qabaqcıl vizual və mətn analizi mühərriklərindən biridir.
Kod arxitekturası Obyektyönümlü Proqramlaşdırma (OOP) prinsiplərinə əsaslanır.
================================================================================
"""

import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
import logging
from datetime import datetime
import traceback

# =====================================================================
# MODUL 1: SİSTEM KONFİQURASİYASI VƏ LOQLAMA
# =====================================================================
# Logların terminalda daha yaxşı oxunması üçün konfiqurasiya
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AZeka_Ultra_Core")

class AppConfig:
    """Tətbiqin qlobal dəyişənlərini saxlayan sinif."""
    APP_NAME = "A-Zəka Ultra"
    VERSION = "15.0 Enterprise"
    CREATOR = "Abdullah Mikayılov"
    API_KEY = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E" # Təhlükəsizlik üçün bunu .env faylına keçirmək tövsiyə olunur
    MODEL_NAME = "gemini-1.5-flash"
    
    SYSTEM_INSTRUCTION = f"""
    Sən {APP_NAME} adlı, {CREATOR} tərəfindən yaradılmış qlobal və dahi süni intellektsən.
    Sənin məqsədin istifadəçinin verdiyi ən çətin sualları saniyələr içində həll etmək və göndərilən şəkilləri dərindən analiz etməkdir.
    Şəkil göndərildikdə, vizual detalları, rəngləri, mətnləri (əgər varsa) və ümumi konteksti peşəkar formada izah et.
    """

# =====================================================================
# MODUL 2: QABAQCIL FRONT-END DİZAYN (CSS INJECTION)
# =====================================================================
class UIDesigner:
    """Tətbiqin vizual interfeysini və animasiyalarını idarə edən sinif."""
    
    @staticmethod
    def inject_global_styles():
        st.set_page_config(
            page_title=AppConfig.APP_NAME, 
            page_icon="🌌", 
            layout="wide",
            initial_sidebar_state="expanded"
        )
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;500;700;900&display=swap');
        
        /* Qlobal Parametrlər */
        html, body, [class*="css"] {
            font-family: 'Montserrat', sans-serif;
            background-color: #0f172a !important; /* Koyu Göy/Qara fon */
            color: #f8fafc;
        }
        
        /* Başlıq Animasiyası və Qradiyent */
        .hero-title {
            background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 5rem; 
            font-weight: 900; 
            text-align: center;
            letter-spacing: -2px;
            padding-bottom: 10px;
            animation: fadeInDown 1s ease-out;
        }
        
        .hero-subtitle {
            text-align: center; color: #94a3b8; font-size: 1.2rem; font-weight: 500;
            margin-bottom: 50px;
        }
        
        /* Mesaj Qutuları - Premium Şüşə Effekti (Dark Glassmorphism) */
        .stChatMessage {
            background: rgba(30, 41, 59, 0.7) !important;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 20px !important;
            padding: 25px !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            margin-bottom: 25px;
            color: #f1f5f9;
        }
        
        /* Chat Giriş Sahəsi (Input) - + Düyməsi üçün xüsusi ayrılmış yer */
        .stChatInputContainer {
            border-radius: 35px !important;
            background: rgba(30, 41, 59, 0.9) !important;
            border: 2px solid #38bdf8 !important;
            padding: 8px !important;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.2) !important;
        }
        
        /* Sidebar Dizaynı */
        [data-testid="stSidebar"] {
            background: rgba(15, 23, 42, 0.95) !important;
            border-right: 1px solid rgba(255,255,255,0.05);
        }
        
        /* Metriklər üçün kartlar */
        div[data-testid="metric-container"] {
            background-color: rgba(30, 41, 59, 0.6);
            border-radius: 15px;
            padding: 15px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        /* Keyframes */
        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        </style>
        """, unsafe_allow_html=True)

# =====================================================================
# MODUL 3: SÜNİ İNTELLEKT NÜVƏSİ (ERROR HANDLING İLƏ)
# =====================================================================
class GenAICore:
    """Google Gemini API ilə əlaqə quran və məlumatları emal edən əsas nüvə."""
    
    def __init__(self, temperature_setting=0.7):
        try:
            genai.configure(api_key=AppConfig.API_KEY)
            self.model = genai.GenerativeModel(
                model_name=AppConfig.MODEL_NAME,
                system_instruction=AppConfig.SYSTEM_INSTRUCTION
            )
            self.temp = temperature_setting
            logger.info("Süni İntellekt Nüvəsi uğurla inisializasiya edildi.")
        except Exception as e:
            logger.error(f"Nüvə inisializasiya xətası: {str(e)}")
            st.error("Kritik xəta: API konfiqurasiyası uğursuz oldu.")

    def _prepare_payload(self, text_prompt, file_uploads):
        """Mətn və şəkilləri modelin oxuya biləcəyi vahid paketə yığır."""
        payload = []
        if file_uploads:
            for uploaded_file in file_uploads:
                try:
                    # Şəkli açırıq və yoxlayırıq
                    image = Image.open(uploaded_file)
                    # RGB formatına məcbur edirik ki, model xəta verməsin
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    payload.append(image)
                    logger.info(f"Şəkil uğurla emal edildi: {uploaded_file.name}")
                except Exception as img_err:
                    logger.warning(f"Şəkil oxunarkən xəta: {str(img_err)}")
                    raise Exception(f"Fayl oxunmadı: {uploaded_file.name}")
        
        payload.append(text_prompt)
        return payload

    def stream_response(self, text_prompt, file_uploads):
        """Sorğunu göndərir və cavabı hissə-hissə (stream) qaytarır."""
        try:
            payload = self._prepare_payload(text_prompt, file_uploads)
            
            response = self.model.generate_content(
                payload,
                stream=True,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temp,
                    top_p=0.9,
                    top_k=40
                )
            )
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except genai.types.generation_types.StopCandidateException:
            yield "\n[Sistem: Analiz təhlükəsizlik səbəbilə dayandırıldı.]"
        except Exception as e:
            logger.error(f"Generasiya xətası: {traceback.format_exc()}")
            if "API_KEY" in str(e):
                yield "🛑 XƏTA: API açarı tapılmadı və ya etibarsızdır."
            else:
                yield f"⚠️ Qlobal Sistem Xətası: Model bu şəkil/mətni qəbul etməkdə çətinlik çəkir. Detal: {str(e)}"

# =====================================================================
# MODUL 4: SESSİYA İDARƏETMƏSİ VƏ LOGİKA
# =====================================================================
class SessionManager:
    """Streamlit-in yaddaşını (Session State) idarə edir."""
    
    @staticmethod
    def initialize():
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": f"Sistem onlayndır. Salam, Dahi Mühəndis {AppConfig.CREATOR}! Mətn yaza və ya sol tərəfdəki **'+'** düyməsi ilə şəkil yükləyə bilərsiniz."}
            ]
        if "total_queries" not in st.session_state:
            st.session_state.total_queries = 0
            
    @staticmethod
    def add_message(role, content):
        st.session_state.messages.append({"role": role, "content": content})
        
    @staticmethod
    def increment_query():
        st.session_state.total_queries += 1

    @staticmethod
    def clear_history():
        st.session_state.messages = [st.session_state.messages[0]]
        st.session_state.total_queries = 0

# =====================================================================
# MODUL 5: ƏSAS İCRA MODULU (MAIN)
# =====================================================================
def main():
    # 1. İnterfeysi və Yaddaşı yüklə
    UIDesigner.inject_global_styles()
    SessionManager.initialize()
    
    # 2. Sidebar Konfiqurasiyası
    with st.sidebar:
        st.markdown(f"<h2 style='text-align:center; color:#38bdf8;'>⚙️ {AppConfig.APP_NAME}</h2>", unsafe_allow_html=True)
        st.caption(f"<div style='text-align:center;'>Build: {AppConfig.VERSION}</div>", unsafe_allow_html=True)
        st.divider()
        
        st.markdown("### 📊 Sistem Statusu")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Sürət", "Ultrafast", delta="Optimized")
        with col2:
            st.metric("Sorğular", st.session_state.total_queries)
            
        st.divider()
        st.markdown("### 🧠 Beyin Ayarları")
        creativity = st.slider("Yaradıcılıq (Temperature)", 0.0, 1.0, 0.7, 0.05)
        
        st.divider()
        if st.button("🗑️ Terminalı Təmizlə", use_container_width=True):
            SessionManager.clear_history()
            st.rerun()
            
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.caption(f"© 2026 | Arquitektor: **{AppConfig.CREATOR}**")

    # 3. Başlıq Paneli
    st.markdown(f"<div class='hero-title'>{AppConfig.APP_NAME}</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-subtitle'>Enterprise Vision & Intelligence Network</div>", unsafe_allow_html=True)

    # 4. Mesajların Ekrana Çıxarılması
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 5. GİRİŞ SAHƏSİ - Ən Kritik Nöqtə (accept_file=True mütləq olmalıdır)
    # Streamlit versiyası 1.39+ olduqda bu sətir avtomatik olaraq sol tərəfdə "+" düyməsi yaradacaq.
    user_input = st.chat_input("Dahi yaradıcı, əmriniz nədir? ('+' düyməsi ilə şəkil yükləyin)", accept_file=True)

    if user_input:
        # Sorğu mətnini təyin et
        prompt = user_input.text if user_input.text else "Zəhmət olmasa bu təsviri detallı şəkildə analiz et."
        
        # İstifadəçi mesajını ekrana yaz
        SessionManager.add_message("user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)
            # Əgər istifadəçi '+' ilə şəkil atıbsa, onları da göstər
            if user_input.files:
                cols = st.columns(len(user_input.files))
                for idx, file in enumerate(user_input.files):
                    with cols[idx]:
                        st.image(file, use_column_width=True, caption=f"Yükləndi: {file.name}")

        # Süni İntellektin Cavab Bölməsi
        with st.chat_message("assistant"):
            response_box = st.empty()
            full_answer = ""
            
            # Nüvəni aktivləşdiririk
            ai_engine = GenAICore(temperature_setting=creativity)
            start_timer = time.time()
            
            with st.spinner("A-Zəka məlumatları emal edir..."):
                # Cavabı axın (stream) ilə gətiririk
                for text_chunk in ai_engine.stream_response(prompt, user_input.files):
                    full_answer += text_chunk
                    response_box.markdown(full_answer + " ▌") # Kursor effekti
                    
            # Analiz bitəndə tam mətni veririk
            response_box.markdown(full_answer)
            
            # Hesablama müddəti
            elapsed_time = round(time.time() - start_timer, 2)
            st.caption(f"⚡ Məlumat işləndi: {elapsed_time} saniyə | Core: Gemini-1.5-Flash")
            
            # Yaddaşa və statistikaya əlavə et
            SessionManager.add_message("assistant", full_answer)
            SessionManager.increment_query()

# =====================================================================
# TƏTBİQİN İŞƏ SALINMASI
# =====================================================================
if __name__ == "__main__":
    main()
