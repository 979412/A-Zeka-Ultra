import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# --- 1. ULTRA DİZAYN ---
st.set_page_config(page_title="A-Zəka 10x Ultra", page_icon="🔮", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #f4f7fb; font-family: 'Helvetica Neue', sans-serif; }
    .ultra-title {
        background: -webkit-linear-gradient(45deg, #1e3c72, #2a5298);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 900;
        font-size: 3.5rem;
        margin-bottom: 10px;
    }
    .stChatMessage { border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .stButton>button { background-color: #ff4b4b; color: white; border-radius: 10px; width: 100%; }
</style>
""", unsafe_allow_html=True)

# --- 2. SOL PANEL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8682/8682970.png", width=80)
    st.markdown("### ⚙️ A-Zəka Paneli")
    st.write("Yaradıcı: **Abdullah Mikayılov**")
    if st.button("🗑️ Tarixçəni Təmizlə"):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='ultra-title'>🔮 A-Zəka Ultra</h1>", unsafe_allow_html=True)

# --- 3. GROQ AYARLARI ---
# Sənin işlək Groq Key-in bura əlavə edildi
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# DİQQƏT: İşləməyən vision modelini ən stabil model ilə əvəz etdik
MODEL_NAME = "llama-3.3-70b-versatility"

if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_image(image):
    buffered = io.BytesIO()
    if image.mode != 'RGB': image = image.convert('RGB')
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Tarixçəni göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. GİRİŞ VƏ ANALİZ ---
prompt = st.chat_input("Sualını yaz və ya şəkil yüklə...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Zəhmət olmasa analiz et."
    with st.chat_message("user"):
        st.markdown(user_text)

    # Sistem təlimatı
    system_instruction = "Sən Abdullah Mikayılov tərəfindən yaradılmış dahi A-Zəka-san. Riyaziyyatı LaTeX ($...$) ilə həll et."
    content_list = [{"type": "text", "text": user_text}]

    # Şəkil varsa əlavə et
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=300)
            # Qeyd: Bu model yalnız mətni dəstəkləyirsə, aşağıdakı hissə xəta verə bilər.
            # Llama 3.3 əsasən mətndir, şəkil üçün Gemini kodu daha stabildir.

    with st.chat_message("assistant"):
        with st.spinner("A-Zəka 10x analiz edir..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_text}
                    ]
                )
                final_res = response.choices[0].message.content
                st.markdown(final_res)
                st.session_state.messages.append({"role": "user", "content": user_text})
                st.session_state.messages.append({"role": "assistant", "content": final_res})
            except Exception as e:
                st.error(f"Xəta: {str(e)}")
