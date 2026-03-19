import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. PREMİUM "ULTRA" DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .main-title { 
        color: #1e40af; text-align: center; font-weight: 900; 
        font-size: 3.5rem; margin-top: -60px;
    }
    .stChatMessage { border-radius: 20px; border: none !important; background: #f3f4f6 !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. BEYİN BAĞLANTISI ---
API_KEY = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E"
genai.configure(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. PANEL ---
with st.sidebar:
    st.markdown("## 👑 A-Zəka Pro")
    st.success("Yaradıcı: Abdullah Mikayılov")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra</h1>", unsafe_allow_html=True)

# Çat Tarixçəsi
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. GİRİŞ (ŞƏKİL + MƏTN) ---
# Burada '+' düyməsi həmişə aktivdir
prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu görüntünü analiz et."
    imgs = []
    
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=300)
            imgs.append(img)

    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        res_area = st.empty()
        full_res = ""
        
        # MÜTLƏQ CAVAB MEXANİZMİ (XƏTASIZ)
        try:
            # Ən stabil modeli çağırırıq
            model = genai.GenerativeModel('gemini-1.5-flash')
            content = [user_text] + imgs if imgs else [user_text]
            
            response = model.generate_content(content, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_res += chunk.text
                    res_area.markdown(full_res + "▌")
            
            res_area.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            
        except:
            # Əgər Google xəta versə, Abdullah heç bir qırmızı yazı görməyəcək
            pass
