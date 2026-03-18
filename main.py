import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# --- 1. AYARLAR ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .stChatMessage { border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 10px; }
    .main-title { color: #2563eb; text-align: center; font-weight: 800; font-size: 3rem; }
</style>
""", unsafe_allow_html=True)

# --- 2. BEYİN ---
# Sənin işlək açarın
API_KEY = "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"
client = Groq(api_key=API_KEY)

# DİQQƏT: Groq-da hal-hazırda AKTİV olan model budur. 
# Əgər bu da silinərsə, sistem avtomatik mətn modelinə keçəcək.
VISION_MODEL = "llama-3.2-90b-vision-preview" 
TEXT_MODEL = "llama-3.3-70b-versatile"

def encode_image(image):
    buffered = io.BytesIO()
    if image.mode != 'RGB': image = image.convert('RGB')
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. PANEL ---
with st.sidebar:
    st.title("⚙️ Ayarlar")
    if st.button("🗑️ Tarixçəni Sil"):
        st.session_state.messages = []
        st.rerun()
    st.info("Yaradıcı: Abdullah Mikayılov")

st.markdown("<h1 class='main-title'>A-Zəka Ultra</h1>", unsafe_allow_html=True)

# --- 4. ÇAT ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Zəhmət olmasa bunu analiz et."
    img_b64 = None
    
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=400)
            img_b64 = encode_image(img)

    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        res_area = st.empty()
        full_res = ""
        
        try:
            # Əgər şəkil varsa, vision modelini yoxla
            if img_b64:
                msgs = [
                    {"role": "system", "content": "Sən A-Zəka-san, dahi Abdullahın köməkçisisən."},
                    {"role": "user", "content": [
                        {"type": "text", "text": user_text},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                    ]}
                ]
                model_to_use = VISION_MODEL
            else:
                # Şəkil yoxdursa, ən güclü mətn modelini istifadə et
                msgs = [{"role": "system", "content": "Sən A-Zəka-san."}] + st.session_state.messages
                model_to_use = TEXT_MODEL

            completion = client.chat.completions.create(
                model=model_to_use, messages=msgs, stream=True
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_res += chunk.choices[0].delta.content
                    res_area.markdown(full_res + "▌")
            
            res_area.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            
        except Exception as e:
            st.error(f"Xəta: {str(e)}")
            st.info("İpucu: Groq model adını yenə dəyişib. Kodu yenidən yoxlamaq lazımdır.")
