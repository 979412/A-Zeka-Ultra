import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. PROFESSIONAL VİSUAL AYARLAR ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .stChatMessage { border-radius: 15px; border: 1px solid #e2e8f0; background-color: #f8fafc !important; margin-bottom: 10px; }
    .main-title { color: #2563eb; text-align: center; font-weight: 800; font-size: 3rem; margin-top: -50px; }
    [data-testid="stSidebar"] { background-color: #f1f5f9 !important; border-right: 1px solid #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# --- 2. BEYİN SİSTEMİ (STABİL KANAL) ---
# Sənin ən son verdiyin yeni açar
API_KEY = "AIzaSyBiPhToQs_WMs_qtY_seJxhCEVd2r1Y7yk"

try:
    genai.configure(api_key=API_KEY)
    # 404 xətasını keçmək üçün ən çox dəstəklənən stabil model adı
    model = genai.GenerativeModel('gemini-1.5-flash-8b') 
except Exception as e:
    st.error(f"Başlanğıc xətası: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. YAN PANEL ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>⚙️ Panel</h2>", unsafe_allow_html=True)
    st.info("Yaradıcı: Abdullah Mikayılov\nStatus: Ultra Aktiv")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-header'>🧠 A-Zəka Ultra</h1>", unsafe_allow_html=True)

# --- 4. ÇAT TARİXÇƏSİ ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. GİRİŞ VƏ ANALİZ ---
prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu şəkli analiz et."
    imgs = []
    
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=400)
            imgs.append(img)

    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        res_placeholder = st.empty()
        full_res = ""
        
        try:
            # Şəkil varsa şəkilli, yoxdursa yalnız mətnli sorğu
            request_content = [user_text] + imgs if imgs else [user_text]
            
            # Stream rejimində cavab
            response = model.generate_content(request_content, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_res += chunk.text
                    res_placeholder.markdown(full_res + "▌")
            
            res_placeholder.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            
        except Exception as e:
            # 404 xətası verərsə alternativ modelə keçid
            if "404" in str(e):
                st.warning("🔄 Model yenilənir, zəhmət olmasa təkrar cəhd edin...")
                # Alternativ model cəhdi
                model = genai.GenerativeModel('gemini-1.5-pro')
            else:
                st.error(f"Xəta: {str(e)}")
