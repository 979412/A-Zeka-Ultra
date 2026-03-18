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
    .stChatMessage { border-radius: 15px; border: 1px solid #eee; margin-bottom: 10px; }
    .main-title { color: #2563eb; text-align: center; font-weight: 800; font-size: 3rem; }
</style>
""", unsafe_allow_html=True)

# --- 2. BEYİN MƏRKƏZİ ---
API_KEY = "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"
client = Groq(api_key=API_KEY)

# Yoxlanılacaq modellərin siyahısı (Groq-un silmə ehtimalına qarşı)
VISION_MODELS = ["llama-3.2-11b-vision-preview", "llama-3.2-90b-vision-preview", "llama-3.3-70b-specdec"]
TEXT_MODEL = "llama-3.3-70b-versatility"

def encode_image(image):
    buffered = io.BytesIO()
    if image.mode != 'RGB': image = image.convert('RGB')
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. PANEL ---
with st.sidebar:
    st.title("⚙️ A-Zəka Ayarları")
    if st.button("🗑️ Tarixçəni Sil"):
        st.session_state.messages = []
        st.rerun()
    st.info("Yaradıcı: Abdullah Mikayılov")

st.markdown("<h1 class='main-title'>A-Zəka Ultra</h1>", unsafe_allow_html=True)

# --- 4. ÇAT MƏNTİQİ ---
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
        
        # MƏSULİYYƏTLİ MODEL SEÇİMİ
        success = False
        
        # Əgər şəkil varsa, vision modellərini tək-tək yoxla
        models_to_try = VISION_MODELS if img_b64 else [TEXT_MODEL]
        
        for model_name in models_to_try:
            try:
                if img_b64:
                    msgs = [
                        {"role": "system", "content": "Sən dahi A-Zəka-san. Şəkilləri görürsən."},
                        {"role": "user", "content": [
                            {"type": "text", "text": user_text},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                        ]}
                    ]
                else:
                    msgs = [{"role": "system", "content": "Sən A-Zəka-san."}] + st.session_state.messages

                completion = client.chat.completions.create(
                    model=model_name, messages=msgs, stream=True
                )
                
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_res += chunk.choices[0].delta.content
                        res_area.markdown(full_res + "▌")
                
                res_area.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
                success = True
                break # Uğurlu oldusa, digər modelləri yoxlama
            except Exception as e:
                continue # Xəta verdisə, növbəti modeli yoxla
        
        if not success:
            st.error("❌ Groq hazırda bütün vision modellərini bağlayıb. Lütfən bir neçə dəqiqə sonra yoxla və ya yalnız mətn yaz.")
