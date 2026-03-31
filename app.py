import streamlit as st
from groq import Groq
import google.generativeai as genai
from PIL import Image
import io

# ==========================================================
# 1. AÇARLAR VƏ MÜHƏRRİKLƏR
# ==========================================================
GROQ_API_KEY = "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"
GEMINI_API_KEY = "AIzaSyC3ze9DV5zdqFViVGs4vvxdvvkV5Eo-ptk" # Gemini açarın

# Groq (Mətn üçün)
groq_client = Groq(api_key=GROQ_API_KEY)

# Gemini (Şəkil üçün)
genai.configure(api_key=GEMINI_API_KEY)
vision_model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="ZƏKA ULTRA v7.0", layout="wide")
st.markdown("<h1>ZƏKA ULTRA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>HİBRİD MÜHƏRRİK: Groq + Gemini</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================================
# 2. İNTERFEYS VƏ MƏNTİQ
# ==========================================================
prompt = st.chat_input("Mesajınızı yazın...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Analiz et."
    active_file = prompt.files[0] if prompt.files else None
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"): st.write(user_text)

    with st.chat_message("assistant"):
        with st.status("🚀 Zəka Ultra işləyir...", expanded=False) as status:
            try:
                if active_file:
                    # ŞƏKİL OLSA: Gemini-yə yönləndiririk
                    st.write("🔍 Şəkil analizi (Gemini)...")
                    img = Image.open(active_file)
                    response = vision_model.generate_content([user_text, img]).text
                else:
                    # ŞƏKİL OLMASA: Groq-a yönləndiririk (Çox sürətlidir)
                    st.write("⚡ Mətn analizi (Groq)...")
                    completion = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": user_text}]
                    )
                    response = completion.choices[0].message.content
                
                status.update(label="Tamamlandı!", state="complete")
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Xəta: {str(e)}")
