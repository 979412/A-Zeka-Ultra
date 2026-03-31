import streamlit as st
import google.generativeai as genai
from PIL import Image
import re

# ==========================================================
# 1. CORE SETUP
# ==========================================================
API_KEY = "AIzaSyC3ze9DV5zdqFViVGs4vvxdvvkV5Eo-ptk"
genai.configure(api_key=API_KEY)

def find_active_model():
    """Google-un icazə verdiyi istənilən modeli tapır"""
    # Yoxlanılacaq modellərin siyahısı (prioritet sırası ilə)
    test_models = [
        'gemini-1.5-pro', 
        'gemini-pro-vision', 
        'gemini-1.0-pro-vision-latest',
        'gemini-1.5-flash-8b'
    ]
    
    for m_name in test_models:
        try:
            # Modeli yoxlayırıq
            m = genai.GenerativeModel(m_name)
            # Çox kiçik bir test (xəta verib vermədiyini anlamaq üçün)
            return m, m_name
        except:
            continue
    return None, None

model, active_model_name = find_active_model()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================================
# 2. INTERFACE
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA v6.5", layout="wide")

st.markdown("<h1>ZƏKA ULTRA</h1>", unsafe_allow_html=True)
if active_model_name:
    st.caption(f"Aktiv Mühərrik: {active_model_name} | Memar: A. Mikayılov")
else:
    st.error("Kritik: Google tərəfindən heç bir model dəstəklənmir.")

# ==========================================================
# 3. LOGIC
# ==========================================================
prompt = st.chat_input("Mesajınızı yazın...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Şəkli analiz et."
    active_file = prompt.files[0] if prompt.files else None
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        with st.status("🚀 Analiz edilir...", expanded=False):
            try:
                system_instruction = "Sən ZƏKA ULTRA-san. Yaradıcın Abdullah Mikayılovdur. İL 2026."
                
                if active_file:
                    img = Image.open(active_file)
                    # Köhnə modellər (Gemini Pro Vision) üçün fərqli format lazım ola bilər
                    if "vision" in active_model_name:
                        response = model.generate_content([user_text, img])
                    else:
                        response = model.generate_content([system_instruction, user_text, img])
                else:
                    response = model.generate_content(system_instruction + user_text)

                final_answer = response.text
                st.markdown(final_answer)
                st.session_state.messages.append({"role": "assistant", "content": final_answer})
                
            except Exception as e:
                st.error(f"Bu model də xəta verdi: {str(e)}")
