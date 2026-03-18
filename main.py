import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# --- 1. GÜCLÜ VƏ ŞİFFFAF DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .stChatMessage { border-radius: 10px; border: 1px solid #d1d5db; background: white !important; }
    .main-title { color: #1e40af; text-align: center; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BEYİN MƏRKƏZİ ---
# Sənin işlək API açarın
API_KEY = "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"
client = Groq(api_key=API_KEY)

# DİQQƏT: Şəkil üçün bu model mütləqdir. Əgər bu işləməsə, Groq-da vision icazən yoxdur deməkdir.
VISION_MODEL = "llama-3.2-90b-vision-preview" 

def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. YAN PANEL ---
with st.sidebar:
    st.markdown("### ⚙️ Ayarlar")
    if st.button("🗑️ Tarixçəni Sil", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.write("Yaradıcı: **Abdullah Mikayılov**")

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra Alim</h1>", unsafe_allow_html=True)

# Mesajları göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. GİRİŞ (+) ---
prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Zəhmət olmasa bu şəkli analiz et."
    image_b64 = None
    
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=400)
            image_b64 = encode_image(img)

    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    # --- 5. VISION MƏNTİQİ ---
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            # Əgər şəkil varsa, vision formatında göndər
            if image_b64:
                messages = [
                    {"role": "system", "content": "Sən Abdullahın yaratdığı dahi A-Zəka-san. Şəkli görə bilirsən."},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_text},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                        ]
                    }
                ]
            else:
                messages = [{"role": "system", "content": "Sən Abdullahın dahi A-Zəka-sısan."}] + st.session_state.messages

            completion = client.chat.completions.create(
                model=VISION_MODEL,
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
            st.info("İpucu: Əgər 404 xətası alırsansa, Groq-da bu modelə girişin yoxdur.")
