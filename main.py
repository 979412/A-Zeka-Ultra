import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. ULTRA MODERN VİSUAL ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background: white; }
    .main-title { 
        color: #1e40af; text-align: center; font-weight: 900; 
        font-size: 3.5rem; margin-top: -60px;
    }
    .stChatMessage { border-radius: 15px; background: #f8fafc !important; border: 1px solid #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# --- 2. AVTOMATİK BEYİN TAPICI (SƏHV VERMƏYƏN SİSTEM) ---
API_KEY = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E"
genai.configure(api_key=API_KEY)

@st.cache_resource
def get_working_brain():
    try:
        # Sənin açarın üçün aktiv olan bütün modelləri tapır
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Ən güclü olanı (Flash və ya Pro) seçir
        for target in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
            if target in models:
                return genai.GenerativeModel(target)
        return genai.GenerativeModel(models[0]) if models else None
    except:
        return None

brain = get_working_brain()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. PANEL ---
with st.sidebar:
    st.title("👑 A-Zəka Ultra")
    st.success("Yaradıcı: Abdullah Mikayılov")
    if brain:
        st.info(f"Beyin Aktiv: {brain.model_name.split('/')[-1]}")
    if st.button("🗑️ Tarixçəni Sil", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra</h1>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. ŞƏKİL VƏ SUAL ANALİZİ (1 SANİYƏDƏ) ---
prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu şəkli ən xırda detalına qədər analiz et."
    imgs = []
    
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=400, caption="Yüklənən Şəkil")
            imgs.append(img)

    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        res_area = st.empty()
        full_res = ""
        
        if not brain:
            st.error("Sistem qoşulmadı. İnterneti və ya API açarını yoxla.")
        else:
            try:
                # Mətn və şəkilləri eyni anda analiz edir
                content = [user_text] + imgs if imgs else [user_text]
                response = brain.generate_content(content, stream=True)
                
                for chunk in response:
                    if chunk.text:
                        full_res += chunk.text
                        res_area.markdown(full_res + "▌")
                
                res_area.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
            except Exception as e:
                st.error(f"Xəta: {str(e)}")
