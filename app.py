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

# 📜 SİSTEM TƏLİMATI: AI-nin şəxsiyyətini burada təyin edirik
SYSTEM_PROMPT = """
Sən ZƏKA ULTRA-san. Yaradıcın Abdullah Mikayılovdur. İL 2026. 
Həmişə Azərbaycan dilində, aydın və professional cavab ver. 
Əgər kimsə səndən kim olduğunu soruşsa, yaradıcının Abdullah olduğunu fəxrlə vurğula.
"""

st.set_page_config(page_title="ZƏKA ULTRA v7.2", layout="wide")
st.markdown("<h1 style='text-align: center;'>ZƏKA ULTRA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>HİBRİD MÜHƏRRİK: Groq + Gemini</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj tarixçəsini ekranda saxla
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
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        with st.spinner("🚀 Zəka Ultra düşünür..."):
            try:
                if active_file:
                    # ŞƏKİL ANALİZİ (Gemini) + Sistem Təlimatı
                    img = Image.open(active_file)
                    # Gemini-yə həm şəkli, həm təlimatı, həm də istifadəçinin sualını veririk
                    full_prompt = f"{SYSTEM_PROMPT}\n\nİstifadəçinin sualı: {user_text}"
                    response = vision_model.generate_content([full_prompt, img]).text
                else:
                    # MƏTN ANALİZİ (Groq) + Sistem Təlimatı
                    completion = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT}, # Groq üçün sistem rolu
                            {"role": "user", "content": user_text}
                        ]
                    )
                    response = completion.choices[0].message.content
                
                # Cavabı birbaşa göstər
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"Xəta baş verdi: {str(e)}")
