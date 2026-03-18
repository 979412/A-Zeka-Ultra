import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# --- 1. AYARLAR VƏ DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .stChatMessage { border-radius: 15px; border: 1px solid #e2e8f0; margin-bottom: 10px; background-color: #f8fafc !important; }
    .main-title { color: #1d4ed8; text-align: center; font-weight: 800; font-size: 3rem; margin-top: -50px; }
    .stChatInputContainer { border-top: 1px solid #eee !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. BEYİN ---
API_KEY = "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"
client = Groq(api_key=API_KEY)

# Modellər
TEXT_MODEL = "llama-3.3-70b-versatile"
VISION_MODEL = "llama-3.2-11b-vision-preview"

def encode_image(image):
    buffered = io.BytesIO()
    if image.mode != 'RGB': image = image.convert('RGB')
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. PANEL ---
with st.sidebar:
    st.title("⚙️ A-Zəka")
    if st.button("🗑️ Tarixçəni Sil", use_container_width=True):
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
    user_text = prompt.text if prompt.text else ""
    img_b64 = None
    
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=400)
            img_b64 = encode_image(img)

    # Ekranda göstəriləcək mesaj
    display_msg = user_text if not img_b64 else f"🖼️ [Şəkil yükləndi] {user_text}"
    st.session_state.messages.append({"role": "user", "content": display_msg})
    
    with st.chat_message("user"):
        st.markdown(display_msg)

    with st.chat_message("assistant"):
        res_area = st.empty()
        full_res = ""
        
        try:
            # Əgər şəkil varsa VİSİON yoxla, yoxdursa birbaşa MƏTN
            if img_b64:
                try:
                    completion = client.chat.completions.create(
                        model=VISION_MODEL,
                        messages=[{"role": "user", "content": [
                            {"type": "text", "text": user_text},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                        ]}],
                        stream=True
                    )
                except:
                    # Vision xəta verərsə avtomatik mətnə keç
                    st.warning("⚠️ Groq Vision hazırda aktiv deyil. Şəkil analiz edilə bilmədi, amma sualına cavab verirəm:")
                    completion = client.chat.completions.create(
                        model=TEXT_MODEL,
                        messages=[{"role": "user", "content": user_text}],
                        stream=True
                    )
            else:
                completion = client.chat.completions.create(
                    model=TEXT_MODEL,
                    messages=[{"role": "system", "content": "Sən A-Zəka-san, Abdullah tərəfindən yaradılmısan."}] + \
                             [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]],
                    stream=True
                )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_res += chunk.choices[0].delta.content
                    res_area.markdown(full_res + "▌")
            
            res_area.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            
        except Exception as e:
            st.error("Bağışla Abdullah, sistemdə texniki nasazlıq var. Bir az sonra yoxla.")
