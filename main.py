import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .stChatMessage { border-radius: 15px; border: 1px solid #e2e8f0; background-color: #f8fafc !important; }
    .main-header { text-align: center; color: #2563eb; font-weight: 800; font-size: 3rem; margin-top: -50px; }
</style>
""", unsafe_allow_html=True)

# --- 2. BEYİN SİSTEMİ (YENİLƏNMİŞ MODEL) ---
# Sənin işlək API açarın
GEMINI_API_KEY = "AIzaSyDz-rB4RGABHiz1S9bQ4OutCY61v39b8Eo"
genai.configure(api_key=GEMINI_API_KEY)

# 404 xətası verməyən ən son model
MODEL_NAME = 'gemini-1.5-flash-latest' 

try:
    model = genai.GenerativeModel(MODEL_NAME)
except:
    model = genai.GenerativeModel('gemini-pro')

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. PANEL ---
with st.sidebar:
    st.title("⚙️ A-Zəka")
    if st.button("🗑️ Tarixçəni Sil"):
        st.session_state.messages = []
        st.rerun()
    st.info("Yaradıcı: Abdullah Mikayılov")

st.markdown("<h1 class='main-header'>A-Zəka Ultra</h1>", unsafe_allow_html=True)

# --- 4. ÇAT ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Zəhmət olmasa bunu analiz et."
    uploaded_images = []
    
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=400)
            uploaded_images.append(img)

    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        res_area = st.empty()
        full_response = ""
        
        try:
            # Şəkil və mətni eyni anda göndəririk
            input_data = [user_text] + uploaded_images if uploaded_images else [user_text]
            
            response = model.generate_content(input_data, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    res_area.markdown(full_response + "▌")
            
            res_area.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            # Əgər hələ də model xətası verərsə, bu hissə kömək edəcək
            st.error(f"Xəta: {str(e)}")
            st.info("İpucu: Google AI Studio-da modelin aktiv olduğundan əmin olun.")
