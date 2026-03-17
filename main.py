import streamlit as st
from groq import Groq
import base64

# --- 1. SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="A-Zəka Ultra Vision", page_icon="🧠", layout="centered")

# --- 2. DİZAYN ---
st.markdown("""
<style>
.stChatMessage { border-radius: 15px; padding: 10px; border: 1px solid #333; margin-bottom: 10px; }
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
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.write("Yaradıcı: **Abdullah Mikayılov**")

# --- 5. ƏSAS EKRAN ---
st.title("🧠 A-Zəka Ultra Vision")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if isinstance(msg["content"], list):
            for part in msg["content"]:
                if part["type"] == "text":
                    st.markdown(part["text"])
                elif part["type"] == "image_url":
                    st.image(part["image_url"]["url"], width=300)
        else:
            st.markdown(msg["content"])

# --- 6. GİRİŞ ---
prompt = st.chat_input("Sualını yaz və ya şəkil at...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu şəkli analiz et."
    content_list = [{"type": "text", "text": user_text}]
    
    if prompt.files:
        for f in prompt.files:
            if f.type in ["image/png", "image/jpeg", "image/jpg"]:
                b64 = encode_image(f)
                content_list.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:{f.type};base64,{b64}"}
                })

    st.session_state.messages.append({"role": "user", "content": content_list})
    
    with st.chat_message("user"):
        st.markdown(user_text)
        if prompt.files:
            for f in prompt.files:
                st.image(f, width=300)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            # DÜZƏLİŞ: Groq-un hal-hazırda aktiv olan ən stabil modeli
            # Əgər bu da xəta versə, model adını "llama-3.2-11b-vision-preview" ilə əvəz et
            target_model = "llama-3.2-11b-vision-preview" 
            
            completion = client.chat.completions.create(
                model=target_model,
                messages=[{"role": "system", "content": "Sən A-Zəka-san, Abdullah Mikayılov tərəfindən yaradılmısan. Sən bir dahisən."}] + st.session_state.messages,
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
