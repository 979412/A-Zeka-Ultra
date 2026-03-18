import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. SƏHİFƏ AYARLARI VƏ DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    .stApp { background-color: #ffffff; color: #1e293b; font-family: 'Inter', sans-serif; }
    
    /* Mesaj Balonları */
    .stChatMessage { 
        border-radius: 15px; 
        border: 1px solid #e2e8f0; 
        background-color: #f8fafc !important; 
        margin-bottom: 10px;
    }
    
    /* Başlıq */
    .main-header { 
        text-align: center; 
        color: #2563eb; 
        font-weight: 800; 
        font-size: 3rem; 
        margin-top: -50px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. BEYİN SİSTEMİ (GEMINI 1.5 FLASH) ---
# Sənin yeni və işlək API açarın bura yerləşdirildi
GEMINI_API_KEY = "AIzaSyBiPhToQs_WMs_qtY_seJxhCEVd2r1Y7yk"
genai.configure(api_key=GEMINI_API_KEY)

# Ən stabil və sürətli model
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. YAN PANEL ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>⚙️ A-Zəka Ayarları</h2>", unsafe_allow_html=True)
    st.info("Yaradıcı: Abdullah Mikayılov")
    st.divider()
    if st.button("🗑️ Tarixçəni Sil", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-header'>A-Zəka Ultra</h1>", unsafe_allow_html=True)

# --- 4. ÇAT TARİXÇƏSİ ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. GİRİŞ SİSTEMİ (+) ---
prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Zəhmət olmasa bu şəkli analiz et."
    uploaded_images = []
    
    # Şəkil yüklənibsə onu emal et
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=400, caption="Yüklənən media")
            uploaded_images.append(img)

    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    # A-Zəka-nın cavabı
    with st.chat_message("assistant"):
        res_area = st.empty()
        full_response = ""
        
        try:
            # Şəkil və mətni eyni anda Gemini-yə göndəririk
            input_data = [user_text] + uploaded_images if uploaded_images else [user_text]
            
            # Stream rejimində cavab alırıq (saniyəlik cavab üçün)
            response = model.generate_content(input_data, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    res_area.markdown(full_response + "▌")
            
            res_area.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"❌ Xəta: {str(e)}")
            st.info("İpucu: Səhifəni yeniləyin və ya API Key-in aktivliyini yoxlayın.")
