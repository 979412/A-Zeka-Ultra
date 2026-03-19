import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. PREMİUM DİZAYN ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .main-title { 
        color: #1e40af; text-align: center; font-weight: 900; font-size: 3.5rem; margin-top: -60px;
    }
    .stChatMessage { border-radius: 15px; background: #f8fafc !important; border: 1px solid #e2e8f0; }
    /* Şəkil yükləmə düyməsinin stili */
    .stFileUploader { margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# --- 2. GÜCLÜ BEYİN BAĞLANTISI ---
API_KEY = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E"
genai.configure(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. PANEL ---
with st.sidebar:
    st.markdown("## 👑 A-Zəka Ultra")
    st.success("Yaradıcı: Abdullah Mikayılov")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra</h1>", unsafe_allow_html=True)

# Çat Tarixçəsi
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. ŞƏKİL VƏ MƏTN GİRİŞİ ---
# Abdullah, şəkili buradan seçirsən (+)
uploaded_file = st.file_uploader("Şəkil yüklə və ya çək (+)", type=['png', 'jpg', 'jpeg'])

prompt = st.chat_input("Sualını bura yaz, Abdullah...")

if prompt or uploaded_file:
    user_input = prompt if prompt else "Bu şəkli analiz et."
    
    # Şəkili hazırla
    img = None
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Yüklənən şəkil", width=300)

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        res_area = st.empty()
        full_res = ""
        
        # MÜTLƏQ CAVAB MEXANİZMİ
        try:
            # Şəkil varsa mütləq Flash modelini işlədirik (çünki Pro şəkil tanımır)
            model_name = 'gemini-1.5-flash'
            model = genai.GenerativeModel(model_name)
            
            # Giriş məlumatını hazırla
            content = [user_input, img] if img else [user_input]
            
            response = model.generate_content(content, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_res += chunk.text
                    res_area.markdown(full_res + "▌")
            
            res_area.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            
        except:
            # Əgər Flash işləməsə və şəkil yoxdursa, Pro modelini yoxla
            if not img:
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(user_input, stream=True)
                    for chunk in response:
                        if chunk.text:
                            full_res += chunk.text
                            res_area.markdown(full_res + "▌")
                    res_area.markdown(full_res)
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                except:
                    pass
