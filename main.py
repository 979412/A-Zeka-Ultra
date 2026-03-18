import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# --- 1. DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .stChatMessage { border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 10px; }
    .main-title { color: #2563eb; text-align: center; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BEYİN (STABİL MODEL) ---
API_KEY = "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"
client = Groq(api_key=API_KEY)

# BU MODEL HAZIRDA GROQ-DA ƏN STABİL VİSİON MODELİDİR
STABLE_VISION_MODEL = "llama-3.2-11b-vision-preview"

def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. PANEL ---
with st.sidebar:
    st.title("⚙️ Ayarlar")
    if st.button("🗑️ Tarixçəni Sil", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.write("Yaradıcı: **Abdullah Mikayılov**")

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra</h1>", unsafe_allow_html=True)

# Mesajlar
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. GİRİŞ ---
prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu şəkli analiz et."
    image_b64 = None
    
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=400)
            image_b64 = encode_image(img)

    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            if image_b64:
                # Şəkilli sorğu formatı
                messages = [
                    {"role": "system", "content": "Sən Abdullahın dahi A-Zəka-sısan. Şəkilləri görə bilirsən."},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_text},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                        ]
                    }
                ]
            else:
                # Sadə mətn sorğusu
                messages = [{"role": "system", "content": "Sən Abdullahın dahi A-Zəka-sısan."}] + st.session_state.messages

            completion = client.chat.completions.create(
                model=STABLE_VISION_MODEL,
                messages=messages,
                stream=True
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Xəta: {str(e)}")
