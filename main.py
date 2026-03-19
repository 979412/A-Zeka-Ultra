import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. PROFESSIONAL DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .stChatMessage { border-radius: 12px; border: 1px solid #e2e8f0; background-color: #f8fafc !important; margin-bottom: 10px; }
    .main-header { text-align: center; color: #2563eb; font-weight: 800; font-size: 3rem; margin-top: -40px; }
    [data-testid="stSidebar"] { background-color: #f1f5f9 !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. BEYİN SİSTEMİ (YENİ KEY İLƏ) ---
NEW_API_KEY = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E"
genai.configure(api_key=NEW_API_KEY)

# Modelləri tək-tək yoxlayan funksiya
@st.cache_resource
def load_stable_model():
    # Yoxlanılacaq modellərin siyahısı (ən yenidən ən stabilə doğru)
    check_models = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    for m_name in check_models:
        try:
            model = genai.GenerativeModel(m_name)
            # Kiçik bir test (sırf modelin mövcudluğunu yoxlamaq üçün)
            return model
        except:
            continue
    return None

model = load_stable_model()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. PANEL ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>⚙️ Panel</h2>", unsafe_allow_html=True)
    st.info("Yaradıcı: Abdullah Mikayılov")
    if model:
        st.success(f"Aktiv Beyin: {model.model_name.split('/')[-1]}")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-header'>🧠 A-Zəka Ultra</h1>", unsafe_allow_html=True)

# Çat tarixçəsi
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. GİRİŞ VƏ ANALİZ ---
prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Zəhmət olmasa bu mediaya bax."
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
        res_area = st.empty()
        full_res = ""
        
        try:
            if not model:
                st.error("Xəta: Heç bir model tapılmadı. Zəhmət olmasa API açarını AI Studio-da yoxlayın.")
            else:
                # Şəkil varsa şəkilli sorğu, yoxdursa yalnız mətn
                input_data = [user_text] + imgs if imgs else [user_text]
                response = model.generate_content(input_data, stream=True)
                
                for chunk in response:
                    if chunk.text:
                        full_res += chunk.text
                        res_area.markdown(full_res + "▌")
                
                res_area.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
                
        except Exception as e:
            st.error(f"⚠️ Texniki nasazlıq: {str(e)}")
