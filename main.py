import streamlit as st
from groq import Groq
import requests
from streamlit_lottie import st_lottie

# --- 1. SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="centered")

# --- 2. PREMIUM CSS DİZAYNI ---
st.markdown("""
    <style>
    /* Ümumi Arxa Fon */
    .stApp {
        background: radial-gradient(circle, #1b2735 0%, #090a0f 100%);
    }
    
    /* Neon Başlıq Effekti */
    .neon-text {
        color: #fff;
        text-shadow: 0 0 10px #00d4ff, 0 0 20px #00d4ff, 0 0 40px #00d4ff;
        font-family: 'Orbitron', sans-serif;
        text-align: center;
    }

    /* Mesaj Balonlarını Gözəlləşdir */
    .stChatMessage {
        border-radius: 20px;
        margin-bottom: 15px;
        border: 1px solid rgba(0, 212, 255, 0.2);
        backdrop-filter: blur(5px);
    }
    
    /* Sol Panel Səliqəsi */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 15, 25, 0.9);
        border-right: 1px solid #00d4ff;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-thumb { background: #00d4ff; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ANIMASİYA YÜKLƏMƏ (Lottie) ---
def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

lottie_ai = load_lottie("https://assets10.lottiefiles.com/packages/lf20_5njp3v8p.json")

# --- 4. BEYİN MƏRKƏZİ (Groq) ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = "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"

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 5. SOL PANEL ---
with st.sidebar:
    if lottie_ai:
        st_lottie(lottie_ai, height=150)
    st.markdown("<h2 style='text-align: center; color: #00d4ff;'>A-Zəka Control</h2>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.write("---")
    st.write("🚀 Versiya: **2.0 Ultra**")
    st.write("👤 Yaradıcı: **Abdullah Mikayılov**")

# --- 6. ƏSAS EKRAN ---
st.markdown("<h1 class='neon-text'>🧠 A-Zəka Ultra Alim</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa;'>Abdullah Mikayılov tərəfindən yaradılan dünyanın ən zəkalı köməkçisi</p>", unsafe_allow_html=True)
st.markdown("---")

# Mesajları göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 7. GİRİŞ SAHƏSİ (Gemini Style) ---
prompt = st.chat_input("Dahi alimə sualını ver...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else ""
    display_content = user_text
    
    if prompt.files:
        for f in prompt.files:
            display_content = f"📎 **Fayl:** {f.name}\n\n" + display_content

    st.session_state.messages.append({"role": "user", "content": display_content})
    with st.chat_message("user"):
        st.markdown(display_content)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Sən A-Zəka-san, dahi Abdullah Mikayılovun sənət əsərisən."}] + st.session_state.messages,
                stream=True
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except:
            st.error("Bağlantı xətası!")
