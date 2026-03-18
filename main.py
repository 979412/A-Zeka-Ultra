import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# --- ULTRA DİZAYN ---
st.set_page_config(page_title="A-Zəka 10x Ultra", page_icon="🔮", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #f4f7fb; }
    .ultra-title {
        background: -webkit-linear-gradient(45deg, #1e3c72, #2a5298);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 900;
        font-size: 3.5rem;
    }
    .stChatMessage { border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8682/8682970.png", width=80)
    st.title("⚙️ A-Zəka Paneli")
    st.write("Yaradıcı: **Abdullah Mikayılov**")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='ultra-title'>🔮 A-Zəka Ultra</h1>", unsafe_allow_html=True)

# --- GROQ AYARLARI ---
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)
# DİQQƏT: Groq-da vision xətası çıxsa, bu modeli 'llama-3.3-70b-versatility' ilə dəyişə bilərsən
MODEL = "llama-3.2-11b-vision-preview"

if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_image(image):
    buffered = io.BytesIO()
    if image.mode != 'RGB': image = image.convert('RGB')
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu şəkli analiz et."
    with st.chat_message("user"):
        st.markdown(user_text)
    
    content_list = [{"type": "text", "text": user_text}]

    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=300)
            b64_img = encode_image(img)
            content_list.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}
            })

    with st.chat_message("assistant"):
        with st.spinner("A-Zəka 10x düşünür..."):
            try:
                chat_completion = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": "Sən Abdullah tərəfindən yaradılmış dahi A-Zəka-san."},
                        {"role": "user", "content": content_list}
                    ]
                )
                res = chat_completion.choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "user", "content": user_text})
                st.session_state.messages.append({"role": "assistant", "content": res})
            except Exception as e:
                st.error(f"Xəta: {str(e)}")
