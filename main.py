import streamlit as st
from groq import Groq
import base64

# --- 1. SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="centered")

# --- 2. GÖZƏL DİZAYN (CSS) ---
st.markdown("""
<style>
    /* Ümumi fon və yazı rəngi */
    .stApp { background-color: #ffffff; }
    
    /* Mesaj qutularının dizaynı */
    .stChatMessage {
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        border: 1px solid #f0f2f6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* İstifadəçi mesajı */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #f8f9fa;
    }
    
    /* Başlıq dizaynı */
    .main-title {
        color: #1E1E1E;
        text-align: center;
        font-weight: 800;
        letter-spacing: -1px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. BEYİN MƏRKƏZİ ---
api_key = "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"
client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# --- 4. SOL PANEL ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>⚙️ Ayarlar</h2>", unsafe_allow_html=True)
    st.write("Yaradıcı: **Abdullah Mikayılov**")
    st.markdown("---")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 5. ƏSAS EKRAN ---
st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra Alim</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Dahi süni intellekt köməkçiniz</p>", unsafe_allow_html=True)
st.markdown("---")

# Tarixçəni göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if isinstance(msg["content"], list):
            for part in msg["content"]:
                if part["type"] == "text": st.markdown(part["text"])
                elif part["type"] == "image_url": st.image(part["image_url"]["url"], width=300)
        else:
            st.markdown(msg["content"])

# --- 6. GİRİŞ (Fayl və Mətn) ---
prompt = st.chat_input("Sualını bura yaz və ya şəkil at...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu şəkildəki misalları həll et."
    content_list = [{"type": "text", "text": user_text}]
    
    if prompt.files:
        for f in prompt.files:
            if f.type in ["image/png", "image/jpeg", "image/jpg"]:
                b64 = encode_image(f)
                content_list.append({"type": "image_url", "image_url": {"url": f"data:{f.type};base64,{b64}"}})

    st.session_state.messages.append({"role": "user", "content": content_list})
    
    with st.chat_message("user"):
        st.markdown(user_text)
        if prompt.files:
            for f in prompt.files: st.image(f, width=300)

    # --- 7. AI CAVABI ---
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            # Ən stabil vision modeli
            completion = client.chat.completions.create(
                model="llama-3.2-11b-vision-preview",
                messages=[{"role": "system", "content": "Sən A-Zəka-san, dahi Abdullah Mikayılov tərəfindən yaradılmısan."}] + st.session_state.messages,
                stream=True
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Xəta: {e}")
