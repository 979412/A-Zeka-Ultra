import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- 1. DİZAYN VƏ BRENDİNG ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .main-title { color: #1a73e8; text-align: center; font-weight: 800; font-size: 3rem; border-bottom: 2px solid #1a73e8; padding-bottom: 10px; }
    .stChatMessage { border-radius: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("⚙️ A-Zəka Ayarları")
    st.write("Yaradıcı: **Abdullah Mikayılov**")
    # Google AI Studio-dan pulsuz API Key al: https://aistudio.google.com/app/apikey
    api_key = st.text_input("Gemini API Key daxil et:", type="password")
    if st.button("🗑️ Tarixçəni Sıfırla"):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra Alim</h1>", unsafe_allow_html=True)

# --- 2. BEYİN QOŞULMASI ---
if not api_key:
    st.info("👋 Salam Abdullah! Başlamaq üçün sol tərəfə Gemini API açarını daxil et. Bu sistem heç vaxt çökməyəcək.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash') # Bu model həm şəkil, həm mətn üçün mükəmməldir

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. SÖHBƏT VƏ ANALİZ ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Dahi səviyyəli sualını yaz və ya şəkil at...", accept_file=True)

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt.text if prompt.text else "Şəkil analizi xahiş olunur.")

    # Modelə göndəriləcək məlumat siyahısı
    inputs = [f"Sən Abdullah Mikayılov tərəfindən yaradılmış A-Zəka-san. Riyaziyyatı LaTeX ilə həll et. Sual: {prompt.text}"]
    
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=300)
            inputs.append(img)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(inputs)
            output_text = response.text
            st.markdown(output_text)
            
            # Yaddaşa yaz
            st.session_state.messages.append({"role": "user", "content": prompt.text if prompt.text else "Şəkil"})
            st.session_state.messages.append({"role": "assistant", "content": output_text})
        except Exception as e:
            st.error(f"Xəta baş verdi: {str(e)}")
