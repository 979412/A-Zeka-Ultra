import streamlit as st
from groq import Groq
import base64

# --- 1. SƏHİFƏ AYARLARI (Geniş və Rahat) ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="wide")

# --- 2. DİZAYN (Gecə Rejiminə Uyğun Modern Stil) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    .stChatMessage { border-radius: 20px; padding: 15px; border: 1px solid #1f2937; margin: 10px 0; }
    .stChatInput { border-radius: 10px !0px; }
</style>
""", unsafe_allow_html=True)

# --- 3. BEYİN MƏRKƏZİ (Sənin Yeni Açarın) ---
# Diqqət: Boşluq qalmaması üçün açarı tam bura yerləşdirdik
api_key = "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"
client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# --- 4. SOL PANEL ---
with st.sidebar:
    st.title("🧠 A-Zəka Pro")
    st.info("Müəllif: Abdullah Mikayılov")
    if st.button("🗑️ Tarixçəni Təmizlə", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 5. ƏSAS EKRAN ---
st.title("🚀 A-Zəka Ultra Alim (Vision Mode)")
st.write("Sualını soruş və ya şəkildəki misalı bura at!")

# Tarixçəni göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if isinstance(msg["content"], list):
            for part in msg["content"]:
                if part["type"] == "text": st.markdown(part["text"])
                elif part["type"] == "image_url": st.image(part["image_url"]["url"], width=400)
        else:
            st.markdown(msg["content"])

# --- 6. GİRİŞ VƏ FAYL ANALİZİ ---
prompt = st.chat_input("Dahi alimə sualını ver...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu şəkildəki misalları həll et."
    content_list = [{"type": "text", "text": user_text}]
    
    # Şəkil yüklənibsə onu bota "göstəririk"
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
            for f in prompt.files: st.image(f, width=400)

    # --- 7. ASSİSTANT CAVABI (Maksimum Sürət) ---
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            # Ən etibarlı vision modeli: llama-3.2-11b-vision-preview
            completion = client.chat.completions.create(
                model="llama-3.2-11b-vision-preview",
                messages=[{"role": "system", "content": "Sən A-Zəka-san. Şəkilləri mükəmməl analiz edirsən. Abdullah Mikayılov səni ən güclü alim beyni ilə təchiz edib."}] + st.session_state.messages,
                stream=True
            )
            
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Xəta kodu: {e}")
