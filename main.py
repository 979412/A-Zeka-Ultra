import streamlit as st
from groq import Groq

# --- 1. SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="centered")

# --- 2. CSS VƏ DİZAYN AYARLARI ---
st.markdown("""
    <style>
    /* Mesaj qutularını dairəvi və seliqəli edirik */
    .stChatMessage { border-radius: 15px; padding: 10px; border: 1px solid #333; }
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

# --- 4. SOL PANEL (FAYL YÜKLƏMƏ BURADA OLACAQ) ---
with st.sidebar:
    st.title("⚙️ A-Zəka Ayarları")
    st.markdown("---")
    
    # Şəkil/Fayl yükləmə qutusunu bura qoyuruq ki, ana ekranı korlamasın
    st.subheader("📎 Fayl və ya Şəkil Yüklə")
    uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg", "pdf"], label_visibility="collapsed")
    
    st.markdown("---")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.write("Yaradıcı: **Abdullah Mikayılov**")

# --- 5. ƏSAS EKRAN ---
st.title("🧠 A-Zəka Ultra Alim")
st.markdown("---")

# Mesajları göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 6. SUAL GİRİŞİ (ARTIQ ÖZ YERİNDƏ, ƏN AŞAĞIDA OLACAQ) ---
prompt = st.chat_input("Dahi alimə sualını ver...")

# --- 7. MƏNTİQ ---
if prompt:
    display_content = prompt
    
    # Əgər sol tərəfdən fayl yüklənibsə, mesaja faylın adını əlavə et
    if uploaded_file:
        display_content = f"📎 **Əlavə edilən fayl:** {uploaded_file.name}\n\n" + prompt

    # İstifadəçi mesajını ekrana yaz
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
            st.error("Xəta baş verdi! VPN-in işlədiyinə əmin ol.")
