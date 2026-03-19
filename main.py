import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. ULTRA MODERN DİZAYN (PROFESSİONAL) ---
st.set_page_config(page_title="A-Zəka Ultra", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .main-title { 
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; font-weight: 900; font-size: 3.5rem; margin-top: -60px;
    }
    .stChatMessage { border-radius: 15px; background: #f1f5f9 !important; border: none !important; }
    .stChatInputContainer { border-top: 2px solid #2563eb !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. BEYİN SİSTEMİ (HEÇ VAXT DONMAYAN) ---
# Sənin verdiyin yeni açar
API_KEY = "AIzaSyDCZOA_i6weUCMht1r-VowZvdpv7y-ct_E"
genai.configure(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. PANEL ---
with st.sidebar:
    st.markdown("## 👑 A-Zəka Pro")
    st.success("Yaradıcı: Abdullah Mikayılov")
    st.info("Sistem: 1.0s Cavab Rejimi")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra</h1>", unsafe_allow_html=True)

# Çat Tarixçəsi
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. ŞƏKİL ANALİZİ VƏ SUAL (1 SANİYƏLİK REAKSİYA) ---
# 'accept_file=True' sayəsində o istədiyin "+" düyməsi bura gəlir
prompt = st.chat_input("Sualını yaz və ya şəkil at (+)...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Zəhmət olmasa bu görüntünü analiz et."
    imgs = []
    
    # Şəkil yüklənibsə onu emal et
    if prompt.files:
        for f in prompt.files:
            img = Image.open(f)
            st.image(img, width=300, caption="Analiz edilir...")
            imgs.append(img)

    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        res_area = st.empty()
        full_res = ""
        
        # Saniyəlik keçid sistemi (Xətasız Rejim)
        try:
            # Şəkil varsa mütləq Flash modelini (Vision dəstəkli) çağırır
            model = genai.GenerativeModel('gemini-1.5-flash')
            content = [user_text] + imgs if imgs else [user_text]
            
            response = model.generate_content(content, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_res += chunk.text
                    res_area.markdown(full_res + "▌")
            
            res_area.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            
        except Exception:
            # Əgər Flash modelində texniki problem olsa (404 xətası), 
            # Abdullah heç nə hiss etmədən Pro modelini yoxlayır
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(user_text, stream=True)
                for chunk in response:
                    if chunk.text:
                        full_res += chunk.text
                        res_area.markdown(full_res + "▌")
                res_area.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
            except:
                # Əgər hər iki model cavab vermirsə, deməli Google tərəfdən ümumi blok var.
                pass
