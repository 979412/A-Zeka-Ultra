import streamlit as st
from groq import Groq
import base64

# --- API AYARLARI ---
client = Groq(api_key="SENIN_GROQ_API_KEY")

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

st.title("🧠 A-Zəka Ultra Vision")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- ŞƏKİL VƏ MƏTN GİRİŞİ ---
uploaded_file = st.file_uploader("Şəkil yüklə (Misal, sənəd və s.)", type=["jpg", "jpeg", "png"])
prompt = st.chat_input("Sualını yaz...")

if prompt:
    image_content = []
    
    # Əgər şəkil yüklənibsə, onu modelin başa düşəcəyi formata salırıq
    if uploaded_file:
        base64_image = encode_image(uploaded_file)
        image_content = [
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
            }
        ]
    
    # İstifadəçi mesajını yadda saxla
    user_msg = {"role": "user", "content": [{"type": "text", "text": prompt}] + image_content}
    st.session_state.messages.append(user_msg)
    
    with st.chat_message("user"):
        st.markdown(prompt)
        if uploaded_file:
            st.image(uploaded_file, caption="Yüklənən şəkil", width=300)

    # --- AI CAVABI ---
    with st.chat_message("assistant"):
        # Şəkil analizi üçün Vision modelindən istifadə edirik
        completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview", 
            messages=st.session_state.messages
        )
        response = completion.choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
