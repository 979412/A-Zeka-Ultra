import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

# --- 1. ULTRA DİZAYN ---
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
</style>
""", unsafe_allow_html=True)

# --- 2. GROQ AYARLARI (SENİN KEYİN) ---
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# BU MODEL ADINI DƏQİQ YAZDIM (404 xətası verməməsi üçün)
MODEL_NAME = "llama3-8b-8192" 

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. SÖHBƏT FUNKSİYASI ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Sualını yaz (Məsələn: Salam)...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            chat_completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "Sən Abdullah tərəfindən yaradılmış dahi A-Zəka-san."},
                    {"role": "user", "content": prompt}
                ]
            )
            ans = chat_completion.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"Xəta: {str(e)}")
