import streamlit as st
from groq import Groq

# --- 1. SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="centered")

# --- 2. CSS: BÖYÜK QUTUNU GİZLƏDİB, BALACA "+" DÜYMƏSİ ETMƏK ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    
    /* 1. Böyük File Uploader sahəsini gizlət */
    .stFileUploader section {
        display: none !important;
    }
    
    /* 2. Özəl bir "+" düyməsi yaradın */
    .custom-plus-button {
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
        position: relative;
        top: 20px; /* Input qutusuna uyğunlaşdırmaq üçün */
    }
    
    .custom-plus-button:hover {
        background-color: #3e404b;
    }
    
    /* Mesaj qutularını gözəlləşdir */
    .stChatMessage { border-radius: 20px; border: 1px solid #262730; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BEYİN MƏRKƏZİ (Groq) ---
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

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 5. İSTƏDİYİN DÜYMƏ VƏ GİRİŞ SAHƏSİ ---
# Düyməni və input qutusunu yan-yana gətirmək üçün sütunlardan istifadə edirik
col1, col2 = st.columns([0.1, 0.9])

with col1:
    # Bu, o böyük qutunun yerinə çıxan balaca dairəvi '+' düyməsidir
    # İstifadəçi buna basanda fayl seçmə pəncərəsi açılacaq
    uploaded_file = st.file_uploader("+", type=["png", "jpg", "jpeg", "pdf"], label_visibility="collapsed")
    
with col2:
    prompt = st.chat_input("Dahi alimə sualını ver...")

# --- 6. PROSES VƏ MƏNTİQ ---
if prompt:
    display_content = prompt
    
    # Əgər fayl yüklənibsə, mesajın başına əlavə edirik
    if uploaded_file:
        # Şəkil yüklənibsə, şəkli göstərək
        if uploaded_file.type.startswith('image/'):
            st.image(uploaded_file, caption=f"Yüklənən şəkil: {uploaded_file.name}", width=200)
            display_content = f"📎 **Şəkil:** {uploaded_file.name}\n\n" + prompt
        else:
            display_content = f"📎 **Fayl:** {uploaded_file.name}\n\n" + prompt

    # İstifadəçi mesajını yaddaşa yaz
    st.session_state.messages.append({"role": "user", "content": display_content})
    with st.chat_message("user"):
        st.markdown(display_content)

    # Botun cavabı
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Sən A-Zəka-san, Abdullah Mikayılov tərəfindən yaradılmısan."}] + st.session_state.messages,
                stream=True
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Xəta: Groq bağlantısı kəsildi! VPN-i qoşmağı unutma.")
