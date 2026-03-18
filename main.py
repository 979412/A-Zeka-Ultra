import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- PREMİUM DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    .main-title { color: #1a73e8; text-align: center; font-weight: 800; font-size: 3rem; }
    .stChatMessage { border-radius: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

# --- SOL PANEL ---
with st.sidebar:
    st.title("⚙️ Ayarlar")
    # BURADA ARTIQ GROQ YOX, GEMINI AÇARINI YAZACAQSAN
    user_api_key = st.text_input("Gemini API Key daxil et:", type="password")
    if st.button("🗑️ Tarixçəni Təmizlə"):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra</h1>", unsafe_allow_html=True)

# --- BEYİNİ AKTİVLƏŞDİRMƏ ---
if user_api_key:
    genai.configure(api_key=user_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.warning("Davam etmək üçün sol tərəfə API Key daxil et!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- GİRİŞ SAHƏSİ (+) ---
prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu şəkli analiz et."
    with st.chat_message("user"):
        st.markdown(user_text)
    
    content = [user_text]
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=300)
            content.append(img)

    with st.chat_message("assistant"):
        with st.spinner("A-Zəka düşünür..."):
            try:
                response = model.generate_content(content)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "user", "content": user_text})
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Xəta: {str(e)}")
