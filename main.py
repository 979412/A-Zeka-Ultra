import streamlit as st
from groq import Groq

# --- 1. SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="centered")

# --- 2. CSS (DÜYMƏ VƏ DİZAYN) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    
    /* Giriş sahəsinin dizaynı */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    
    /* Plus düyməsi üçün xüsusi stil (sidebar-da və ya input yanında) */
    .plus-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #262730;
        color: white;
        cursor: pointer;
        border: 1px solid #4a4d5a;
        font-size: 24px;
        margin-right: 10px;
    }
    
    .stChatMessage { border-radius: 20px; border: 1px solid #262730; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. GROQ BAĞLANTISI ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = "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"

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. ƏSAS EKRAN ---
st.title("🧠 A-Zəka Ultra Alim")
st.markdown("---")

# Mesajları göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. PLUS DÜYMƏSİ VƏ SUAL GİRİŞİ ---
# Streamlit-də inputun tam yanında düymə qoymaq üçün sütunlardan istifadə edirik
col1, col2 = st.columns([0.1, 0.9])

with col1:
    # Bu sənin istədiyin "+" düyməsidir
    uploaded_file = st.file_uploader("", type=["pdf", "txt", "png", "jpg"], label_visibility="collapsed")
    # Fayl yüklənəndə kiçik bir işarə göstərək
    if uploaded_file:
        st.toast("Fayl əlavə edildi!", icon="📎")

with col2:
    prompt = st.chat_input("Dahi alimə sualını ver...")

# --- 6. MƏNTİQ ---
if prompt:
    # İstifadəçi mesajını göstər
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Botun cavabı
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Sən A-Zəka-san, Abdullah Mikayılov tərəfindən yaradılan dahi alimsən."}] + st.session_state.messages,
                stream=True
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error("Xəta: Groq bağlantısını və VPN-i yoxlayın.")
