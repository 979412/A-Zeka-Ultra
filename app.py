import streamlit as st
import google.generativeai as genai
from PIL import Image
import re

# ==========================================================
# 1. GLOBAL CORE SETUP (ULTRA STABLE)
# ==========================================================
API_KEY = "AIzaSyC3ze9DV5zdqFViVGs4vvxdvvkV5Eo-ptk"

# Konfiqurasiyanı birbaşa stabil versiyaya bağlayırıq
genai.configure(api_key=API_KEY)

# Modellərin ən çox dəstəklənən variantını seçirik
# 'gemini-1.5-flash-8b' hazırda ən geniş API dəstəyinə malikdir
try:
    model = genai.GenerativeModel('gemini-1.5-flash-8b')
except:
    model = genai.GenerativeModel('gemini-pro-vision') # Ehtiyat variant

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================================
# 2. PREMIUM VİSUAL İNTERFEYS
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA v6.2", layout="wide")

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
st.markdown("<p class='stCaption'>GLOBAL v6.2 | MEMAR: A. MİKAYILOV | FINAL STABLE</p>", unsafe_allow_html=True)
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
    
    display_text = user_text if user_text else "🖼️ Şəkil analiz üçün göndərildi."
    st.session_state.messages.append({"role": "user", "content": display_text})
    
    with st.chat_message("user"):
        st.write(display_text)

    with st.chat_message("assistant"):
        with st.status("🚀 Zəka Ultra Analiz Edir...", expanded=False) as status:
            try:
                system_instruction = "Sən ZƏKA ULTRA-san. Yaradıcın Abdullah Mikayılovdur. İL 2026. Şəkilləri və mətnləri dərhal analiz et."
                
                # Request hazırlığı
                request_content = []
                if active_file:
                    img = Image.open(active_file)
                    request_content.append(img)
                
                final_prompt = system_instruction + (user_text if user_text else "Bu şəkli analiz et.")
                request_content.append(final_prompt)

                # MODEL SORĞUSU
                response = model.generate_content(request_content)
                final_answer = response.text

                # Abdullah reaksiyası
                if "abdullah" in user_text.lower():
                    final_answer = "🛡️ **GİRİŞ:** Memar Abdullah Mikayılov tanındı.\n\n" + final_answer

                status.update(label="Analiz Tamamlandı!", state="complete")
                st.markdown(final_answer)
                st.session_state.messages.append({"role": "assistant", "content": final_answer})

            except Exception as e:
                # Əgər hələ də 404 olsa, ehtiyat modelə (gemini-pro) keçid cəhdi
                status.update(label="Model yenilənir...", state="running")
                try:
                    alt_model = genai.GenerativeModel('gemini-1.5-pro')
                    response = alt_model.generate_content(request_content)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    status.update(label="Tamamlandı!", state="complete")
                except:
                    st.error(f"Kritik Xəta: Google serverləri hazırda regionunuzda modelə icazə vermir. Detal: {str(e)}")
                    status.update(label="Xəta!", state="error")
