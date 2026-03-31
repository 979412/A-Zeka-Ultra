import streamlit as st
from groq import Groq
import google.generativeai as genai
from PIL import Image
import io

# ==========================================================
# 1. AÇARLAR VƏ MÜHƏRRİKLƏR
# ==========================================================
GROQ_API_KEY = "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"
GEMINI_API_KEY = "AIzaSyC3ze9DV5zdqFViVGs4vvxdvvkV5Eo-ptk"

# Groq (Mətn üçün)
groq_client = Groq(api_key=GROQ_API_KEY)

# Gemini (Şəkil üçün)
genai.configure(api_key=GEMINI_API_KEY)
vision_model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="ZƏKA ULTRA v7.1", layout="wide")
st.markdown("<h1 style='text-align: center;'>ZƏKA ULTRA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>HİBRİD MÜHƏRRİK: Groq + Gemini</p>", unsafe_allow_html=True)

# 🧠 YADDAŞ SİSTEMİ: Köhnə mesajların silinməməsi üçün
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları ekrana yazdır (Hər dəfə yenilənəndə köhnələr qalsın)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# 2. İNTERFEYS VƏ MƏNTİQ
# ==========================================================
prompt = st.chat_input("Mesajınızı yazın...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Analiz et."
    active_file = prompt.files[0] if prompt.files else None
    
    # İstifadəçi mesajını yaddaşa əlavə et və ekrana yaz
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    # Süni İntellektin cavabı
    with st.chat_message("assistant"):
        # Status yalnız emal gedəndə görünsün
        with st.spinner("🚀 Zəka Ultra düşünür..."):
            try:
                if active_file:
                    # ŞƏKİL ANALİZİ (Gemini)
                    img = Image.open(active_file)
                    response = vision_model.generate_content([user_text, img]).text
                else:
                    # MƏTN ANALİZİ (Groq)
                    completion = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": user_text}]
                    )
                    response = completion.choices[0].message.content
                
                # 🎯 CAVABI BİRBAŞA AÇIQ GÖSTƏRİRİK (Statusun içində deyil!)
                st.markdown(response)
                
                # Cavabı yaddaşa əlavə et ki, növbəti mesajda silinməsin
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"Xəta baş verdi: {str(e)}")
