import streamlit as st
from groq import Groq
import base64

# --- 1. SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="centered")

# --- 2. DİZAYN ---
st.markdown("""
<style>
.stChatMessage { border-radius: 15px; padding: 10px; border: 1px solid #f0f2f6; margin-bottom: 10px; }
.stChatInputContainer { padding-bottom: 20px; }
.main-title { color: #1E1E1E; text-align: center; font-weight: 800; }
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
    st.markdown("---")
    st.write("Yaradıcı: **Abdullah Mikayılov**")

# --- 5. ƏSAS EKRAN ---
st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra Alim</h1>", unsafe_allow_html=True)

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
    user_text = prompt.text if prompt.text else "Zəhmət olmasa bu müraciəti cavabla."
    
    # Yeni mesaj formatı (Daim siyahı formatında saxlayırıq ki, Vision xətası verməsin)
    new_user_content = [{"type": "text", "text": user_text}]
    
    is_image = False
    if prompt.files:
        for f in prompt.files:
            if f.type in ["image/png", "image/jpeg", "image/jpg"]:
                b64 = encode_image(f)
                new_user_content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:{f.type};base64,{b64}"}
                })
                is_image = True

    st.session_state.messages.append({"role": "user", "content": new_user_content})
    
    with st.chat_message("user"):
        st.markdown(user_text)
        if prompt.files:
            for f in prompt.files: st.image(f, width=300)

    # --- 7. ASSİSTANT CAVABI ---
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            # Əgər tarixçədə HARADASA şəkil varsa, Vision modelini istifadə etməyə davam etməliyik
            # Çünki mətn modelləri siyahı (list) formatındakı keçmiş mesajları oxuya bilmir.
            has_ever_sent_image = any(isinstance(m["content"], list) and len(m["content"]) > 1 for m in st.session_state.messages)
            
            if is_image or has_ever_sent_image:
                target_model = "meta-llama/llama-4-scout-17b-16e-instruct"
            else:
                target_model = "llama-3.3-70b-versatile"
            
            system_prompt = "Sən A-Zəka-san, Abdullah Mikayılov tərəfindən yaradılmısan. Ultra alimsən. Riyaziyyatı və bütün fənləri mükəmməl bilirsən. Addım-addım həll ver."
            
            completion = client.chat.completions.create(
                model=target_model,
                messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
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
            st.info("İpucu: Əgər xəta davam edərsə 'Tarixçəni Təmizlə' düyməsinə basaraq yenidən başlayın.")
