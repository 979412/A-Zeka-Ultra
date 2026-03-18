import streamlit as st
from groq import Groq

# --- 1. SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="centered")

# --- 2. DİZAYN AYARLARI ---
st.markdown("""
    <style>
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

# --- 4. SOL PANEL (Yalnız Tarixçəni Təmizləmək Üçün) ---
with st.sidebar:
    st.title("⚙️ A-Zəka Ayarları")
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

# --- 6. SUAL VƏ FAYL GİRİŞİ (YENİ SİSTEM) ---
# Düyməni birbaşa qutunun içinə əlavə edirik: accept_file=True
prompt = st.chat_input("Dahi alimə sualını ver...", accept_file=True)

# --- 7. MƏNTİQ ---
if prompt:
    # İstifadəçinin yazdığı mətni alırıq (boşdursa, boş sətir qalır)
    user_text = prompt.text if prompt.text else ""
    display_content = user_text
    
    # Əgər qutunun içindəki o düymə vasitəsilə fayl yüklənibsə:
    if prompt.files:
        for uploaded_file in prompt.files:
            # Faylın adını da mesaja qoşuruq
            display_content = f"📎 **Əlavə edilən fayl:** {uploaded_file.name}\n\n" + display_content

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
                messages=[{"role": "system", "content": "Sən A-Zəka-san, dahi proqramçı Abdullah Mikayılov tərəfindən yaradılmısan."}] + st.session_state.messages,
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
