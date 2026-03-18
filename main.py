import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- 1. A-ZƏKA AYARLARI ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="wide")

# Yaradıcıya xüsusi təlimat
SYSTEM_INSTRUCTION = (
    "Sən A-Zəka-san, dahi Abdullah Mikayılov tərəfindən yaradılmış Ultra Alim AI-san. "
    "Riyaziyyat suallarını addım-addım və LaTeX ($...$) ilə həll et."
)

# --- 2. BEYİN QOŞULMASI ---
# Bura mütləq AI Studio-dan aldığın açarı qoy!
API_KEY = "AIzaSyDz-rB4RGABHiz1S9bQ4OutCY61v39b8Eo" 
genai.configure(api_key=API_KEY)

# Modeli başladırıq
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_INSTRUCTION
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. PEŞƏKAR DİZAYN ---
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    .stChatMessage { border-radius: 12px; border: 1px solid #e0e0e0; }
    .main-title { color: #1a73e8; text-align: center; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra Alim</h1>", unsafe_allow_html=True)
st.write(f"<p style='text-align: center;'>Yaradıcı: <b>Abdullah Mikayılov</b></p>", unsafe_allow_html=True)

# --- 4. TARİXÇƏ ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. GİRİŞ VƏ ANALİZ ---
prompt = st.chat_input("Dahi sualını bura yaz və ya şəkil at...", accept_file=True)

if prompt:
    user_content = []
    
    # Mətni əlavə et
    text_query = prompt.text if prompt.text else "Zəhmət olmasa bu vizualı analiz et."
    user_content.append(text_query)
    
    # Şəkli əlavə et
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            user_content.append(img)
            st.image(img, width=400)

    # İstifadəçi mesajını göstər
    with st.chat_message("user"):
        st.markdown(text_query)

    # Cavab al
    with st.chat_message("assistant"):
        with st.spinner("A-Zəka düşünür..."):
            try:
                response = model.generate_content(user_content)
                st.markdown(response.text)
                
                # Tarixçəni yadda saxla
                st.session_state.messages.append({"role": "user", "content": text_query})
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Xəta: {e}. Zəhmət olmasa API açarını və İnternetini yoxla.")
