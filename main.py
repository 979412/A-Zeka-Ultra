import streamlit as st
from groq import Groq
import base64

# --- 1. SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="A-Zəka Ultra Vision", page_icon="🧠", layout="centered")

# --- 2. DİZAYN (GÖZƏL GÖRÜNÜŞ) ---
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; padding: 10px; border: 1px solid #333; margin-bottom: 10px; }
    .stChatInputContainer { padding-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BEYİN MƏRKƏZİ (Groq API) ---
# Sənin işlək API açarını bura yerləşdirdim
api_key = "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"
client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Şəkli AI-ya göndərmək üçün hazırlayan funksiya
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# --- 4. SOL PANEL (AYARLAR) ---
with st.sidebar:
    st.title("⚙️ A-Zəka Ayarları")
    st.write("Yaradıcı: **Abdullah Mikayılov**")
    st.markdown("---")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 5. ƏSAS EKRAN ---
st.title("🧠 A-Zəka Ultra Vision")
st.caption("Şəkilləri analiz edən və sualları cavablandıran dahi AI")

# Keçmiş mesajları göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if isinstance(msg["content"], list):
            for part in msg["content"]:
                if part["type"] == "text":
                    st.markdown(part["text"])
                elif part["type"] == "image_url":
                    # Şəkil URL-dən datanı göstər
                    st.image(part["image_url"]["url"], width=300)
        else:
            st.markdown(msg["content"])

# --- 6. GİRİŞ HİSSƏSİ (Mətn və Şəkil) ---
prompt = st.chat_input("Sualını yaz və ya şəkil yüklə...", accept_file=True)

# --- 7. MƏNTİQ VƏ AI CAVABI ---
if prompt:
    user_text = prompt.text if prompt.text else "Bu şəkli analiz et."
    content_list = [{"type": "text", "text": user_text}]
    
    # Əgər şəkil yüklənibsə, onu emal et
    if prompt.files:
        for uploaded_file in prompt.files:
            if uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
                base64_image = encode_image(uploaded_file)
                content_list.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:{uploaded_file.type};base64,{base64_image}"}
                })

    # İstifadəçi mesajını yaddaşa əlavə et
    st.session_state.messages.append({"role": "user", "content": content_list})
    
    # Ekranda göstər
    with st.chat_message("user"):
        st.markdown(user_text)
        if prompt.files:
            for f in prompt.files:
                st.image(f, width=300)

    # Botun cavab vermə prosesi
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            # Əsas dəyişiklik: llama-3.2-90b-vision-preview modelindən istifadə olunur
            completion = client.chat.completions.create(
                model="llama-3.2-90b-vision-preview",
                messages=[
                    {"role": "system", "content": "Sən A-Zəka-san, dahi Abdullah Mikayılov tərəfindən yaradılmısan. Şəkilləri və misalları dərindən analiz edib, Azərbaycan dilində cavab verirsən."}
                ] + st.session_state.messages,
                stream=True
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Xəta baş verdi: {e}. VPN-i yoxlamağı unutma!")
