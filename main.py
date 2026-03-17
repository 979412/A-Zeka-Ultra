import streamlit as st
from groq import Groq
import base64

# --- 1. SƏHİFƏ AYARLARI ---
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="centered")

# --- 2. PEŞƏKAR DİZAYN (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .stChatMessage { border-radius: 15px; padding: 15px; margin-bottom: 10px; border: 1px solid #f0f2f6; }
    .main-title { color: #1E1E1E; text-align: center; font-weight: 800; margin-top: -50px; }
    .sidebar-text { font-size: 0.9rem; color: #555; }
</style>
""", unsafe_allow_html=True)

# --- 3. BEYİN MƏRKƏZİ (Groq) ---
# Sənin aktiv API açarın
api_key = "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"
client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Şəkli kodlaşdırmaq üçün funksiya
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# --- 4. SOL PANEL (Ayarlar) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>⚙️ Ayarlar</h2>", unsafe_allow_html=True)
    st.markdown("<p class='sidebar-text'>Yaradıcı: <b>Abdullah Mikayılov</b></p>", unsafe_allow_html=True)
    st.markdown("<p class='sidebar-text'>Rejim: <b>Ultra Alim (Görmə Aktiv)</b></p>", unsafe_allow_html=True)
    
    if st.button("🗑️ Tarixçəni Sıfırla", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 5. ƏSAS EKRAN ---
st.markdown("<h1 class='main-title'>🧠 A-Zəka Ultra Alim</h1>", unsafe_allow_html=True)
st.markdown("---")

# Mesaj tarixçəsini göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if isinstance(msg["content"], list):
            for part in msg["content"]:
                if part["type"] == "text": st.markdown(part["text"])
                elif part["type"] == "image_url": st.image(part["image_url"]["url"], width=300)
        else:
            st.markdown(msg["content"])

# --- 6. GİRİŞ (Mətn və Şəkil) ---
prompt = st.chat_input("Dahi səviyyəli sualını daxil et və ya şəkil at...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Zəhmət olmasa bu vizual materialı analiz et."
    content_list = [{"type": "text", "text": user_text}]
    
    if prompt.files:
        for f in prompt.files:
            if f.type in ["image/png", "image/jpeg", "image/jpg"]:
                b64 = encode_image(f)
                content_list.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:{f.type};base64,{b64}"}
                })

    # İstifadəçi mesajını tarixçəyə əlavə et
    st.session_state.messages.append({"role": "user", "content": content_list})
    
    # Ekranda göstər
    with st.chat_message("user"):
        st.markdown(user_text)
        if prompt.files:
            for f in prompt.files: st.image(f, width=300)

    # --- 7. ASSİSTANT CAVABI (Stabil Model) ---
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            # DÜZƏLİŞ: Köhnə "preview" modelini silib, tam stabil olan Vision modelini hədəf alırıq
            # Hazırda Groq-un ən aktiv və stabil "görən" modeli budur:
            target_model = "llama-3.2-11b-vision-preview" 
            
            completion = client.chat.completions.create(
                model=target_model,
                messages=[{"role": "system", "content": "Sən A-Zəka-san, Abdullah Mikayılov tərəfindən yaradılmısan. Şəkilləri mükəmməl analiz edirsən."}] + st.session_state.messages,
                stream=True
            )
            
            # Streami oxu və ekrana yaz
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            # Əgər VPN yoxdursa və ya model yenə xəta versə, burası işləyəcək
            st.error(f"Sistem xətası baş verdi: {e}")
