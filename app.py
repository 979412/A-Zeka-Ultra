import streamlit as st
import requests # Kitabxana əvəzinə birbaşa HTTP istifadə edirik
import base64
from PIL import Image
import io
import re

# ==========================================================
# 1. CORE CONFIGURATION
# ==========================================================
API_KEY = "AIzaSyC3ze9DV5zdqFViVGs4vvxdvvkV5Eo-ptk"
# Ən stabil API endpointi (v1beta istifadə edirik ki, 404 verməsin)
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_image_to_base64(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# ==========================================================
# 2. PREMIUM VİSUAL İNTERFEYS
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA v6.4", layout="wide")

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
st.markdown("<p class='stCaption'>GLOBAL v6.4 | MEMAR: A. MİKAYILOV | DIRECT BYPASS</p>", unsafe_allow_html=True)
st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# 3. MƏNTİQ VƏ SORĞU (REST API METHOD)
# ==========================================================
prompt = st.chat_input("Mesajınızı yazın...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu şəkli analiz et."
    active_file = prompt.files[0] if prompt.files else None
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        with st.status("🚀 Zəka Ultra Analiz Edir...", expanded=False) as status:
            try:
                # JSON Payload hazırlayırıq (Google-un tam istədiyi formatda)
                payload = {
                    "contents": [{
                        "parts": []
                    }]
                }

                # 1. Şəkil varsa əlavə et
                if active_file:
                    b64_image = encode_image_to_base64(active_file)
                    payload["contents"][0]["parts"].append({
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": b64_image
                        }
                    })

                # 2. Mətni əlavə et
                system_instruction = "Sən ZƏKA ULTRA-san. Yaradıcın Abdullah Mikayılovdur. İL 2026. "
                payload["contents"][0]["parts"].append({
                    "text": system_instruction + user_text
                })

                # 3. Birbaşa POST sorğusu göndəririk
                headers = {'Content-Type': 'application/json'}
                response = requests.post(API_URL, json=payload, headers=headers)
                result = response.json()

                # Cavabı çıxarırıq
                if "candidates" in result:
                    final_answer = result["candidates"][0]["content"]["parts"][0]["text"]
                    
                    if "abdullah" in user_text.lower():
                        final_answer = "🛡️ **GİRİŞ TƏSDİQLƏNDİ:** Abdullah Mikayılov.\n\n" + final_answer

                    status.update(label="Analiz Tamamlandı!", state="complete")
                    st.markdown(final_answer)
                    st.session_state.messages.append({"role": "assistant", "content": final_answer})
                else:
                    # Əgər yenə xəta olsa, JSON-un özünü göstər ki, problemi görək
                    st.error(f"Google API Xətası: {result.get('error', {}).get('message', 'Bilinməyən xəta')}")
                    status.update(label="Xəta!", state="error")

            except Exception as e:
                st.error(f"Sistem Xətası: {str(e)}")
                status.update(label="Xəta!", state="error")
