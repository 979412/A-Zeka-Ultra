import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# --- 1. ULTRA DİZAYNIN BƏRPASI ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="centered")

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

# --- 2. SOL PANEL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8682/8682970.png", width=80)
    st.title("⚙️ A-Zəka Paneli")
    st.write("Yaradıcı: **Abdullah Mikayılov**")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='ultra-title'>🔮 A-Zəka Ultra</h1>", unsafe_allow_html=True)

# --- 3. GROQ KONFİQURASİYASI (Sənin İşlək Keyin) ---
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# DİQQƏT: Silinmiş modelin əvəzinə ən yeni və güclü 'llama-3.3-70b-versatility' qoydum
MODEL_NAME = "llama-3.3-70b-versatility"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. GİRİŞ VƏ ANALİZ ---
prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Zəhmət olmasa bu məlumatı analiz et."
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        with st.spinner("A-Zəka düşünür..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": "Sən Abdullah tərəfindən yaradılmış dahi A-Zəka-san."},
                        {"role": "user", "content": user_text}
                    ]
                )
                res = response.choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "user", "content": user_text})
                st.session_state.messages.append({"role": "assistant", "content": res})
            except Exception as e:
                st.error(f"Xəta: {str(e)}")
