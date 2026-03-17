import streamlit as st
from groq import Groq
import base64

# --- 1. SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="centered")

# --- 2. DİZAYN ---
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .stChatMessage { border-radius: 15px; padding: 15px; margin-bottom: 10px; border: 1px solid #f0f2f6; }
    .main-title { color: #1E1E1E; text-align: center; font-weight: 800; margin-top: -50px; }
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
    st.title("⚙️ Ayarlar")
    st.write("Yaradıcı: **Abdullah Mikayılov**")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 5. ƏSAS EKRAN ---
st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra Alim</h1>", unsafe_allow_html=True)

# Mesajları göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if isinstance(msg["content"], list):
            for part in msg["content"]:
                if part["type"] == "text": st.markdown(part["text"])
                elif part["type"] == "image_url": st.image(part["image_url"]["url"], width=300)
        else:
            st.markdown(msg["content"])

# --- 6. GİRİŞ ---
prompt = st.chat_input("Sualını yaz və ya şəkil at...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Zəhmət olmasa cavabla."
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

    # --- 7. AI CAVABI (Ağıllı Model Seçimi) ---
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # Groq-da hal-hazırda aktiv olan modellərin siyahısı
        # Əgər biri 404 versə, o birini yoxlayacaq
        models_to_try = [
            "llama-3.2-11b-vision-preview",
            "llama-3.2-90b-vision-preview",
            "llama-3.2-11b-text-preview" # Əgər şəkil modelləri işləməsə, heç olmasa mətn işləsin
        ]
        
        success = False
        for model in models_to_try:
            if success: break
            try:
                completion = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "system", "content": "Sən A-Zəka-san, Abdullah Mikayılov tərəfindən yaradılmısan."}] + st.session_state.messages,
                    stream=True
                )
                
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        placeholder.markdown(full_response + "▌")
                
                placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                success = True
            except Exception as e:
                if model == models_to_try[-1]: # Əgər sonuncu model də xəta versə
                    st.error(f"Sistem xətası: {e}")
                continue
