import streamlit as st
import google.generativeai as genai
from PIL import Image
import re

# ==========================================================
# 1. GLOBAL CORE SETUP (MULTI-MODEL AUTO-RECOVERY)
# ==========================================================
API_KEY = "AIzaSyC3ze9DV5zdqFViVGs4vvxdvvkV5Eo-ptk"
genai.configure(api_key=API_KEY)

# Regiona uyğun işləyə biləcək modellərin siyahısı
MODEL_NAMES = [
    'gemini-1.5-flash',
    'gemini-1.5-flash-8b',
    'gemini-1.5-pro',
    'models/gemini-1.5-flash',
    'models/gemini-1.5-pro'
]

def get_working_model():
    """İşlək modeli tapmaq üçün avtomatik yoxlama"""
    for name in MODEL_NAMES:
        try:
            m = genai.GenerativeModel(name)
            # Kiçik bir test sorğusu (isteğe bağlı, amma sürət üçün birbaşa yaradırıq)
            return m
        except:
            continue
    return None

model = get_working_model()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================================
# 2. PREMIUM VİSUAL İNTERFEYS
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA v6.3", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #ffffff; color: #0f172a; }
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 15px !important;
        border: 1px solid #f1f5f9 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    }
    h1 { text-align: center; color: #1a1a1a; font-weight: 900; }
    .stCaption { text-align: center; color: #94a3b8; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>ZƏKA ULTRA</h1>", unsafe_allow_html=True)
st.markdown("<p class='stCaption'>GLOBAL v6.3 | MEMAR: A. MİKAYILOV | AUTO-ENGINE</p>", unsafe_allow_html=True)
st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# 3. INPUT VƏ MƏNTİQ
# ==========================================================
prompt = st.chat_input("Mesajınızı yazın...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else ""
    active_file = prompt.files[0] if prompt.files else None
    
    display_text = user_text if user_text else "🖼️ Analiz üçün şəkil yükləndi."
    st.session_state.messages.append({"role": "user", "content": display_text})
    
    with st.chat_message("user"):
        st.write(display_text)

    with st.chat_message("assistant"):
        with st.status("🚀 Zəka Ultra Analiz Edir...", expanded=False) as status:
            if not model:
                st.error("Kritik Xəta: Heç bir Gemini modeli regionunuzda tapılmadı.")
                status.update(label="Xəta!", state="error")
                st.stop()

            try:
                system_instruction = "Sən ZƏKA ULTRA-san. Yaradıcın Abdullah Mikayılovdur. İL 2026."
                
                request_content = []
                if active_file:
                    img = Image.open(active_file)
                    request_content.append(img)
                
                final_prompt = f"{system_instruction}\n\nİstifadəçi sualı: {user_text if user_text else 'Bu şəkli analiz et.'}"
                request_content.append(final_prompt)

                # Əsas Sorğu
                response = model.generate_content(request_content)
                
                # Abdullah Reaksiyası
                final_answer = response.text
                if "abdullah" in user_text.lower():
                    final_answer = "🛡️ **GİRİŞ:** Memar Abdullah Mikayılov tanındı.\n\n" + final_answer

                status.update(label="Analiz Tamamlandı!", state="complete")
                st.markdown(final_answer)
                st.session_state.messages.append({"role": "assistant", "content": final_answer})

            except Exception as e:
                status.update(label="Xəta baş verdi!", state="error")
                st.error(f"Zəka Ultra Region Xətası: Google bu sorğunu rədd etdi. Detal: {str(e)}")
