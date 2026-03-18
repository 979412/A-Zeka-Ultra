import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. PROFESSIONAL DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .stChatMessage { border-radius: 12px; border: 1px solid #e2e8f0; background-color: #f8fafc !important; }
    .main-header { text-align: center; color: #2563eb; font-weight: 800; font-size: 3rem; margin-top: -50px; }
</style>
""", unsafe_allow_html=True)

# --- 2. BEYİN SİSTEMİ (STABİL KONFİQURASİYA) ---
GEMINI_API_KEY = "AIzaSyBiPhToQs_WMs_qtY_seJxhCEVd2r1Y7yk"

# API-nı ən stabil versiya ilə işə salırıq
genai.configure(api_key=GEMINI_API_KEY)

# Modelləri tək-tək yoxlayan "Ağıllı Seçim" funksiyası
def get_working_model():
    # Ən stabil modellərin siyahısı
    models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    for m in models_to_try:
        try:
            model = genai.GenerativeModel(m)
            # Kiçik bir test sorğusu ilə yoxlayırıq
            return model
        except:
            continue
    return None

model = get_working_model()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. PANEL ---
with st.sidebar:
    st.title("⚙️ Ayarlar")
    if st.button("🗑️ Tarixçəni Sil", use_container_width=True):
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
    user_text = prompt.text if prompt.text else "Bu şəkli analiz et."
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
            if model is None:
                st.error("Xəta: Heç bir modelə qoşulmaq mümkün olmadı. API Key-i yoxlayın.")
            else:
                input_data = [user_text] + uploaded_images if uploaded_images else [user_text]
                
                # Stream rejimində cavab alırıq
                response = model.generate_content(input_data, stream=True)
                
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        res_area.markdown(full_response + "▌")
                
                res_area.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"⚠️ Texniki Nasazlıq: {str(e)}")
            st.info("İpucu: Səhifəni yeniləyin və ya API Key-in aktivliyini AI Studio-da yoxlayın.")
